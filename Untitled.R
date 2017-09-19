Sys.setlocale("LC_ALL", "C")
len <- function(x) {
  return(length(x))
}
options(digits=22)

### Load libraries
library(raster)
library(readr)
library(jsonlite)
library(magrittr)
library(RJSONIO)
library(tensorflow)
library(tm)
library(stringr)
library(RCurl)

### Set directory
setwd("~/Documents/pipeline_old/m5Nph2Ef")

all <- RJSONIO::fromJSON("batch/2017-08-09.json")
data <- all[sample(1:length(all), 50000)]

merchants <- sapply(data, '[[', "merchant")
asos <- data[merchants=="ASOS US"]
st <- data[merchants=="Shoptiques"]
hbx <- data[merchants=="HBX"]
on <- data[merchants=="The Outnet US"]
al <- data[merchants=="AHAlife"]
data <- list(asos, st, hbx, on, al)

x <- data.frame()

for (i in 1:len(data)) {
  cn <- names(data[[i]][[1]])
  nr <- length(data[[i]])
  nvs <- sapply(data[[i]], length)
  data[[i]] <- data[[i]][nvs==43]
  a <- data.frame(matrix(unlist(data[[i]]), nrow=length(data[[i]]), byrow=T))
  colnames(a) <- cn
  include <- c("prod_id", "product_link", "brand", "cat_1", "cat_2", "cat_3", "cat_code", "long_desc", "merchant", "mcat_1", "mcat_2", "mcat_3", "mcat_4", "mcat_5", "short_desc")
  x <- rbind(x, a[,include])
}

x <- x[x$merchant != "ASOS US",]

it1 <- x[,c("prod_id", "product_link", "short_desc")]
it2 <- x[,c("prod_id", "product_link", "long_desc")]
it3 <- cbind(x[,c("prod_id", "product_link")], mcats=trim(paste(x$mcat_1, x$mcat_2, x$mcat_3, x$mcat_4, x$mcat_5)))
it4 <- cbind(x[,c("prod_id", "product_link")], tags=paste(trim(paste(x$mcat_1, x$mcat_2, x$mcat_3, x$mcat_4, x$mcat_5)), trim(as.character(x$short_desc)), trim(as.character(x$long_desc))))

write.csv(it1, file="post-processing/test_it1.csv", row.names=FALSE)
write.csv(it2, file="post-processing/test_it2.csv", row.names=FALSE)
write.csv(it3, file="post-processing/test_it3.csv", row.names=FALSE)
write.csv(it4, file="post-processing/test_it4.csv", row.names=FALSE)
write.csv(it4, file="post-processing/all_it4.csv", row.names=FALSE)


feats <- cbind(product_link=as.character(x$product_link))
feats <- cbind(feats, mcats = trim(paste(x$mcat_1, x$mcat_2, x$mcat_3, x$mcat_4, x$mcat_5)))
feats <- cbind(feats, x[,c("short_desc", "long_desc")])
brands <- unique(c(as.character(x$brand), as.character(x$merchant)))


##Remove invalid characters
feats$short_desc <- str_replace_all(as.character(feats$short_desc), "\\<(.*)\\>", " ")
feats$mcats <- str_replace_all(as.character(feats$mcats), "\\<(.*)\\>", " ")
feats$long_desc <- str_replace_all(as.character(feats$long_desc), "\\<(.*)\\>", " ")
brands <- str_replace_all(as.character(brands), "\\<(.*)\\>", " ")

feats$short_desc <- str_replace_all(as.character(feats$short_desc), "[^[:alnum:]]", " ")
feats$mcats <- str_replace_all(as.character(feats$mcats), "[^[:alnum:]]", " ")
feats$long_desc <- str_replace_all(as.character(feats$long_desc), "[^[:alnum:]]", " ")
brands <- str_replace_all(as.character(brands), "[^[:alnum:]]", " ")


## Lower
feats$short_desc <- tolower(feats$short_desc)
feats$long_desc <- tolower(feats$long_desc)
feats$mcats <- tolower(feats$mcats)
brands <- tolower(feats$brands)


##Remove brand names and stopwords
feats$short_desc <- removeWords(as.character(feats$short_desc), brands)
feats$long_desc <- removeWords(as.character(feats$long_desc), brands)
feats$short_desc <- removeWords(as.character(feats$short_desc), stopwords('en'))
feats$long_desc <- removeWords(as.character(feats$long_desc), stopwords('en'))


##Clean up spaces
feats$short_desc <- gsub(' +', ' ', feats$short_desc)
feats$long_desc <- gsub(' +', ' ', feats$long_desc)
feats$mcats <- gsub(' +', ' ', feats$mcats)


##### Move to separate file
## Create occurrence table for words in data
##TODO
read_from_file <- FALSE
if (read_from_file) {
  #voc <- read.csv("post-processing/glarket_corpus.csv")
} else {
  words <- unlist(strsplit(c(feats$mcats, feats$short_desc, feats$long_desc), ' '))
  voc <- as.data.frame(as.character(unlist(unique(words))))
  colnames(voc) <- "term"
  voc$count <- 0
  voc$term <- as.character(voc$term)
  n_terms <- len(voc$term)
  
  for (i in 1:n_terms) {
    voc$count[i] <- sum(str_count(words, voc$term[i]))
    print(paste0(i, ": ", round(i/n_terms*100,2), "%"))
  }
  
  d_url <- "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
  df <- "post-processing/dict_en.csv"
  download.file(d_url, destfile = df, method="curl")
  dict <- read.csv(df)
  dict <- as.character(dict$a)
  #write.csv(voc, "post-processing/glarket_corpus.csv")
}


## Remove low-frequency words, words not in dict, 1-2 char words
v <- voc$term
nc <- sapply(v, nchar)
keep <- v %in% dict
rm <- v[!keep | voc$count <= 3 | nc < 3]
vv <- v[!(v %in% rm)]

batch <- ceiling(len(rm)/100)
for (i in 1:batch) {
  remove <- rm[((i-1)*100+1):(min(len(rm),i*100))]
  feats$mcats <- removeWords(as.character(feats$mcats), remove)
  feats$short_desc <- removeWords(as.character(feats$short_desc), remove)
  feats$long_desc <- removeWords(as.character(feats$long_desc), remove)
  print(paste0(i, ": ", i/batch*100, "%"))
}

##Clean up spaces
feats$short_desc <- gsub(' +', ' ', feats$short_desc)
feats$long_desc <- gsub(' +', ' ', feats$long_desc)
feats$mcats <- gsub(' +', ' ', feats$mcats)


fn <- "post-processing/categorization_training_raw_50k.csv"
write.csv(feats, file=fn, row.names=FALSE)


x <- x[,c("merchant", "mcat_1", "mcat_2", "mcat_3", "mcat_4", "mcat_5")]
x <- unique(x)
