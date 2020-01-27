#PCA

dataset <- read.csv('Wine.csv')

#Splitting dataset
install.packages('caTools')
library(caTools)
set.seed(123)
split = sample.split(dataset$Customer_Segment, SplitRatio = 0.8)
training_set <- subset(dataset, split == TRUE)
test_set <- subset(dataset, split == FALSE)

#Feature Scaling
training_set[-14] = scale(training_set[-14])
test_set[-14] = scale(test_set[-14])

#Applying PCA
library(caret)
install.packages('e1071')
library(e1071)

pca <- preProcess(training_set[-14], method = 'pca', pcaComp = 2)
pca_training_set <- predict(pca, training_set)
pca_training_set <- pca_training_set[c(2, 3, 1)]
pca_test_set <- predict(pca, test_set)
pca_test_set <- pca_test_set[c(2, 3, 1)]

#Fitting SVM to model
classifier = svm(formula = Customer_Segment ~ .,
                 data = pca_training_set,
                 type = 'C-classification',
                 kernel = 'linear')

y_pred <- predict(classifier, newdata = pca_test_set[-3])

#Confusion Matrix
cm = table(pca_test_set[, 3], y_pred)

#Visualizing Training Set
install.packages('ElemStatLearn')
library(ElemStatLearn)
set <- pca_training_set
x1 <- seq(min(set[, 1]) -1, max(set[, 1]) +1, by = 0.01)
x2 <- seq(min(set[, 2]) -1, max(set[, 2]) +1, by = 0.01)
grid_set <- expand.grid(x1, x2)
colnames(grid_set) = c('PC1', 'PC2')
y_grid <- predict(classifier, newdata = grid_set)
plot(set[, 3],
     main = 'SVM(Training set)',
     xlab = 'PC1', ylab = 'PC2',
     xlim = range(x1), ylim = range(x2))
contour(x1, x2, matrix(as.numeric(y_grid), length(x1), length(x2)), add = TRUE)
points(grid_set, pch = '.', col = ifelse(y_grid == 2, 'deepskyblue', ifelse(y_grid == 1, 'springgreen3', 'tomato')))
points(set, pch = 21, bg = ifelse(set[, 3] == 2, 'blue3', ifelse(set[, 3] == 1, 'green4', 'red3')))

set <- pca_test_set
x1 <- seq(min(set[, 1]) -1, max(set[, 1]) +1, by = 0.01)
x2 <- seq(min(set[, 2]) -1, max(set[, 2]) +1, by = 0.01)
grid_set <- expand.grid(x1, x2)
colnames(grid_set) = c('PC1', 'PC2')
y_grid <- predict(classifier, newdata = grid_set)
plot(set[, 3],
     main = 'SVM(Training set)',
     xlab = 'PC1', ylab = 'PC2',
     xlim = range(x1), ylim = range(x2))
contour(x1, x2, matrix(as.numeric(y_grid), length(x1), length(x2)), add = TRUE)
points(grid_set, pch = '.', col = ifelse(y_grid == 2, 'deepskyblue', ifelse(y_grid == 1, 'springgreen3', 'tomato')))
points(set, pch = 21, bg = ifelse(set[, 3] == 2, 'blue3', ifelse(set[, 3] == 1, 'green4', 'red3')))


