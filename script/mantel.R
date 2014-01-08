install.packages("vegan")
library(vegan)
//read file into string
slopetxt<-readChar("Slope10.txt", file.info("Slope10.txt")$size)
//read string into a matrix -> has to be diagonal (that's fill) and you tell it # of columns
slopedmat<-data.matrix(read.table(text=slopetxt, fill=T, col.names=paste("V", 2:71)))
//converts diagonal to symetric matrix
slopedmat[upper.tri(slopedmat)]<-t(slopedmat)[upper.tri(slopedmat)]

//do that for all your files, then mantel:
//as.dist converts the matrix to a distance object for the test, update permutations

mantel(as.dist(eucdmat), as.dist(rousdmat), method="pearson", permutations=99)

mantel.partial(as.dist(rousdmat), as.dist(slopedmat), as.dist(eucdmat), method="pearson", permutations=9999)

