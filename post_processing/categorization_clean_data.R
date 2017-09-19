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

fn <- "post_processing/categorization_all_raw_091517.csv"
all <- read.csv(fn)

fn <- "products/hbx_20170918_usd.json"
all <- RJSONIO::fromJSON(fn)
a <- all

aa <- all[1:10]
al <- data.frame(aa)

View(head(all))
all$X <- NULL
#data <- all
#x <- data
#feats <- x

feats <- all
rm(all)

##Remove invalid characters
feats$long_desc <- str_replace_all(as.character(feats$long_desc), "\\<(.*)\\>", " ")
feats$long_desc <- str_replace_all(as.character(feats$long_desc), "[^[:alnum:]]", " ")

## Lower
feats$long_desc <- tolower(feats$long_desc)

##Remove brand names and stopwords
feats$long_desc <- removeWords(as.character(feats$long_desc), brands) ##TODO
feats$long_desc <- removeWords(as.character(feats$long_desc), stopwords('en'))

##Clean up spaces
feats$long_desc <- gsub(' +', ' ', feats$long_desc)

## Remove words not in dict, 1-2 char words
words <- unlist(strsplit(c(feats$long_desc), ' '))
voc <- as.data.frame(as.character(unlist(unique(words))))
colnames(voc) <- "term"
voc$term <- as.character(voc$term)
n_terms <- len(voc$term)

df <- "post-processing/dict_en.csv"
dict <- read.csv(df)
dict <- as.character(dict$a)

v <- voc$term
nc <- sapply(v, nchar)
keep <- v %in% dict
rm <- v[!keep | nc < 3]
vv <- v[!(v %in% rm)]

batch <- ceiling(len(rm)/100)
for (i in 1:batch) {
  remove <- rm[((i-1)*100+1):(min(len(rm),i*100))]
  feats$long_desc <- removeWords(as.character(feats$long_desc), remove)
  print(paste0(i, ": ", i/batch*100, "%"))
}

##Clean up spaces
feats$long_desc <- gsub(' +', ' ', feats$long_desc)

nwords <- function(string, pseudo=F){
  ifelse( pseudo, 
          pattern <- "\\S+", 
          pattern <- "[[:alpha:]]+" 
  )
  str_count(string, pattern)
}


all <- feats
rm(feats)

## Shorten long descriptions to 68 words (max of outnet)
nwl <- as.vector(sapply(as.character(all$long_desc), nwords))
mw = 68
all$long_desc_sh <- ""
all$long_desc_sh[nwl <= 68] <- as.character(all$long_desc[nwl <= 68])
t <- as.character(all$long_desc[nwl > 68])
tt <- sapply(t, function(x) strsplit(x, ' '))
ttt <- sapply(tt, function(x) paste(as.vector(unlist(x))[1:68], collapse=" "))
all$long_desc_sh[nwl > 68] <- ttt

fn <- "post-processing/categorization_all_input_clean_091517.csv"
all <- all[,c("product_link", "long_desc_sh")]
write.csv(all, file=fn, row.names=FALSE)
