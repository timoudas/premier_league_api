install.packages("jsonlite")

library("jsonlite")
data <- "gk.json"
json_data <- fromJSON(paste(readLines(data), collapse=""))

