from tkinter.font import Font
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import numpy as np
from Standarization_Algorithm.rescaling import Rescaling
from Standarization_Algorithm.z_score import Z_score
from Standarization_Algorithm.white_stripe import White_stripe
from Standarization_Algorithm.histogram_matching import histogram_matching
from Denoise_Algorithm.mean_filter import Mean_Filter
from Denoise_Algorithm.median_filter import Median_filter
from Denoise_Algorithm.median_filter_borders import Median_filter_borders

import customtkinter

class Standarization():
    def __init__(self, window, image_data, ax_x, ax_y, ax_z, bigfont2, canvas, axx, canvas_widget, axis, listAxis,image_name):
        self.window = window
        self.data = image_data
        self.ax_x = ax_x
        self.ax_y = ax_y
        self.ax_z = ax_z
        self.bigFont2 = bigfont2
        self.standarization_frame= None
        self.canvas = canvas
        self.ax = axx
        self.canvas_widget = canvas_widget
        self.Axis = axis
        self.ax_list = listAxis
        self.data_standardized = self.data
        self.image_name=image_name
        self.histogram_matching_frame=None
    
        # Menu para estandarizar
        self.standarization_frame = tk.Frame(self.window, bg="#000000")
        options_list = ["Rescaling", "Z-score", "Histogram Matching", "White Stripe" ]
        self.standarization_frame_standarization_method = tk.StringVar(self.standarization_frame)
        self.standarization_frame_standarization_method.set("Select an Option")
        self.standarization_frame_l_algorimt = tk.Label(self.standarization_frame, text="Standarization", fg="white", bg="#000000", font=self.bigFont2)
        self.standarization_frame_question_menu = tk.OptionMenu(self.standarization_frame, self.standarization_frame_standarization_method, *options_list, command=self.select_algorithm)
        self.standarization_frame_question_menu.place(x=120, y=85)
        self.standarization_frame_l_algorimt.place(x=0, y=85)
        l_ax=tk.Label(self.standarization_frame,text= "Axis",fg="white",bg = "#000000", font=self.bigFont2)
        ax_menu = tk.OptionMenu(self.standarization_frame, self.Axis, *self.ax_list, command=self.display_selected)
        ax_menu.place(x=50, y=30)
        l_ax.place(x=0, y=30)
        #Menu para remoción de ruido

        self.standarization_frame_l_filter = tk.Label(self.standarization_frame, text="Denoise", fg="white", bg="#000000", font=self.bigFont2)
        filters_list = ["Mean Filter", "Median Filter", "Median Filter Borders"]
        self.standarization_frame_filter_method = tk.StringVar(self.standarization_frame)
        self.standarization_frame_filter_method.set("Select an Option")
        self.standarization_frame_question_menu = tk.OptionMenu(self.standarization_frame, self.standarization_frame_filter_method, *filters_list, command=self.select_filter)
        self.standarization_frame_l_filter.place(x=0, y=460)
        self.standarization_frame_question_menu.place(x=80, y=460)
        # plot de un histograma
        self.hist_fig, self.hist_ax = plt.subplots(figsize=(3, 3))
        self.hist_ax.hist(self.data[self.data > 10].flatten(), 100)
        self.hist_fig.tight_layout()

        self.standarization_frame_canvashist = FigureCanvasTkAgg(self.hist_fig, master=self.standarization_frame)
        self.standarization_frame_canvashist.draw()
        self.standarization_frame_canvashist.get_tk_widget().place(x=0, y=200, width=250, height=250)

        # Agregar el marco al window
        self.standarization_frame.place(x=690, y=70, relwidth=1, relheight=1)


    def plotHistogram(self,type):
        self.standarization_frame_canvashist.get_tk_widget().delete("all")
        # create a new histogram on a new axes object
        fig, ax = plt.subplots(figsize=(3, 3))
        if type== "Rescaling":
            ax.hist(self.data_standardized[self.data_standardized > 0.02].flatten(), 100)
            # ax.hist(self.data_standardized.flatten(), 100)
        if type== "Z-score":
            ax.hist(self.data_standardized[self.data_standardized > (-1.7)].flatten(), 100)
            # ax.hist(self.data_standardized.flatten(), 100)
        if type== "White Stripe":
            ax.hist(self.data_standardized[self.data_standardized > (0.02)].flatten(), 100)
            # ax.hist(self.data_standardized.flatten(), 100)
        if type== "Histogram Matching":
            ax.hist(self.data_standardized[self.data_standardized > (10)].flatten(), 100)
        # ax.hist(self.data_standardized.flatten(), 100)
        fig.tight_layout()

        # replace the existing canvas with the new one
        self.standarization_frame_canvashist = FigureCanvasTkAgg(fig, master=self.standarization_frame)
        self.standarization_frame_canvashist.draw()
        self.standarization_frame_canvashist.get_tk_widget().place(x=0, y=200, width=250, height=250)

    def select_filter(self, *args):
        if self.standarization_frame_filter_method.get() == "Mean Filter": 
            self.data_standardized=Mean_Filter(self.data_standardized)
            # self.plotHistogram()
            self.plotAx()
        if self.standarization_frame_filter_method.get() == "Median Filter": 
            self.data_standardized=Median_filter(self.data_standardized)
            # self.plotHistogram()
            self.plotAx()
        if self.standarization_frame_filter_method.get() == "Median Filter Borders": 
            self.data_standardized=Median_filter_borders(self.data_standardized)
            # self.plotHistogram()
            self.plotAx()    
             
    def select_algorithm(self, *args):
        if self.standarization_frame_standarization_method.get() == "Rescaling":
                
                if self.histogram_matching_frame is not None:
                    widgets = [self.label_historgram, self.entryKlandmarks,self.btn]
                    for widget in widgets:
                        widget.destroy()
                    self.histogram_matching_frame.destroy()
                    self.histogram_matching_frame= None

                self.data_standardized=Rescaling(self.data)
                self.plotHistogram("Rescaling")
                self.plotAx()
        if self.standarization_frame_standarization_method.get() == "Z-score":
                
                if self.histogram_matching_frame is not None:
                    widgets = [self.label_historgram, self.entryKlandmarks,self.btn]
                    for widget in widgets:
                        widget.destroy()
                    self.histogram_matching_frame.destroy()
                    self.histogram_matching_frame= None

                self.data_standardized=Z_score(self.data)
                self.plotHistogram("Z-score")
                self.plotAx() 
        if self.standarization_frame_standarization_method.get() == "White Stripe":
                if self.histogram_matching_frame is not None:
                    widgets = [self.label_historgram, self.entryKlandmarks,self.btn]
                    for widget in widgets:
                        widget.destroy()
                    self.histogram_matching_frame.destroy()
                    self.histogram_matching_frame= None

                self.data_standardized=White_stripe(self.data)
                self.plotHistogram("White Stripe")
                self.plotAx()
        if self.standarization_frame_standarization_method.get()== "Histogram Matching":
                if self.histogram_matching_frame is None:
                    self.histogram_matching_frame = tk.Frame(self.standarization_frame, bg="#000000")
                    self.label_historgram = tk.Label(self.histogram_matching_frame, text="k landmarks", fg="white", bg="#000000", font=self.bigFont2)
                    self.entryKlandmarks = tk.Entry(self.histogram_matching_frame,justify="center", fg="white", bg="#000000")
                    self.img_boton2 = tk.PhotoImage(file="play.png")
                    self.btn = tk.Button(self.histogram_matching_frame, image=self.img_boton2, bg="#000000", borderwidth=0, command= self.hist_matching)
                    self.entryKlandmarks.insert(0, "4")
                    self.entryKlandmarks.place(x=90, y=0, width=100, height=25)
                    self.btn.place(x=220, y=5)
                    self.histogram_matching_frame.place(x=0, y=140, width=300, height=40)
                    self.label_historgram.place(x=0, y=0)
    def hist_matching(self):
        if((self.image_name=="T1.nii.gz")or (self.image_name=="T1.nii") ):
            self.imgRefenrece = nib.load('imagenes_pruebas/1/T1.nii.gz')
            self.imgRefenrece_data=self.imgRefenrece.get_fdata()
            self.data_standardized=histogram_matching(self.imgRefenrece_data,self.data,int(self.entryKlandmarks.get()))
            self.plotHistogram("Histogram Matching")
            self.plotAx()
            
        if((self.image_name=="IR.nii.gz")or (self.image_name=="IR.nii") ):
            self.imgRefenrece = nib.load('imagenes_pruebas/1/IR.nii.gz')
            self.imgRefenrece_data=self.imgRefenrece.get_fdata()
            self.data_standardized=histogram_matching(self.imgRefenrece_data,self.data,int(self.entryKlandmarks.get()))
            self.plotHistogram("Histogram Matching")
            self.plotAx()
           
        if((self.image_name=="FLAIR.nii.gz")or (self.image_name=="FLAIR.nii") ):
            self.imgRefenrece = nib.load('imagenes_pruebas/1/FLAIR.nii.gz')
            self.imgRefenrece_data=self.imgRefenrece.get_fdata()
            self.data_standardized=histogram_matching(self.imgRefenrece_data,self.data,int(self.entryKlandmarks.get()))
            self.plotHistogram("Histogram Matching")
            self.plotAx()

    def display_selected(self, *args):
        
            if(self.Axis.get()=="x"):
                
                max=self.data_standardized.shape[0]-1
            elif(self.Axis.get()=="y"):
                max=self.data_standardized.shape[1]-1
                
            elif(self.Axis.get()=="z"):
                max=self.data_standardized.shape[2]-1
    
            self.var_ax = DoubleVar()
            ax_scale=Scale(
            self.window,
            variable=self.var_ax,
            from_=0,
            to=max,
            orient=HORIZONTAL,
            bg= "#000000",fg="white", font=self.bigFont2,borderwidth=0,troughcolor="white", command=self.plotAx)

            ax_scale.place(x=800, y=97,width=150, height=50)


        
    def plotAx(self, *args ):
            self.canvas.delete("all")
            if (self.Axis.get()=="select"):
                 self.ax.imshow(self.data_standardized[:,:,30], cmap="gray")
            else:
                if(self.Axis.get()=="x"):
                    self.ax_x=int(self.var_ax.get())
                    self.ax_y=-1
                    self.ax_z=-1
                    self.ax.imshow(self.data_standardized[self.ax_x,:,:], cmap="gray")
                    
            
                if(self.Axis.get()=="y"):
                    self.ax_x=-1
                    self.ax_y=int(self.var_ax.get())
                    self.ax_z=-1
                    self.ax.imshow(self.data_standardized[:,self.ax_y,:], cmap="gray")
                    
                if(self.Axis.get()=="z"):
                    self.ax_x=-1
                    self.ax_y=-1
                    self.ax_z=int(self.var_ax.get())
                    self.ax.imshow(self.data_standardized[:,:,self.ax_z], cmap="gray")

            self.ax.set_aspect("auto",adjustable="box")
            self.canvas_widget.draw() 
         
    
    