#Hierarchical clustering

dataset <- read.csv('Mall_Customers.csv')
x <- dataset[4:5]

#Using a dendrogram to find optimal number of clusters
dendrogram <- hclust(dist(x, method = 'euclidean'), method = 'ward.D')

plot(dendrogram, 
     main = paste('Dendrogram'),
     xlab = 'Customers',
     ylab = 'Euclidean distances')

#Fitting hiearchcical clustering to mall dataset
#5 clusters
hc <- hclust(dist(x, method = 'euclidian'), method = 'ward.D')
y_hc <- cutree(hc, 5)

#6 clusters
hc2 <- hclust(dist(x, method = 'euclidian'), method = 'ward.D')
y_hc2 <- cutree(hc, 6)

#Visualizing the clusters
library(cluster)
clusplot(x, 
         y_hc,
         lines = 0, 
         shade = TRUE,
         color = TRUE,
         labels = 2,
         plotchar = FALSE,
         span = TRUE,
         main = paste('Clusters of customers'),
         xlab = 'Annual Income',
         ylab = 'Spending Score')

clusplot(x, 
         y_hc2,
         lines = 0, 
         shade = TRUE,
         color = TRUE,
         labels = 2,
         plotchar = FALSE,
         span = TRUE,
         main = paste('Clusters of customers'),
         xlab = 'Annual Income',
         ylab = 'Spending Score')