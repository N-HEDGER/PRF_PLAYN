library(ggplot2)
library(ggforce)
library(mixtools)
library(cowplot)
library(kableExtra)
library(stringr)
library(pracma)
library(viridis)


myfile=read.csv('/Volumes/BAHAMUT/OUTPUT/longframe.csv')


myfile$onscreen=rep(0,nrow(myfile))

myfile$onscreen=ifelse(myfile$X>-10 & myfile$X<10 &  myfile$Y>-10 & myfile$Y<10,1,0)


myfile_clean1=myfile[myfile$onscreen==1,]

myfile_clean2=myfile_clean1[myfile_clean1$r2>0.22,]





myfile_clean2=na.omit(myfile_clean2)



myfile_clean2$normdat=rep(0,nrow(myfile_clean2))

idxs=unique(myfile_clean2$idx)
for (i in 1:length(idxs)){
myfile_clean2[myfile_clean2$idx==idxs[i],]$normdat=(myfile_clean2[myfile_clean2$idx==idxs[i],]$pred/max(myfile_clean2[myfile_clean2$idx==idxs[i],]$pred))
  
  
}


VFplot=ggplot()+geom_hline(yintercept=0,colour='white')+
  theme_classic()+theme(panel.background = element_rect(fill='black'))+geom_circle(data=myfile_clean2[myfile_clean2$X.1==25,],mapping=aes(x0=X,y0=Y,r=S/2,fill=data),colour='transparent',alpha=.1)+geom_vline(xintercept=0,colour='white')+xlim(-10,10)+ylim(-10,10)+coord_fixed()+ scale_fill_viridis(option='plasma')+facet_wrap(. ~X.1,nrow=10)




VFplot=ggplot(myfile_clean2,aes(x=X,y=Y))+geom_hline(yintercept=0,colour='white')+
  theme_classic()+theme(panel.background = element_rect(fill='black'))+
  geom_point(aes(fill=normdat,colour=normdat,alpha=normdat))+geom_vline(xintercept=0,colour='white')+xlim(-10,10)+ylim(-10,10)+coord_fixed()+ scale_fill_viridis(option='plasma')+ scale_color_viridis(option='plasma')+facet_wrap(.~X.1,nrow=10)



sl=list.files('/Volumes/BAHAMUT/STIM',full.names = TRUE)


library(cowplot)

stimlist <- vector(mode = "list", length = length(sl))


for (i in 1:length(sl)){
stimlist[[i]]=ggdraw()+draw_image(sl[i],scale=0.8)
}



array=89:103

r1=plot_grid(plotlist=stimlist[array],nrow=1)

r2=ggplot(myfile_clean2[myfile_clean2$X.1 %in% array,],aes(x=X,y=Y))+geom_hline(yintercept=0,colour='white')+
  theme_nothing()+theme(panel.background = element_rect(fill='black'))+
  geom_point(aes(fill=normdat,colour=normdat,alpha=normdat))+geom_vline(xintercept=0,colour='white')+xlim(-10,10)+ylim(-10,10)+coord_fixed()+ scale_fill_viridis(option='plasma')+ scale_color_viridis(option='plasma')+facet_wrap(.~X.1,nrow=1)+ theme(legend.position = "none")+ylab("")


mplot=plot_grid(r1,r2,nrow = 2,axis='tblr',align = 'h')



dumpdir='/Volumes/BAHAMUT/STIM/FIGS/'
ggsave(mplot, file=paste0(dumpdir,"Pass4.bmp"), device="bmp",dpi=300,width=12,height=2,units="in")





bplot=ggplot(myfile_clean2,aes(x=X,y=Y))+geom_hline(yintercept=0,colour='white')+
  theme_nothing()+theme(panel.background = element_rect(fill='black'))+
  geom_point(aes(fill=normdat,colour=normdat,alpha=normdat))+geom_vline(xintercept=0,colour='white')+xlim(-10,10)+ylim(-10,10)+coord_fixed()+ scale_fill_viridis(option='plasma')+ scale_color_viridis(option='plasma')+facet_wrap(.~X.1,nrow=10)+ theme(legend.position = "none")+ylab("")



VFplot=ggplot()+geom_hline(yintercept=0,colour='white')+
  theme_classic()+theme(panel.background = element_rect(fill='black'))+geom_circle(data=myfile_clean2[myfile_clean2$X.1 %in% 36:48,],mapping=aes(x0=X,y0=Y,r=S/2,fill=normdat,colour=normdat,alpha=normdat))+geom_vline(xintercept=0,colour='white')+xlim(-10,10)+ylim(-10,10)+coord_fixed()+ scale_fill_viridis(option='plasma')+ scale_colour_viridis(option='plasma')+facet_wrap(. ~X.1,nrow=10)


which.max(myfile_clean2$r2)


