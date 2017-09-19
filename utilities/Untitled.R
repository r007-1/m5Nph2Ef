
len <- function(x) {
  return(length(x))
}

### Load libraries
Sys.setlocale("LC_ALL", "C")
options(digits=22)
library(raster)
library(readr)
library(jsonlite)
library(magrittr)
library(RJSONIO)

### Set directory
setwd("~/Documents/pipeline_old/m5Nph2Ef")


### List files
fps <- c("test/shoptiques_2017-08-04.json", "test/ahalife_2017-08-04.json", "test/theoutnet-us_2017-08-03.json")
fps <- c(fps, "products/asos-us_2017-08-03.json", "products/hbx_2017-08-03.json", "products/shoptiques2-edited.json")
cnames <- ""
s <- list()

for (i in 1:length(fps)) {
  fp <- fps[i]
  ### Load json file
  s <- c(s, list(fromJSON(fp)))
  if (i==6) {
    s[[6]] <- s[[6]][[1]]
    s[[6]]$imglinks <- NULL
    ss[[6]] <- as.data.frame(s[[6]])[1:100,]
  } else {
    ss <- s[[i]][1:100]
    for (i in 1:100) {
      ss[[i]]$imglinks <- NULL
    }
  }
  
  ### Get and simplify sample
  if (fp==fps[1]) {
    cnames <- names(ss[[1]])
    df <- data.frame(matrix(unlist(ss), nrow=100, byrow=T))
    colnames(df) <- cnames
  } else {
    if (i==5){
      for (i in 1:100) {
        ss[[i]]$image_urls <- ""
        ss[[i]]$tags <- trim(paste(ss[[i]]$tags, collapse=" "))
      }
    }
    if (i!= 6) {
      cnames <- names(ss[[i]])
      tdf <- data.frame(matrix(unlist(ss), nrow=100, byrow=T))
    } else {
      cnames <- colnames(ss[[6]])
      tdf <- ss[[6]]
    }
    colnames(tdf) <- cnames
    df <- rbind(df, tdf)
  }
}






###HBX EDIT
for (i in 1:length(s[[5]])) {
  s[[5]][[i]]$image_urls <- ""
  s[[5]][[i]]$tags <- trim(paste(s[[5]][[i]]$tags, collapse=" "))
}

### ASOS EDIT
df$on_sale[df$merchant=="ASOS US" & df$on_sale==0] <- FALSE
df$on_sale[df$merchant=="ASOS US" & df$on_sale==1] <- TRUE
for (i in 1:length(s[[4]])) {
  if (s[[4]][[i]]$on_sale == 0) {
    s[[4]][[i]]$on_sale <- FALSE
  } else {
    s[[4]][[i]]$on_sale <- TRUE
  }
}

### Save individually as JSON
for (i in 1:length(s)) {
  if (i!=1 & i!=6) {
    fname <- tolower(gsub(" ", "-", s[[i]][[1]]$merchant))
    fname <- paste0("products/", fname, "_20170807_clean.json")
    j <- s[[i]]
    j %>% toJSON() %>% write_lines(fname)
  }
}

### Save all




## MERGE
fps <- c("products/ahalife_20170807_clean.json", "products/the-outnet-us_20170807_clean.json", "products/asos-us_20170807_clean.json", "products/hbx_20170807_clean.json")
fps <- c(fps, "products/shoptiques_20170809_clean.json")

j <- NULL
for (i in 1:length(fps)) {
  j <- c(j, RJSONIO::fromJSON(fps[i]))
  if (i==5) {
    j5 <- RJSONIO::fromJSON(fps[i])
    j <- c(j, j5[[1]], j5[[2]])
  }
}

### Save as JSON
fname <- paste0("batch/", "test.json")
j %>% RJSONIO::toJSON() %>% write_lines(fname)

rm(j)

## TEST
jj <- RJSONIO::fromJSON(fname)
len(jj)
jj[[1]]$merchant
jj[[len(jj)]]$merchant


rm(jj)



all <- RJSONIO::fromJSON("batch/2017-08-09.json")

#t <- all
links <- NULL
for (i in 1:length(all)) {
  links <- c(links, all[[i]]$product_link)
}


l = links

batch = ceiling(length(links)/100.0)
u = TRUE
for (i in 1:batch) {
  start <- (i-1)*100+1
  end <- min(i*100, length(links))
  s <- links[start:end]
  u = length(unique(s)) == length(s)
  print(u)
  print(end)
}



t %>% rjson::toJSON() %>% write_lines("batch/2017-08-09.json")

t %>% RJSONIO::toJSON(encoding='UTF-8') %>% write_lines("batch/testenc6.json")


#all %>% RJSONIO::toJSON(encoding='UTF-8') %>% write_lines("batch/20170809.json")

test <- RJSONIO::fromJSON("batch/testenc6.json")

gsub("\"", "", ugh)


all <- RJSONIO::fromJSON("batch/2017-08-09.json")
#a <- as.data.frame(all)
test <- all[sample(1:len(all), 1000)]
test_backup <- test
t <- data.frame()

for (i in 1:len(test)) {
  test[[i]]['prod_id'] <- as.character(test[[i]]['prod_id'])
  t <- rbind(t, as.data.frame(test[[i]]))
}

t <- t[,c("cat_1", "cat_2", "cat_3", "long_desc", "mcat_1", "mcat_2", "mcat_3", "mcat_4", "mcat_5", "merchant", "brand", "short_desc", "tags")]



