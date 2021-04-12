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

## Time Series Heatmap
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

######## Plotting starts here#####################
options(warn=-1)
CairoPDF("Heatmap_RP_TS_Weights.pdf",width = 12,height = 11)
ggplot(df,aes(day,Asset,fill=Value))+
    geom_tile(color= "white",size=0.1) + 
    scale_fill_viridis(name="权重",option ="C") +
    facet_grid(year~month) + 
    labs(title= "权重热图--风险平价", x="时间-工作日", y="大类资产") +
    scale_y_discrete( breaks = unique(df$Asset)) +
    scale_x_continuous(breaks =c(1,10,20,31)) +
    theme_minimal(base_size = 8) + 
    theme(legend.position = "bottom")+
    theme(text=element_text(family="SimHei")) +
    theme(plot.title=element_text(size = 14))+
    theme(axis.text.y=element_text(size=6)) +
    theme(plot.title=element_text(size = 14))+
    theme(axis.text.y=element_text(size=6)) +
    theme(plot.title=element_text(size = 14))+
    theme(axis.text.y=element_text(size=6)) +
    theme(strip.background = element_rect(colour="white"))+
    theme(plot.title=element_text(hjust=0))+
    theme(axis.ticks=element_blank())+
    theme(axis.text=element_text(size=7))+
    theme(legend.title=element_text(size=8))+
    theme(legend.text=element_text(size=6))+
    removeGrid()
dev.off()