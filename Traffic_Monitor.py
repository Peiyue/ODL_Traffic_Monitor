from Tkinter import *
import tkFont
import time
import random
import thread
from get_topology import get_topology
from rate_monitor_spg import rate_monitor_spg
from get_all_ports_statics import get_all_ports_statics
from check_ports_rate_spg import check_ports_rate_spg
from check_topo_spg import check_topo_spg
from PIL import Image,ImageTk,ImageDraw
import ImageGrab
from time import ctime,strftime

class switch(object):
        def __init__(self,name,cv,switch_image,x=100,y=100):
                self.name=name
                self.x=x
                self.y=y
                self.links=[]
                self.pairs=[]
                self.cv=cv
                self.switch_image=switch_image
                self.tag=get_switch_name(name)
                

                
                
        def draw(self):
                self.image = self.cv.create_image(self.x,self.y,anchor=NE,image=self.switch_image,tags=self.name)
                self.cv.tag_bind(self.name,'<B1-Motion>',self.move)
                self.text= self.cv.create_text((self.x-80,self.y+70),text =self.tag,anchor = W,tags=self.name)
                
                
                
        def move(self,event):
                if event.x>800:
                        event.x=800
                if event.x<88:
                        event.x=88
                if event.y>420:
                        event.y=420
                if event.y<0:
                        event.y=0
                        
                self.cv.coords(self.image,(event.x,event.y))
                self.cv.coords(self.text,(event.x-80,event.y+70))
                self.x=event.x
                self.y=event.y
                for index in range(len(self.links)):
                        self.links[index].move(self,self.pairs[index],self.cv)
                        
                        
        def add_link(self,s2,link):
                self.links.append(link)
                self.pairs.append(s2)

class link(object):
        def __init__(self,s1,s2,cv,port_1,port_2):
                self.name=s1.name+port_1+s2.name+port_2
                self.cv=cv
                self.margin=44
                self.s1=s1
                self.s2=s2
                
                self.line=cv.create_line((s1.x-self.margin,s1.y+self.margin,s2.x-self.margin,s2.y+self.margin),width=3,tags=self.name)
                cv.itemconfig(self.line,fill= '#ffa500')

                self.head=s1.name
                self.head_port=port_1

                self.tail=s2.name
                self.tail_port=port_2
                
                print 'add link ',self.head,'port ',self.head_port,' ',self.tail,' ','port ',self.tail_port
        def move(self,s_move,s_change,cv):
                cv.coords(self.line,(s_change.x-self.margin,s_change.y+self.margin,s_move.x-self.margin,s_move.y+self.margin))

        def broken(self):
                self.cv.itemconfig(self.line,fill= '#000000')
                
        def recovery(self):
                self.cv.itemconfig(self.line,fill= '#20B2AA')
        def colorrate(self,rate):
                
                if rate>2000:
                        self.cv.itemconfig(self.line,fill= '#cd0000')#red
                        #print 'red'
                elif rate>1000:
                        self.cv.itemconfig(self.line,fill= '#ee7600')#yellow
                        #print 'yellow'
                elif rate>1:
                        self.cv.itemconfig(self.line,fill= '#7fff00')#green
                        #print 'green'
                else:
                        self.cv.itemconfig(self.line,fill= '#CCCCCC')#gray
                        #print 'gray'
                
def get_switch_name(name):
        lenn=len(name)
        for index in range(lenn):
            if name[index]!='0':
                if name[index]!=':':
                        break
        return 'Switch-'+name[index:lenn]


def link_helper(s1,s2,cv,port_1='none',port_2='none'):
        new_link=link(s1,s2,cv,port_1,port_2)
        s1.add_link(s2,new_link)
        s2.add_link(s1,new_link)
        return new_link

def switch_finder(switches,switch_id):
        for switch in switches:
                if switch.name==switch_id:
                        
                        return switch
                        break
        
def check_new_switch(switches,switch_id):
        flag=0
        for switch in switches:
                
                if switch_id==switch.name:
                        return 1
                        break
        if flag==0:
                return 0

def check_new_link(links,switch_id_1,switch_id_2):
        flag=0
        for link in links:
                
                if switch_id_1==link.head:
                        if switch_id_2==link.tail:
                                return 1
                                break
        if flag==0:
                return 0

class spg_topo(object):
#main frame
        def __init__(self,root):
                
                self.font1 = tkFont.Font(family = 'Arial',size = 10,weight =tkFont.BOLD)
                self.root =root
                self.frame_traffic = LabelFrame(self.root,text="Traffic Visualization",font=self.font1)
                self.frame_traffic.pack()

                self.refresh_index=1
                self.ini=0

                #self.switch_image= PhotoImage(file = "switch.gif")


                self.switch_jpg=Image.open('switch.bmp')
                self.switch_image=ImageTk.PhotoImage(self.switch_jpg)                
                
                self.height=500
                self.width=800
                self.cv = Canvas(self.frame_traffic,bg = 'white',height=self.height,width=self.width)
                                
                self.switches=[]
                self.links=[]

                

                self.logo=Image.open('logo.jpg')
                self.imagelogo=ImageTk.PhotoImage(self.logo)
                self.cv.create_image(650,50,image=self.imagelogo)
                

                #add switch
                '''
                                             
                self.data=get_topology()
                self.num_of_links=len(self.data['edgeProperties'])
                for index in range(self.num_of_links):
                        switch_id_1=self.data['edgeProperties'][index]['edge']['headNodeConnector']['node']['id']

                        if check_new_switch(self.switches,switch_id_1)==0:
                                new_switch_1=switch(switch_id_1,self.cv,self.switch_image,random.randint(30,370),random.randint(30,370))
                                self.switches.append(new_switch_1)

                        switch_id_2=self.data['edgeProperties'][index]['edge']['tailNodeConnector']['node']['id']
                        if check_new_switch(self.switches,switch_id_2)==0:
                                new_switch_2=switch(switch_id_2,self.cv,self.switch_image,random.randint(30,370),random.randint(30,370))
                                self.switches.append(new_switch_2)

                        if check_new_link(self.links,switch_id_1,switch_id_2)==0:
                                print 'creat link'
                                port_1=self.data['edgeProperties'][index]['edge']['headNodeConnector']['id']
                                port_2=self.data['edgeProperties'][index]['edge']['tailNodeConnector']['id']
                                new_link=link_helper(switch_finder(self.switches,switch_id_1),switch_finder(self.switches,switch_id_2),self.cv,port_1,port_2)
                                self.links.append(new_link)
                for switch_t in self.switches:
                        switch_t.draw()
                self.time= self.cv.create_text((550,480),text ='Last updated: '+ctime(),anchor = W,tags='time')
                '''
                                                  
                self.cv.pack()

        def auto_triger(self):
                if self.refresh_index==1:
                        time.sleep(1)
                        self.refresh([])
                else:
                        self.refresh_index=1
                                
        def find_link(self,target):
                flag=0
                for link in self.links:
                        if link.name==target:
                                flag=1
                                return link                                
                                break
                if flag==0:
                        return 'none'
        def restart(self):

                for item in self.switches:

                        self.cv.delete(item.name)
                for item in self.links:
                        self.cv.delete(item.name)

                self.switches=[]
                self.links=[]

                self.data_old=get_all_ports_statics()
                

                #add switch
                                             
                self.data=get_topology()
                self.num_of_links=len(self.data['edgeProperties'])
                for index in range(self.num_of_links):
                        switch_id_1=self.data['edgeProperties'][index]['edge']['headNodeConnector']['node']['id']

                        if check_new_switch(self.switches,switch_id_1)==0:
                                new_switch_1=switch(switch_id_1,self.cv,self.switch_image,random.randint(30,370),random.randint(30,370))
                                self.switches.append(new_switch_1)

                        switch_id_2=self.data['edgeProperties'][index]['edge']['tailNodeConnector']['node']['id']
                        if check_new_switch(self.switches,switch_id_2)==0:
                                new_switch_2=switch(switch_id_2,self.cv,self.switch_image,random.randint(30,370),random.randint(30,370))
                                self.switches.append(new_switch_2)

                        if check_new_link(self.links,switch_id_1,switch_id_2)==0:
                                print 'creat link'
                                port_1=self.data['edgeProperties'][index]['edge']['headNodeConnector']['id']
                                port_2=self.data['edgeProperties'][index]['edge']['tailNodeConnector']['id']
                                new_link=link_helper(switch_finder(self.switches,switch_id_1),switch_finder(self.switches,switch_id_2),self.cv,port_1,port_2)
                                self.links.append(new_link)
                for switch_t in self.switches:
                        switch_t.draw()
                self.cv.delete('time')
                self.time= self.cv.create_text((550,480),text ='Last updated: '+ctime(),anchor = W,tags='time')
                self.ini=1

        def snapshoot(self):
                white=(255,255,255)
                x0 = self.cv.winfo_rootx()
                y0 = self.cv.winfo_rooty()
                x1 = x0 + self.cv.winfo_width()
                y1 = y0 + self.cv.winfo_height()
                im = ImageGrab.grab((x0, y0, x1, y1))
                draw = ImageDraw.Draw(im)
                draw.text((50,480),"flowGlance|A traffic monitor for Opendaylight",(0,0,0))

                
                #self.snapshoot = Image.new("RGB", (800, 500), white)
                #self.snapshootd=ImageDraw.Draw(self.snapshoot)
                times=strftime('%Y-%m-%d_%H_%M_%S')
                self.filename='snapshot\\flowGlance'+times+'.bmp'
                im.save(self.filename)                
                
        
        def refresh(self,event):
                        print 'refresh started'
                        if self.ini==0:
                                self.data_old=get_all_ports_statics()
                                self.restart()
                                self.ini=1
                        
                        self.time_interval=1
                        self.mode='all'
                        #time.sleep(self.time_interval)
                        self.data_new=get_all_ports_statics()
                        self.result_switch={'Added Port':[],'Deleted Port':[]}
                        self.result_rate=[]
                        #Refresh data rate
                        self.rates=check_ports_rate_spg(self.data_old,self.data_new,self.result_switch,self.time_interval,self.mode,self.result_rate)
                        self.time= self.cv.create_text((550,480),text ='Last updated: '+ctime(),anchor = W,tags='time')


                        for link in self.links:
                                head_rate=self.get_rate(self.rates,link.head,link.head_port)
                                tail_rate=self.get_rate(self.rates,link.head,link.head_port)
                                if head_rate['TX_rate']!='none':
                                        if tail_rate['RX_rate']!='none':
                                                link.colorrate(min(head_rate['TX_rate'],tail_rate['RX_rate']))
                        #Refresh link
                        
                        self.result=check_topo_spg(self.data,self.data,get_topology())
                        for link in self.result['Remove link']:
                                result_t=self.find_link(link)
                                if result_t!='none':
                                        result_t.broken()

                        for link in self.result['Add link']:
                                result_t=self.find_link(link)
                                if result_t!='none':
                                        result_t.recovery()

                        self.data_old=self.data_new
                        print 'relodad'
                        self.cv.delete('time')
                        self.time= self.cv.create_text((550,480),text ='Last updated: '+ctime(),anchor = W,tags='time')

                        
                        thread.start_new_thread(self.auto_triger,())
                    
        def get_rate(self,rates,switch_id,port_id):
                flag=0
                for rate in rates:
                        if switch_id==rate['switch_id']:
                                if port_id==rate['port_id']:
                                        flag=1
                                        return {'RX_rate':rate['RX_rate'],'TX_rate':rate['TX_rate']}
                                        break
                if flag==0:
                        return {'RX_rate':'none','TX_rate':'none'}
