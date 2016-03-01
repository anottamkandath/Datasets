library(e1071)
library(lattice)

graph_trust_level_boolean<-function(data,threshold){
	data1<-data[,c('score','typingDuration','c')]
	data1$c<-data1$c>threshold
	data1$c<-factor(data1$c,labels=c('N','T'))
	model  <- svm(formula=c~.,data = data1)
	pdf(paste("trust_level_threshold_",threshold,".pdf"))
	plot(model,data1)
	dev.off()
}

graph_trust_level_boolean_limit<-function(data,threshold){
	data1<-data[,c('score','typingDuration','c')]
	data1<-subset(data1,typingDuration<1000)
	data1<-subset(data1,c<20)
	data1$c<-data1$c>threshold
	data1$c<-factor(data1$c,labels=c('N','T'))
	model  <- svm(formula=c~.,data = data1)
	pdf(paste("trust_level_threshold_limit_",threshold,".pdf"))
	plot(model,data1)
	dev.off()
}

graph_trust_level_limit<-function(data){
	data1<-data[,c('score','typingDuration','c')]
	data1<-subset(data1,typingDuration<1000)
	data1<-subset(data1,c<10)
	data1$c<-factor(data1$c,labels=seq(1,length(unique(data1$c))))
	model  <- svm(formula=c~.,data = data1)
	pdf("trust_level_limit.pdf")
	plot(model,data1)
	dev.off()
}

graph_trust_level_limit_sl<-function(data){
	data1<-data[,c('score','typingDuration','c')]
	data1<-subset(data1,typingDuration<1000)
	data1<-subset(data1,c<20)
	data1$c<-(data1$c/(data1$c+2))
	data1$c<-ceiling(data1$c*10)
	data1$c<-factor(data1$c,labels=seq(1,length(unique(data1$c))))
	model  <- svm(formula=c~.,data = data1)
	pdf("trust_level_limit_sl.pdf")
	plot(model,data1)
	dev.off()
}


graph_trust_level_limit_sl_hour<-function(data){
	data1<-data[,c('hour','typingDuration','c')]
	data1<-subset(data1,typingDuration<1000)
	data1<-subset(data1,c<20)
	data1$c<-(data1$c/(data1$c+2))
	data1$c<-ceiling(data1$c*10)
	data1$c<-factor(data1$c,labels=seq(1,length(unique(data1$c))))
	model  <- svm(formula=c~.,data = data1)
	pdf("trust_level_limit_sl_hour.pdf")
	plot(model,data1)
	dev.off()
}

graph_trust_level_limit_sl_dayOfWeek<-function(data){
	data1<-data[,c('dayOfWeek','typingDuration','c')]
	data1<-subset(data1,typingDuration<1000)
	data1<-subset(data1,c<20)
	data1$c<-(data1$c/(data1$c+2))
	data1$c<-ceiling(data1$c*10)
	data1$c<-factor(data1$c,labels=seq(1,length(unique(data1$c))))
	model  <- svm(formula=c~.,data = data1)
	pdf("trust_level_limit_sl_dayOfWeek.pdf")
	plot(model,data1)
	dev.off()
}

compute_belief<-function(p=0,n=0,r=2){
	p/(p+n+r)
}

graph_trust_level<-function(data,fields,fl=TRUE,sl=TRUE){
	data1<-data[,fields]
	data1<-data1[fl & sl,]
	data1$c<-(data1$c/(data1$c+2))
	data1$c<-ceiling(data1$c*10)
	data1$c<-factor(data1$c,labels=seq(1,length(unique(data1$c))))
	#model  <- svm(formula=c~.,data = data1)
	#pdf("trust_level.pdf")
	#plot(model,data1)
	#dev.off()
	index <- 1:nrow(data1)
	testindex <- sample(index, trunc(length(index)*30/100))
	testset <- data1[testindex,]
	trainset <- data1[-testindex,]
	tuned <- tune.svm(c~., data = trainset, gamma = 10^(-6:-1), cost = 10^(-1:1))
	s<-summary(tuned)
	model  <- svm(c~., data = trainset, kernel="radial", gamma=s$best.parameters$gamma, cost=s$best.parameters$cost)
	prediction <- predict(model, testset[,-3])
	tab <- table(pred = prediction, true = testset[,3]) 
}


for(i in 1:nrow(d)){
  for(j in 1:nrow(d)){
    if(d$name[i]==d$name[j]){
      d$match[i]<-d$match[i]+exp(-(abs(d$time[j]-d$time[i])/1000)*0.2)
    }
  }
}

con <- dbConnect(MySQL(), user="root", dbname="mbh", host="localhost")
data <- dbGetQuery(con, "select * from TagEntry")



for (i in 1:nrow(videos)){
  d<-data[data$video_id==videos[i,],]
  print(nrow(d))
  print(i)
  u <- unique(d$normalizedTag)
  for(j in 1:length(u)){
    d1<-d[d$normalizedTag==u[j],]
    for(k in 1:nrow(d1)){
      for(z in k:nrow(d1)){
        s<-exp(-(abs(d1$gametime[k]-d1$gametime[z])*0.0002))
        data$match[data$id==d1$id[k]]<-data$match[data$id==d1$id[k]]+s
        data$match[data$id==d1$id[z]]<-data$match[data$id==d1$id[z]]+s
      }
    }
  }
}


for (i in 13:length(tags)){
  d<-data[data$normalizedTag==tags[i],]
  print(paste(i," ",nrow(d)))
  u <- unique(d$video_id)
  for(j in 1:length(u)){
    d1<-d[d$video_id==u[j],]
    for(k in 1:nrow(d1)){
      for(z in k:nrow(d1)){
        s<-exp(-(abs(d1$gametime[k]-d1$gametime[z])*0.0002))
        data$match[data$id==d1$id[k]]<-data$match[data$id==d1$id[k]]+s
        data$match[data$id==d1$id[z]]<-data$match[data$id==d1$id[z]]+s
      }
    }
  }
}

graph_pca<-function(data){
  dat[,"match"]<-((dat[,"match"]+1)/(dat[,"match"]+2))
  #data[,5]<-floor(data[,5]*10)
  dat[,"match"]<-round(dat[,"match"]*20)/2
  #data[,6]<-data[,6]
  #data[,6]<-factor(data[,6],labels=seq(1,length(unique(data[,6]))))
  dat[,"match"]<-factor(dat[,"match"])
  index <- length(dat[,"match"])
  trainindex <- 1:trunc(index*70/100)
  testset <- dat[-trainindex,]
  trainset <- dat[trainindex,]
  tuned <- tune.svm(match~., data = trainset, gamma = 10^(-6:-1), cost = 10^(-1:1))
  s<-summary(tuned)
  model  <- svm(match~., data = trainset, kernel="radial", gamma=s$best.parameters$gamma, cost=s$best.parameters$cost)
  prediction <- predict(model, testset[,"match"])
  write.csv(cbind(prediction,testset[,"match"]),"prediction_matches_zeros_abs_fine_2.csv")
  tab <- table(pred = prediction, true = testset[,"match"]) 
  tab
}

precision<-function(t){
  p = array(10)
  for(i in 1:9){
    #print(t[(i+2):length(t),(i+2):length(t)])
    #print(i)
    p[i] <-sum(sum(t[1:(i),1:(i)])+sum(t[(i+1):10,(i+1):10]))/sum(t)
    #print(t[1:(i),1:(i)])
    #print(t[(i+1):10,(i+1):10])
  }
  p[10]<-sum(t)/sum(t)
  p
}

precision_raw<-function(t){
  p = array(3)
  for(i in 1:3){
    p[i] <-sum(sum(t[1:(i+1),1:(i+1)])+sum(t[(i+2):5,(i+2):5]))/sum(t)
  }
  p
}