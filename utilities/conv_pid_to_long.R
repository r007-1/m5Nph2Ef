################################################################
### Convert prod_id from concatenated long to long
################################################################

Sys.setlocale("LC_ALL", "C")
options(digits=22)
len <- function(x) {
  return(length(x))
}

str <- function(x) {
  return(as.character(x))
}

### Load libraries

library(raster)
library(readr)
library(jsonlite)
library(magrittr)
library(RJSONIO)

### Set directory
setwd("~/Documents/pipeline_old/m5Nph2Ef")


### Load original files
fps <- c("products/shoptiques_20170809_clean.json", "products/hbx_20170807_clean.json")
#fps <- c("test/shoptiques_2017-08-04.json", "products/shoptiques2-edited.json", "products/hbx_2017-08-03.json")
cnames <- ""
s <- list()
alldf <- data.frame()
for (i in 1:len(fps)) {
  fp <- fps[i]
  s <- c(s, list(RJSONIO::fromJSON(fp)))
  if (i==1) {
    s1a <- s[[i]][[1]]
    s1b <- s[[i]][[2]]
    s1 <- c(s1a, s1b)
    s[[1]] <- s1
    rm(s1)
    rm(s1a)
    rm(s1b)
  }
  s[[i]]$imglinks <- NULL
  for (z in 1:len(s[[i]])) {
    s[[i]][[z]]$prod_id <- str(s[[i]][[z]]$prod_id)
  }
}

z <- c(s[[1]], s[[2]])

## Sanity check!!
pids <- sapply(z, function(x) x$prod_id)
len(pids) == len(unique(pids))

z %>% RJSONIO::toJSON() %>% write_lines("batch/20170817_st_hbx_3.json")

z %>% RJSONIO::toJSON(encoding="UTF-8") %>% write_lines("batch/20170817_st_hbx_4.json")



