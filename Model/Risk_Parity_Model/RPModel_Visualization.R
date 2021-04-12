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

## Correlation
# input data
df_index <- read.csv('../../Data/Data_Outsample.csv',  fileEncoding="UTF-8")

df_index <- na.omit(df_index)
m_index <- as.matrix(df_index[2:ncol(df_index)])

# correlation calculation
cor_index = cor(m_index)
recor_index = melt(cor_index)

# plot correlation heatmap
CairoPDF("Heatmap_Cor_Asset.pdf",width = 7,height = 6)
ggplot(data = recor_index, aes(x=Var1, y=Var2, fill=value)) + 
    xlab("")+ ylab("") +
    scale_fill_gradient2(high = "#5E4FA2",mid="white",low="#F6FBB2")+
    theme(text=element_text(family="SimHei")) +
    theme(axis.text.x = element_text(angle = 90, vjust = 1, hjust = 1)) +
    geom_raster()
dev.off()



## Weights
# load and melt data
views <- read.table('view.csv',header=T,sep=",",fileEncoding="UTF-8")
colnames(views) <- c("Date",colnames(views)[2:16])
#views$Date <- as.Date(views$Date)
views_mt <- melt(views,id.vars = 1)
colnames(views_mt) = c("Date","Gp","Value")
head(views_mt)

# plot
CairoPDF('Heatmap_RP_Weight.pdf', width= 9, height = 4)
ggplot(data = views_mt, aes(x=Date, y=Gp, fill=Value)) + 
    xlab("")+ ylab("") +
    scale_fill_gradient2(high = "#5E4FA2")+
    theme(text=element_text(family="SimHei")) +
    theme(axis.text.x = element_text(angle = 90, vjust = 1, hjust = 1)) +
    geom_raster()
dev.off()


## Asset
asset <- read.table('RP_Asset.csv',header=T,sep=",",fileEncoding="UTF-8")
asset$Date <- as.Date(asset$Date)
asset <- melt(asset,id.vars = 1)
colnames(asset) <- c("Date","Model","Value")

# plot
CairoPDF('Heatmap_RP_Weight.pdf', width= 9, height = 4)
ggplot(data = views_mt, aes(x=Date, y=Gp, fill=Value)) + 
    xlab("")+ ylab("") +
    scale_fill_gradient2(high = "#5E4FA2")+
    theme(text=element_text(family="SimHei")) +
    theme(axis.text.x = element_text(angle = 90, vjust = 1, hjust = 1)) +
    geom_raster()
dev.off()