from Traffic_Monitor import *
from Tkinter import *
import tkFont
from PIL import Image,ImageTk,ImageDraw


class TM_Window(object):

        def start_button(self):
                self.TM.refresh([])
        def stop_button(self):
                self.TM.refresh_index=0
        def delete_button(self):
                self.TM.restart()
        def snapshoot_button(self):
                self.TM.snapshoot()
        
        def __init__(self):
                
                self.Top=Tk(className='FlowGlance-Opendaylight Traffic Monitor')
                self.Top.resizable(False, False)
                #logo
                self.Top.iconbitmap('logo_ico.ico')
                #font
                font1 = tkFont.Font(family = 'Arial',size = 10,weight =tkFont.BOLD)
                font2 = tkFont.Font(family = 'Arial',size = 10)
                #Button Frame
                self.frame_button=Frame(self.Top)
                self.frame_button.pack(ipadx = 10,ipady = 20)
                #add button

                #start button
                self.button = Button(self.frame_button,width=25,padx=5,pady=2,font=font1,bg = 'white')

                self.start_jpg=Image.open('start.png')
                self.start_image=ImageTk.PhotoImage(self.start_jpg)
                self.button.config(image=self.start_image,width='125',compound = 'left')

                self.button['text'] = 'Start'
                self.button['bd']=6
                self.button['command'] =self.start_button
                
                self.button.pack(side=LEFT,padx = 10,pady = 20)
                #stop button
                self.button = Button(self.frame_button,width=15,padx=5,pady=2,font=font1,bg = 'white')

                self.stop_jpg=Image.open('stop.png')
                self.stop_image=ImageTk.PhotoImage(self.stop_jpg)
                self.button.config(image=self.stop_image,width='125',compound = 'left')

                self.button['text'] = 'Stop'
                self.button['bd']=6
                self.button['command'] =self.stop_button
                self.button.pack(side=LEFT,padx = 10,pady = 20)
                #refresh
                self.button = Button(self.frame_button,width=15,padx=5,pady=2,font=font1,bg = 'white')

                self.refresh_jpg=Image.open('refresh.png')
                self.refresh_image=ImageTk.PhotoImage(self.refresh_jpg)
                self.button.config(image=self.refresh_image,width='150',compound = 'left')

                self.button['text'] = 'Refresh'
                self.button['bd']=6
                self.button['command'] =self.delete_button
                self.button.pack(side=LEFT,padx = 10,pady = 15)
#snp
                self.button = Button(self.frame_button,width=15,padx=5,pady=2,font=font1,bg = 'white')
                self.snp_jpg=Image.open('snp.png')
                self.snp_image=ImageTk.PhotoImage(self.snp_jpg)
                self.button.config(image=self.snp_image,width='125',compound = 'left')


                self.button['text'] = 'Snapshot'
                self.button['bd']=6
                self.button['command'] =self.snapshoot_button
                self.button.pack(side=LEFT,padx = 10,pady = 15)
                #Topo
                self.TM=spg_topo(self.Top)
                self.Top.mainloop()
