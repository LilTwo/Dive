import tkinter
import PIL.Image, PIL.ImageTk
from Image import Image


class GUI:
    def __init__(self,img_dir):
        self.c_img = Image(img_dir)
        self.window = tkinter.Tk()
        height,width,chan = self.c_img.shape
        self.canvas = tkinter.Canvas(self.window, width = width, height = height)
        self.contrast = tkinter.Button(self.window,text="contrast",command=self.on_contrast)

        self.rscale = [tkinter.Scale(self.window,orient=tkinter.HORIZONTAL,command=self.on_rscale,from_=0,to=254)
            ,tkinter.Scale(self.window,orient=tkinter.HORIZONTAL,command=self.on_rscale,from_=1,to=255)]
        self.gscale = [tkinter.Scale(self.window,orient=tkinter.HORIZONTAL,command=self.on_gscale,from_=0,to=254)
            ,tkinter.Scale(self.window,orient=tkinter.HORIZONTAL,command=self.on_gscale,from_=1,to=255)]
        self.bscale = [tkinter.Scale(self.window,orient=tkinter.HORIZONTAL,command=self.on_bscale,from_=0,to=254)
            ,tkinter.Scale(self.window,orient=tkinter.HORIZONTAL,command=self.on_bscale,from_=1,to=255)]
        self.tint = tkinter.Scale(self.window,orient=tkinter.HORIZONTAL,command=self.on_tint,from_=-50,to=50)
        self.temp = tkinter.Scale(self.window,orient=tkinter.HORIZONTAL,command=self.on_temp,from_=-50,to=50)

        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.c_img.to_uint8()))
        self.m = self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def start(self):
        self.rscale[0].grid(row=1,column=0)
        self.rscale[1].grid(row=2,column=0)
        self.rscale[1].set(255)
        self.gscale[0].grid(row=1,column=1)
        self.gscale[1].grid(row=2,column=1)
        self.gscale[1].set(255)
        self.bscale[0].grid(row=1,column=2)
        self.bscale[1].grid(row=2,column=2)
        self.bscale[1].set(255)
        self.tint.grid(row=3,column=1,sticky=tkinter.E)
        self.temp.grid(row=3,column=1,sticky=tkinter.W)
        self.contrast.grid(row=4,column=1)
        self.canvas.grid(row=0,column=0,columnspan=3)
        self.window.mainloop()

    def on_contrast(self):
        self.c_img.adjust_contrast()
        self.reset_scale()
        self.update()

    def update(self):
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.c_img.to_uint8()))
        self.canvas.itemconfig(self.m,image=self.photo)

    def reset_scale(self):
        self.rscale[0].set(0)
        self.rscale[1].set(255)
        self.gscale[0].set(0)
        self.gscale[1].set(255)
        self.bscale[0].set(0)
        self.bscale[1].set(255)

    def on_rscale(self,value):
        value = int(value)
        is_min = value == self.rscale[0].get()
        min = self.rscale[0].get()
        max = self.rscale[1].get()
        if min >= max:
            if is_min:
                self.rscale[0].set(max-1)
            else:
                self.rscale[1].set(min+1)
        self.c_img.scale(min,max,2)
        self.update()

    def on_gscale(self,value):
        value = int(value)
        is_min = value == self.gscale[0].get()
        min = self.gscale[0].get()
        max = self.gscale[1].get()
        if min >= max:
            if is_min:
                self.gscale[0].set(max-1)
            else:
                self.gscale[1].set(min+1)
        self.c_img.scale(min,max,1)
        self.update()

    def on_bscale(self,value):
        value = int(value)
        is_min = value == self.bscale[0].get()
        min = self.bscale[0].get()
        max = self.bscale[1].get()
        if min >= max:
            if is_min:
                self.bscale[0].set(max-1)
            else:
                self.bscale[1].set(min+1)
        self.c_img.scale(min,max,0)
        self.update()

    def on_tint(self,value):
        value = int(value)
        self.c_img.adjust_tint(value)
        self.update()

    def on_temp(self,value):
        value = int(value)
        self.c_img.adjust_temp(value)
        self.update()

g = GUI("diving.jpg")
g.start()


