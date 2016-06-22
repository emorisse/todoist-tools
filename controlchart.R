group_size = 7
init_period = 4

tasks <- read.csv("data.csv",header=FALSE)
names(tasks) <- c("tasks")

control.points <- 'n,A2,D4,D3
2,1.88,3.267
3,1.023,2.575
4,0.729,2.282
5,0.577,2.115
6,0.483,2.004
7,0.419,1.924,0.076
8,0.373,1.864,0.136
9,0.337,1.816,0.184
10,0.308,1.777,0.223'

controls <- read.csv(text=control.points, header=TRUE)

# add groups
groups = ceiling(nrow(tasks)/group_size)
tasks <- data.frame(tasks=tasks,group=rep(1:groups,each=group_size,length.out=nrow(tasks)))

# ranges
rbar <- aggregate(tasks~group,data=tasks, function(x) max(x)-min(x) )
rbarbar <- mean(rbar[rbar$group <= init_period,]$tasks)

# add control lines
xbarbar <- task.mean <- mean(tasks[tasks$group <= init_period,]$tasks)
task.lcl <- xbarbar - controls[controls$n == group_size,]$A2 * rbarbar
task.ucl <- xbarbar + controls[controls$n == group_size,]$A2 * rbarbar

# add daily errors
tasks <- cbind(tasks, daily_errors = tasks$tasks>task.ucl|tasks$tasks<task.lcl)

# add weekly errors
task.errors <- sum(apply(tasks[tasks$group <= init_period,],1,function(x) x[1] < task.lcl | x[1] > task.ucl))/init_period
weekly.errors <- aggregate(tasks~group,data=tasks, function(x) sum(x > task.ucl, x < task.lcl))[,c("group","tasks")]
tasks <- cbind(tasks,weekly_errors = tasks$group %in% weekly.errors[weekly.errors$tasks > task.errors,]$group)

# group means
group.mean <- aggregate(tasks~group,data=tasks, function(x) mean(x))

library(ggplot2)
library(gridExtra)

xchart <- 
ggplot(tasks, aes(x=group)) + geom_vline(xintercept=init_period, color="gray", linetype="dotted") + geom_point(aes(y=tasks, color=daily_errors, shape=weekly_errors)) + scale_color_manual(values=c("gray","red")) + geom_line(aes(y=task.mean), linetype="dashed", color="gray") + geom_line(aes(y=task.lcl), color="gray") + geom_line(aes(y=task.ucl), color="gray") + geom_line(data=group.mean, aes(y=tasks,x=group), color="blue") + theme_minimal() + xlab("week") + ylab("tasks completed") 

# range chart
range.ucl <- rbarbar * controls[controls$n == group_size,]$D4
range.lcl <- rbarbar * controls[controls$n == group_size,]$D3

rbar <- cbind(rbar,range_errors=aggregate(tasks~group,data=rbar, function(x) x > range.ucl | x < range.lcl)[,c("group","tasks")][,"tasks"])

rchart <-
ggplot(rbar, aes(x=group,y=tasks)) + geom_vline(xintercept=init_period, color="gray", linetype="dotted") + geom_line(aes(y=rbarbar), color="gray", linetype="dashed") + geom_line(aes(y=range.ucl), color="gray") + geom_line(aes(y=range.lcl), color="gray") + geom_line(color="blue") + geom_point(aes(color=range_errors)) + scale_color_manual(values=c("gray","red"))+ theme_minimal() + xlab("week") + ylab("range of tasks completed") 


# error chart (p-chart)
pbar.mean <- task.errors/group_size
pbar.lcl <- pbar.mean - 3 * sqrt((1-pbar.mean) * pbar.mean/group_size)
pbar.ucl <- pbar.mean + 3 * sqrt((1-pbar.mean) * pbar.mean/group_size) 

weekly.errors <- cbind(weekly.errors,portion_errors=aggregate(tasks~group,data=weekly.errors, function(x) x/group_size > pbar.ucl | x/group_size < pbar.lcl)[,c("group","tasks")][,"tasks"])

pbar.lcl <- pbar.mean - 3 * sqrt((1-pbar.mean) * pbar.mean/group_size)
pbar.ucl <- pbar.mean + 3 * sqrt((1-pbar.mean) * pbar.mean/group_size) 
pchart <-
ggplot(weekly.errors, aes(x=group, y=tasks/group_size)) + geom_vline(xintercept=init_period, color="gray", linetype="dotted") + geom_line(aes(y=pbar.mean), color="gray", linetype="dashed") + geom_line(aes(y=pbar.ucl), color="gray") + geom_line(aes(y=pbar.lcl), color="gray") + geom_line(color="blue") + geom_point(aes(color=portion_errors)) + scale_color_manual(values=c("gray","red")) + theme_minimal() + xlab("week") + ylab("portion of errors") + ylim(0,NA)


grid.arrange(xchart,rchart,pchart,ncol=1)
