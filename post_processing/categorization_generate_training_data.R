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

all <- read.csv("post-processing/categorization_training_raw_50k.csv")
all$mcats <- as.character(all$mcats)
all$cat <- ""

words <- unlist(sapply(as.character(all$mcats), function(x) strsplit(x, ' ')))
words <- sapply(words, trim)
voc <- as.data.frame(unique(words))
colnames(voc) <- "term"
voc$count <- 0
voc$term <- as.character(voc$term)
n_terms <- len(voc$term)

for (i in 1:n_terms) {
  voc$count[i] <- sum(str_count(words, voc$term[i]))
  print(paste0(i, ": ", round(i/n_terms*100,2), "%"))
}


all$cat[grepl("\\bmen\\b", as.character(all$mcats))] <- "men"
all$cat[grepl("\\bwomen\\b", as.character(all$mcats))] <- "women"
all$cat[grepl("\\bhome\\b", as.character(all$mcats))] <- "home"
all$cat[grepl("\\bdecor\\b", as.character(all$mcats))] <- "home"
all$cat[grepl("\\bgarden\\b", as.character(all$mcats))] <- "home"
all$cat[grepl("\\bkitchen\\b", as.character(all$mcats))] <- "home"
all$cat[grepl("\\boffice\\b", as.character(all$mcats))] <- "home"
all$cat[grepl("\\bbeauty\\b", as.character(all$mcats))] <- "beauty & health"
all$cat[grepl("\\bwellness\\b", as.character(all$mcats))] <- "beauty & health"
all$cat[grepl("\\bdining\\b", as.character(all$mcats))] <- "home"
all$cat[grepl("\\btravel\\b", as.character(all$mcats))] <- "men & women"
all$cat[grepl("\\btech\\b", as.character(all$mcats))] <- "electronics"
all$cat[grepl("\\bpets\\b", as.character(all$mcats))] <- "others"
all$cat[grepl("\\btools\\b", as.character(all$mcats))] <- "others"
all$cat[grepl("\\boutdoor\\b", as.character(all$mcats))] <- "others"
all$cat[grepl("\\bfitness\\b", as.character(all$mcats))] <- "others"
all$cat[grepl("\\bkids\\b", as.character(all$mcats))] <- "kids"
all$cat[grepl("\\bart\\b", as.character(all$mcats))] <- "home"
all$cat[grepl("\\bboys\\b", as.character(all$mcats))] <- "kids"
all$cat[grepl("\\btoys\\b", as.character(all$mcats))] <- "kids"
all$cat[grepl("\\bdresses\\b", as.character(all$mcats))] <- "women"
all$cat[grepl("\\bshoes\\b", as.character(all$mcats)) & grepl("shoptiques", as.character(all$product_link))] <- "women"
all$cat[grepl("\\baccessories\\b", as.character(all$mcats)) & grepl("shoptiques", as.character(all$product_link))] <- "women"
all$cat[grepl("\\bclothing\\b", as.character(all$mcats)) & grepl("shoptiques", as.character(all$product_link))] <- "women"
all$cat[grepl("\\bbags\\b", as.character(all$mcats)) & grepl("shoptiques", as.character(all$product_link))] <- "women"
all$cat[grepl("outnet", as.character(all$product_link))] <- "women"


View(all[all$cat=="",])
print(paste0("Classified: ", round((1-sum(all$cat=="")/len(all$cat))*100,2), '%'))
print(paste0(sum(all$cat==""), " left"))



#View(all[grepl("shoptiques", as.character(all$product_link)) & all$cat=="",])
#zz = unique(unlist(sapply(all$mcats[as.character(all$cat)==""], function(x) strsplit(x, " "))))
#sort(zz)

#View(all[grepl(x, as.character(all$mcats)) & as.character(all$cat)=="",])
all$merchant <- ""
all$merchant[grepl("shoptiques", as.character(all$product_link))] <- "Shoptiques"
all$merchant[grepl("hbx", as.character(all$product_link))] <- "HBX"
all$merchant[grepl("outnet", as.character(all$product_link))] <- "The Outnet US"
all$merchant[grepl("ahalife", as.character(all$product_link))] <- "AHAlife"


all <- all[all$mcats!="" & all$mcats!=" ",]
all <- all[all$short_desc!="" & all$short_desc!=" ",]
all <- all[all$long_desc!="" & all$long_desc!=" ",]
all <- all[all$cat!="", ]

all <- unique(all)

set.seed(101417)
all$id <- ""
all$id <- sample(100000000:999999999, len(all$id), replace=FALSE)

all$duplicate <- FALSE
upl <- data.frame(unique(all$product_link))
colnames(upl) <- "product_link"

ulinks <- c()

all$product_link <- as.character(all$product_link)

for (i in 1:len(all$product_link)) {
  if (all$product_link[i] %in% ulinks) {
    all <- all[-i,]
  } else {
    ulinks <- c(ulinks, as.character(all$product_link[i]))
  }
  print(paste0(i, ": ", i/len(all$product_link)*100, "%"))
}

len(all$product_link)==len(unique(all$product_link))

require(stringr)
nwords <- function(string, pseudo=F){
  ifelse( pseudo, 
          pattern <- "\\S+", 
          pattern <- "[[:alpha:]]+" 
  )
  str_count(string, pattern)
}


## Shorten long descriptions to 68 words (max of outnet)
nwl <- as.vector(sapply(as.character(all$long_desc), nwords))
nwll <- as.vector(sapply(ttt, nwords))
mw = 68
all$long_desc_sh <- ""
all$long_desc_sh[nwl <= 68] <- as.character(all$long_desc[nwl <= 68])
t <- as.character(all$long_desc[nwl > 68])
tt <- sapply(t, function(x) strsplit(x, ' '))
ttt <- sapply(tt, function(x) paste(as.vector(unlist(x))[1:68], collapse=" "))
all$long_desc_sh[nwl > 68] <- ttt

write.csv(all, "post-processing/cat_tr_t_raw_Xy_50w.csv")
