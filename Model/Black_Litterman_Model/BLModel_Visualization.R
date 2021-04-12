library(dplyr) # easier data wrangling 
library(viridis) # colour blind friendly palette, works in B&W also
library(Interpol.T) #  will generate a large dataset on initial load
library(lubridate) # for easy date manipulation
library(ggExtra) # because remembering ggplot theme options is beyond me
library(tidyr) 
library(plotly)
library(hrbrthemes)
library(ggplot2)
library(readxl)
library(pheatmap)
library(reshape2)
library(RColorBrewer)
library(Cairo)

# set current path as working directory
setwd("../Black_Litterman_Model")
options (warn = -1)



## Asset
asset <- read.table('BL_Asset.csv',header=T,sep=",",fileEncoding="UTF-8")
colnames(asset) <- c("Date",colnames(asset)[2:3])
asset$Date <- as.Date(asset$Date)
asset <- melt(asset,id.vars = 1)
colnames(asset) <- c("Date","Model","Value")

# plot
CairoPDF('BL_Asset.pdf', width= 9, height = 4)

ggplot() +
    geom_line(data = asset, aes(x=Date, y=Value,color=Model),) +
    theme_ipsum() + theme_bw() + theme(legend.position="right") +
    theme(panel.border = element_blank(),
          axis.line = element_line(colour = "white")) +
    theme(plot.title = element_text(size=10))
dev.off()

## Heatmap
# load data
df <- read.table('view.csv',  sep=",",header=1,fileEncoding="UTF-8")
colnames(df) <- c("Date",colnames(df)[2:length(colnames(df))])
df$Date <- ymd(df$Date)

# melt
df <- melt(df,id.vars = 1)
colnames(df) <- c("Date","Asset","Value")
df$Asset <- as.factor(df$Asset)


df <- df %>% mutate(year = year(Date),
                  month = month(Date, label=TRUE),
                  day = day(Date))

# fill missing value
df <-df %>% select(day,Asset,month,year,Value)%>%
        fill(Value) 