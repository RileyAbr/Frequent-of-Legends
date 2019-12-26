library(arules)

X = read.table("../win_transactions.txt",header = TRUE)
n = dim(X)[1]
Xp <- as(as.matrix(X), "itemMatrix")
itemSetsX <- apriori(Xp, parameter = list(support= 0.01, target="frequent"))

d = length(itemSetsX) #Number of frequent itemsets
outMatrix = matrix(0,n,d) #trans and frequent itemset.

for(i in 1:d){
  l = as(itemSetsX[i]@items,"list")[[1]]
  print(l)  #itemsets
  Xl = X[,l]
  if (length(l)==1)
    rr=which(Xl==1)
  else
    rr = which(rowSums(Xl) == length(l))
  
  outMatrix[rr,i] = 1
}

Xneg = read.table("../loss_transactions.txt",header = TRUE)
nneg = dim(Xneg)[1]
Xn <- as(as.matrix(Xneg), "itemMatrix")
itemSetsXn <- apriori(Xn, parameter = list(support= 0.01, target="frequent"))

d = length(itemSetsXn) #Number of frequent itemsets
outMatrixNeg = matrix(0,nneg,d)
for(i in 1:d){
  l = as(itemSetsXn[i]@items,"list")[[1]]
  print(l)  #itemsets
  Xl = Xneg[,l]
  if (length(l)==1)
    rr=which(Xl==1)
  else
    rr = which(rowSums(Xl) == length(l))
  
  outMatrixNeg[rr,i] = 1
}

#totalMatrix = rbind(outMatrix, outMatrixNeg, deparse.level = 1)
#print(totalMatrix)