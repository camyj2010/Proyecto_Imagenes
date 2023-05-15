from tkinter.font import Font
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from Segmentation_Algorithm.thresholdind import thres
from Segmentation_Algorithm.kMeans import k_means
from Segmentation_Algorithm.region_growing import RegionGrowing
from Border_Algorithm.Border import border_magnitude
import customtkinter


class Segmentation():
    def __init__(self,window,image_data, ax_x,ax_y,ax_z, bigfont2,canvas, ax, canvas_widget, axis,listAxis):
        self.window=window
        self.data=image_data
        self.ax_x=ax_x
        self.ax_y=ax_y
        # print(self.ax_y)
        self.ax_z=ax_z
        self.bigFont2=bigfont2
        self.thresholdind_frame = None
        self.k_means_frame=None
        self.regionGrowing_frame=None
        self.canvas=canvas
        self.ax=ax
        self.canvas_widget=canvas_widget
        self.Axis=axis
        self.ax_list=listAxis
        self.data_segmented=self.data
        

        #Menu para segmentar

        self.segmentation_frame = tk.Frame(self.window, bg="#000000")
        l_ax=tk.Label( self.segmentation_frame,text= "Axis",fg="white",bg = "#000000", font=self.bigFont2)
        ax_menu = tk.OptionMenu(self.segmentation_frame, self.Axis, *self.ax_list, command=self.display_selected)
        ax_menu.place(x=50, y=100)
        l_ax.place(x=0, y=100)
        options_list = ["Thresholdind", "K-means","Region Growing"]
        self.segmentation_method = tk.StringVar(self.window)
        self.segmentation_method.set("Select an Option")
        l_algorimt = tk.Label(self.segmentation_frame, text="Segmentation", fg="white", bg="#000000", font=self.bigFont2)
        question_menu = tk.OptionMenu(self.segmentation_frame, self.segmentation_method, *options_list, command=self.select_algorithm)
        question_menu.place(x=100, y=180)
        l_algorimt.place(x=0, y=180)
       
        # Agregar el marco al window
        self.segmentation_frame.place(x=690, y=70, relwidth=1, relheight=1)
        # print(self.ax_y)
          
    
    # Define the select_algorithm function
    def select_algorithm(self, *args):
        
        if self.segmentation_method.get() == "Thresholdind":
            if self.k_means_frame is not None:
                widgets = [self.k_means_frame_entryK, self.k_means_frame_l_k,self.button_Bordes,self.button]
                for widget in widgets:
                    widget.destroy()
                self.k_means_frame.destroy()
                self.k_means_frame = None

            if self.regionGrowing_frame is not None:
                widgets = [self.regionGrowing_frame_entryTolerance, self.regionGrowing_frame_l_tol,self.button_Bordes,self.button]
                for widget in widgets:
                    widget.destroy()
                self.regionGrowing_frame.destroy()
                self.regionGrowing_frame= None

            if self.thresholdind_frame is None:
                self.thresholdind_frame = tk.Frame(self.window, bg="#000000")
                self.thresholdind_frame_img_boton2 = tk.PhotoImage(file="play.png")
                self.thresholdind_frame_l_tao = tk.Label(self.thresholdind_frame, text="Tao", fg="white", bg="#000000", font=self.bigFont2)
                self.thresholdind_frame_entryTao = tk.Entry(self.thresholdind_frame,justify="center", fg="white", bg="#000000")
                self.thresholdind_frame_entryTao.insert(0, "110")
                self.thresholdind_frame_l_tol = tk.Label(self.thresholdind_frame, text="Tolerance", fg="white", bg="#000000", font=self.bigFont2)
                self.thresholdind_frame_entryTolerance = tk.Entry(self.thresholdind_frame,justify="center", fg="white", bg="#000000")
                self.thresholdind_frame_entryTolerance.insert(0, "1")
                # self.thresholdind_frame_btn = tk.Button(self.thresholdind_frame, image=self.thresholdind_frame_img_boton2, bg="#000000", borderwidth=0, command= lambda: self.segm("Thresholdind"))
                self.button_Bordes = customtkinter.CTkButton(self.thresholdind_frame, text="Bordes",font=("PT Bold Heading",12), width=200,height=40, command= lambda: self.segm_border("Thresholdind") )
                self.button = customtkinter.CTkButton(self.thresholdind_frame, text="Segmentate",font=("PT Bold Heading",12), width=200,height=40, command= lambda: self.segm("Thresholdind"))
                
                self.thresholdind_frame.pack()
                self.thresholdind_frame.place(x=690, y=320, width=300, height=400) 
                # self.thresholdind_frame_btn.place(x=220, y= 20)
                self.thresholdind_frame_entryTolerance.place(x=90, y=0, width=100, height=25)
                self.thresholdind_frame_entryTao.place(x=90, y=40, width=100, height=25)
                self.thresholdind_frame_l_tao.place(x=10, y=40)
                self.thresholdind_frame_l_tol.place(x=10, y=0)
                self.button_Bordes.place(x=20, y=150)
                self.button.place(x=20, y=100)
                
            else:
                self.thresholdind_frame.lift()
        elif self.segmentation_method.get() == "K-means":

            if self.thresholdind_frame is not None:
                widgets = [self.thresholdind_frame_entryTao, self.thresholdind_frame_entryTolerance, self.button_Bordes,self.thresholdind_frame_l_tao, self.thresholdind_frame_l_tol, self.button]
                for widget in widgets:
                    widget.destroy()
                self.thresholdind_frame.destroy()
                self.thresholdind_frame = None

            if self.regionGrowing_frame is not None:
                widgets = [  self.regionGrowing_frame_entryTolerance, self.regionGrowing_frame_l_tol,self.button_Bordes, self.button]
                for widget in widgets:
                    widget.destroy()
                self.regionGrowing_frame.destroy()
                self.regionGrowing_frame= None

            if self.k_means_frame is None:
                self.k_means_frame = tk.Frame(self.window, bg="#000000")
                self.k_means_frame_img_boton2 = tk.PhotoImage(file="play.png")
                self.k_means_frame_l_k = tk.Label(self.k_means_frame, text="K", fg="white", bg="#000000", font=self.bigFont2)
                self.k_means_frame_entryK = tk.Entry(self.k_means_frame,justify="center", fg="white", bg="#000000")
                self.k_means_frame_entryK.insert(0, "3")
                self.button_Bordes = customtkinter.CTkButton(self.k_means_frame, text="Bordes",font=("PT Bold Heading",12), width=200,height=40, command= lambda: self.segm_border("K-means"))
                self.button = customtkinter.CTkButton(self.k_means_frame, text="Segmentate",font=("PT Bold Heading",12), width=200,height=40, command= lambda: self.segm("K-means"))
                
                
                # self.k_means_frame_btn = tk.Button(self.k_means_frame, image=self.k_means_frame_img_boton2, bg="#000000", borderwidth=0, command= lambda: self.segm("K-means"))
                self.k_means_frame.pack()
                self.k_means_frame.place(x=690,y=320, width=300, height=400) 
                # self.k_means_frame_btn.place(x=220, y= 20)
                
                self.k_means_frame_entryK.place(x=90, y=40, width=100, height=25)
                self.k_means_frame_l_k.place(x=10, y=40)
                self.button_Bordes.place(x=20, y=150)
                self.button.place(x=20, y=100)
                
            else:
                self.k_means_frame.lift()
        elif self.segmentation_method.get()=="Region Growing":
            if self.k_means_frame is not None:
                widgets = [self.k_means_frame_entryK, self.k_means_frame_l_k,self.button_Bordes,self.button]
                for widget in widgets:
                    widget.destroy()
                self.k_means_frame.destroy()
                self.k_means_frame = None
            if self.thresholdind_frame is not None:
                widgets = [self.thresholdind_frame_entryTao, self.thresholdind_frame_entryTolerance, self.thresholdind_frame_l_tao, self.thresholdind_frame_l_tol,self.button_Bordes, self.button]
                for widget in widgets:
                    widget.destroy()
                self.thresholdind_frame.destroy()
                self.thresholdind_frame = None
            if self.regionGrowing_frame is None:
                self.regionGrowing_frame = tk.Frame(self.window, bg="#000000")
                # self.regionGrowing_frame_img_boton2 = tk.PhotoImage(file="play.png")
                
                self.regionGrowing_frame_l_tol = tk.Label(self.regionGrowing_frame, text="Tolerance", fg="white", bg="#000000", font=self.bigFont2)
                self.regionGrowing_frame_entryTolerance = tk.Entry(self.regionGrowing_frame,justify="center", fg="white", bg="#000000")
                self.regionGrowing_frame_entryTolerance.insert(0, "1")
                # self.regionGrowing_frame_btn = tk.Button(self.regionGrowing_frame, image=self.regionGrowing_frame_img_boton2, bg="#000000", borderwidth=0, command= lambda: self.segm("Region Growing"))
                self.button_Bordes = customtkinter.CTkButton(self.regionGrowing_frame, text="Bordes",font=("PT Bold Heading",12), width=200,height=40, command= lambda: self.segm_border("Region Growing"))
                self.button = customtkinter.CTkButton(self.regionGrowing_frame, text="Segmentate",font=("PT Bold Heading",12), width=200,height=40, command= lambda: self.segm("Region Growing"))
                self.regionGrowing_frame.pack()
                self.regionGrowing_frame.place(x=690, y=320, width=300, height=400) 
                # self.regionGrowing_frame_btn.place(x=220, y= 20)
                self.regionGrowing_frame_entryTolerance.place(x=90, y=0, width=100, height=25)
                
                self.regionGrowing_frame_l_tol.place(x=10, y=0)
                self.button.place(x=20, y=100)
                self.button_Bordes.place(x=20, y=150)
            else:
                self.regionGrowing_frame.lift()     
             
                
    def segm(self, type):
         if type=="Thresholdind":
            
            self.data_segmented=thres(self.data,float(self.thresholdind_frame_entryTolerance.get()), float(self.thresholdind_frame_entryTao.get()))
            self.plotAx()
            
         if type=="K-means":
            
            self.data_segmented=k_means(self.data, int(self.k_means_frame_entryK.get()))
        
            self.plotAx()
         if type=="Region Growing":
            self.data_segmented=RegionGrowing(self.data,int(self.regionGrowing_frame_entryTolerance.get()))
        
            self.plotAx() 
    def segm_border(self, type):
         if type=="Thresholdind":
            
            self.data_segmented=border_magnitude(self.data)
            
            self.plotAx()
            
         if type=="K-means":
            self.data_segmented=border_magnitude(self.data)
        
            self.plotAx()
         if type=="Region Growing":
            self.data_segmented=border_magnitude(self.data)
        
            self.plotAx() 
    
    def display_selected(self, *args):
        
            if(self.Axis.get()=="x"):
                
                max=self.data_segmented.shape[0]-1
            elif(self.Axis.get()=="y"):
                max=self.data_segmented.shape[1]-1
                
            elif(self.Axis.get()=="z"):
                max=self.data_segmented.shape[2]-1
    
            self.var_ax = DoubleVar()
            ax_scale=Scale(
            self.window,
            variable=self.var_ax,
            from_=0,
            to=max,
            orient=HORIZONTAL,
            bg= "#000000",fg="white", font=self.bigFont2,borderwidth=0,troughcolor="white", command=self.plotAx)

            ax_scale.place(x=800, y=160,width=150, height=50)


        
    def plotAx(self, *args ):
            self.canvas.delete("all")
            if (self.Axis.get()=="select"):
                 self.ax.imshow(self.data_segmented[:,:,30])
            else:
                if(self.Axis.get()=="x"):
                    self.ax_x=int(self.var_ax.get())
                    self.ax_y=-1
                    self.ax_z=-1
                    self.ax.imshow(self.data_segmented[self.ax_x,:,:])
                    
            
                if(self.Axis.get()=="y"):
                    self.ax_x=-1
                    self.ax_y=int(self.var_ax.get())
                    self.ax_z=-1
                    self.ax.imshow(self.data_segmented[:,self.ax_y,:])
                    
                if(self.Axis.get()=="z"):
                    self.ax_x=-1
                    self.ax_y=-1
                    self.ax_z=int(self.var_ax.get())
                    self.ax.imshow(self.data_segmented[:,:,self.ax_z])

            
            self.canvas_widget.draw() 
         