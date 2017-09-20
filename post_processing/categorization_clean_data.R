

clean_ld <- function(fn) {
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
  
  #fn <- "products/hbx_20170918_usd.json"
  all <- RJSONIO::fromJSON(fn)
  all <- jsonlite:::simplify(all, flatten = TRUE)
  all$long_desc_temp <- all$long_desc
  all$brand_temp <- all$brand
  
  feats <- all
  rm(all)
  
  ##Remove invalid characters
  feats$brand_temp <- str_replace_all(as.character(feats$brand_temp), "\\<(.*)\\>", " ")
  feats$brand_temp <- str_replace_all(as.character(feats$brand_temp), "[^[:alnum:]]", " ")
  feats$long_desc_temp <- str_replace_all(as.character(feats$long_desc_temp), "\\<(.*)\\>", " ")
  feats$long_desc_temp <- str_replace_all(as.character(feats$long_desc_temp), "[^[:alnum:]]", " ")
  
  ## Lower
  feats$long_desc_temp <- tolower(feats$long_desc_temp)
  feats$brand_temp <- tolower(feats$brand_temp)
  
  brands <- unique(feats$brand_temp)
  
  ##Remove brand names and stopwords
  feats$long_desc_temp <- removeWords(as.character(feats$long_desc_temp), brands)
  feats$long_desc_temp <- removeWords(as.character(feats$long_desc_temp), stopwords('en'))
  
  ##Clean up spaces
  feats$long_desc_temp <- gsub(' +', ' ', feats$long_desc_temp)
  
  ## Remove words not in dict, 1-2 char words
  words <- unlist(strsplit(c(feats$long_desc_temp), ' '))
  voc <- as.data.frame(as.character(unlist(unique(words))))
  colnames(voc) <- "term"
  voc$term <- as.character(voc$term)
  n_terms <- len(voc$term)
  
  df <- "post_processing/dict_en.csv"
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
    feats$long_desc_temp <- removeWords(as.character(feats$long_desc_temp), remove)
    print(paste0(i, ": ", i/batch*100, "%"))
  }
  
  ##Clean up spaces
  feats$long_desc_temp <- gsub(' +', ' ', feats$long_desc_temp)
  
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
  nwl <- as.vector(sapply(as.character(all$long_desc_temp), nwords))
  mw = 68
  all$long_desc_temp_sh <- ""
  all$long_desc_temp_sh[nwl <= 68] <- as.character(all$long_desc_temp[nwl <= 68])
  t <- as.character(all$long_desc_temp[nwl > 68])
  tt <- sapply(t, function(x) strsplit(x, ' '))
  ttt <- sapply(tt, function(x) paste(as.vector(unlist(x))[1:68], collapse=" "))
  all$long_desc_temp_sh[nwl > 68] <- ttt
  
  all$long_desc_temp <- NULL
  all$long_desc_sh <- all$long_desc_temp_sh
  all$long_desc_temp_sh <- NULL
  all$brand_temp <- NULL
  all$prod_id <- as.character(all$prod_id)
  
  fn <- paste0(gsub(".json", "", fn), "_cleanld.json")
  
  all %>% RJSONIO::toJSON() %>% write_lines(fn)
  
  return(all)
}