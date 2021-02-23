import tkinter as tk
import tkinter.messagebox as tkm
import tkinter.ttk as ttk
import tkinter.filedialog as tkf
from PIL import ImageTk,Image
import polygarm as pg
import numpy as np

class Compare(tk.Frame):
    def push(self):
        print("push")
        lam=self.lam_entry.get()
        try :
            lam=float(lam)
        except TypeError:
            tkm.showwarning(title="Внимание",message="Ожидается числовое значение параметра")
            return "Type"

        dim=self.dim_entry.get()
        if dim.isdigit():
            dim=int(dim)
        else:
            tkm.showwarning(title="Внимание",message="Ожидается целочисленное значение степени")
            return "Type"

        ss=self.ss_entry.get()
        if ss.isdigit():
            ss=int(ss)
        else:
            tkm.showwarning(title="Внимание",message="Ожидается целочисленное значение размера окна")
            return "Type"

        file_name = tkf.askopenfilename(
                        filetypes=(("image files", "*.bmp;*.png;*.jpg;*.jpeg"),
                       ("All files", "*.*")))

        if file_name =="":
            return

        img=Image.open(file_name)
        img.load()
        img=img.convert("L")
        img=self.prepare_image(img)
        self.img_before=ImageTk.PhotoImage(img)
        self.lab_bfr["image"]=self.img_before
        res=pg.Range(-pg.Rev_Lap(np.array(img,dtype=np.uint8),dim,lam))
        print("min, max",np.min(res),np.max(res))
        self.img_res=Image.fromarray(np.uint8(res),"L")
        self.img_res.save("test.png")
        self.img_res=ImageTk.PhotoImage(self.img_res)
        pg.save_show(res,"test2")



        self.lab_aft["image"]=self.img_res




    def __init__(self,root):
        self.parent=root
        self.create()
    def create(self):
        self.settings_frame=tk.Frame(self.parent)
        self.settings_frame.pack(fill="x")
        #settings_frame(
        self.lam_frame=tk.LabelFrame(self.settings_frame,text="Коэф лапласа")
        self.lam_frame.pack(side="left")

        self.dim_frame=tk.LabelFrame(self.settings_frame,text="Степень")
        self.dim_frame.pack(side="left")

        self.ss_frame=tk.LabelFrame(self.settings_frame,text="Размер окна(0-fullscreen)")
        self.ss_frame.pack(side="left")

        self.dim_entry=tk.Entry(self.dim_frame,width=5)
        self.dim_entry.pack(side="left")
        self.ss_entry=tk.Entry(self.ss_frame,width=5)
        self.ss_entry.pack(side="left")

        self.lam_entry=tk.Entry(self.lam_frame,width=5)
        self.lam_entry.pack(side="left")

        self.but=tk.Button(self.settings_frame,text="OK",command=self.push)
        self.but.pack(side="left")

        self.lam_entry.insert(0,"1.01")
        self.ss_entry.insert(0,"0")
        self.dim_entry.insert(0,"1")


        #settings_frame)

        self.img_frame=tk.Frame(self.parent)
        self.img_frame.pack(fill="both")
        #img_frame(
        self.lab_bfr = tk.Label(self.img_frame)
        self.lab_bfr.pack(side="left",padx=5)
        self.lab_aft = tk.Label(self.img_frame)
        self.lab_aft.pack(side="left",padx=5)
        #img_frame)


    def centerWindow(self):
        w = 290
        h = 150

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def prepare_image(self,img):
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        width=img.width
        height=img.height
        print("размеры получены",sw,sh,width,height)
        if width>0.4*sw or height>0.8*sh:
            if width>0.4*sw:
                kf=0.4*sw/width
                width=width*kf
                height=height*kf
            if height>0.8*sh:
                kf=0.4*sh/hight
                width=width*kf
                height=height*kf
            return img.resize((round(width),round(height)))
        else:
            return img












root=tk.Tk()
app=Compare(root)
root.mainloop()
