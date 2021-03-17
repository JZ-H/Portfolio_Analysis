rm(list=ls())

library(ggplot2)
library(RColorBrewer)

# Dummy data
x <- LETTERS[1:20]
y <- paste0("var", seq(1,1000))
data <- expand.grid(X=x, Y=y)
data$Z <- runif(10000, 0, 5)

# Heatmap

ggplot(data, aes(X, Y, fill= Z)) + 
  geom_tile() +
  scale_y_discrete(breaks=y[seq(10,1000,200)]) +
  ylab("Date") + xlab("") +
  coord_flip()


# Save graph
ggsave("View_Matrix.png", plot = last_plot(), 
       path = "D:\\VSC\\Portfolio_Analysis\\Visualization\\", dpi = 1024)
