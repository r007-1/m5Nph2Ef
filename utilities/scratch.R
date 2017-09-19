Sys.setlocale("LC_ALL", "C")
len <- function(x) {
  return(length(x))
}

### Load libraries

library(raster)
library(readr)
library(jsonlite)
library(magrittr)
library(RJSONIO)

### Set directory
setwd("~/Documents/pipeline_old/m5Nph2Ef")


### List files
fps <- c("test/shoptiques_2017-08-04.json", "products/shoptiques2-edited.json")
cnames <- ""
s <- list()
alldf <- data.frame()

for (i in 1:2) {
  fp <- fps[i]
  s <- c(s, list(fromJSON(fp)))
  
  s[[i]]$imglinks <- NULL
  ss <- as.data.frame(s[[i]])[1:100,]
  
  df <- ss
  
  alldf <- rbind(alldf, df)
}

### Double check


### Merge
j1 <- fromJSON(fps[1])
j1$imglinks <- NULL
j2 <- fromJSON(fps[2])
j2$imglinks <- NULL
j <- list(j1, j2)
jj <- toJSON(j)

## Check
len(jj)



### Save as JSON
fname <- tolower(gsub(" ", "-", "shoptiques"))
fname <- paste0("products/", fname, "_20170809_clean_2.json")
j <- jj
j %>% write_lines(fname)


## Check
fp <- "products/shoptiques_20170809_clean_2.json"
zz<- RJSONIO::fromJSON(fps[1])

zz<- RJSONIO::fromJSON("batch/20170817_st_hbx_2.json")

all <- RJSONIO::fromJSON("batch/2017-08-09.json")



