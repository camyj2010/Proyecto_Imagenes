import SimpleITK as sitk
import nibabel as nib
import matplotlib.pyplot as plt
from tkinter.font import Font
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import numpy as np
import customtkinter
import os
from Segmentation_Algorithm.kMeans import k_means
from ants import get_ants_data, image_read, resample_image, get_mask, registration, apply_transforms, from_numpy, image_write
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
from Standarization_Algorithm.z_score import Z_score
from Denoise_Algorithm.median_filter_borders import Median_filter_borders
# from register_algoritm.registration_algorithm import register_algorithm
class Registration():
    
    def __init__(self, window, image_data, ax_x, ax_y, ax_z, bigfont2, canvas, axx, canvas_widget, axis, listAxis,image_name, path):
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
        self.data_registrate = self.data
        self.image_name=image_name
        self.histogram_matching_frame=None
        self.file_path=path
        # Menu para estandarizar
        self.registation_frame = tk.Frame(self.window, bg="#000000")
        
        
        self.button_registrate = customtkinter.CTkButton(self.registation_frame, text="Registrate",font=("PT Bold Heading",12), width=200,height=40, command=self.registrate)
        self.button_registrate.place(x=65, y=100)
        l_ax=tk.Label(self.registation_frame,text= "Axis",fg="white",bg = "#000000", font=self.bigFont2)
        ax_menu = tk.OptionMenu(self.registation_frame, self.Axis, *self.ax_list, command=self.display_selected)
        ax_menu.place(x=50, y=30)
        l_ax.place(x=0, y=30)
        #self.registation_frame_l_register = tk.Label(self.standarization_frame, text="Image to registrate", fg="white", bg="#000000", font=self.bigFont2)
        # self.standarization_frame_question_menu = tk.OptionMenu(self.standarization_frame, self.combobox, *options_list)
        # self.standarization_frame_question_menu.place(x=120, y=85)
        

        # Agregar el marco al window
        self.registation_frame.place(x=690, y=70, relwidth=1, relheight=1)

   

    def registrate(self):
        
        image = nib.load(self.file_path).get_fdata()
        print("1")
        image=Z_score(image)
        print("2")
        image=Median_filter_borders(image)
        print("3")
        if((self.image_name=="T1.nii.gz")or (self.image_name=="T1.nii") ):
            
            segmentate = k_means(image, 4, 10)
        if((self.image_name=="IR.nii.gz")or (self.image_name=="IR.nii") ):
             segmentate=k_means(image,2, 10)
        print("4")
        imageUploaded = nib.load('Patient/'+self.image_name)
        affine = imageUploaded.affine
        reconstructed_image = nib.Nifti1Image(segmentate.astype(np.float32), affine)
        output_path = os.path.join("Patient", "SEG_"+self.image_name)
        nib.save(reconstructed_image, output_path)

        fixed_image = image_read("Patient/FLAIR.nii.gz")
        moving_image = image_read("Patient/SEG_"+self.image_name)
        transform = registration(fixed=fixed_image, moving=moving_image, type_of_transform='Rigid')
        registered_image = apply_transforms(fixed=fixed_image, moving=moving_image, transformlist=transform['fwdtransforms'])
        self.data_registrate = registered_image.numpy()

        imageUploaded = nib.load('Patient/'+self.image_name)
        affine = imageUploaded.affine
        reconstructed_image = nib.Nifti1Image(self.data_registrate.astype(np.float32), affine)
        output_path = os.path.join("Patient", "Register_"+self.image_name)
        nib.save(reconstructed_image, output_path)
        print("5")

        self.plotAx()
      
    def segmentate_register(self):
        self.data_registrate = nib.load('Patient/Registered_'+self.image_name).get_fdata()
        if((self.image_name=="T1.nii.gz")or (self.image_name=="T1.nii") ):
            self.data_registrate=k_means(self.data_registrate,4, 10)
            imageUploaded = nib.load('Patient/Registered_'+self.image_name)
            affine = imageUploaded.affine
            reconstructed_image = nib.Nifti1Image(self.data_registrate.astype(np.float32), affine)
            output_path = os.path.join("Patient", "Final_"+self.image_name)
            nib.save(reconstructed_image, output_path)
            self.data_registrate=nib.load("Patient/Final_"+self.image_name).get_fdata()
        if((self.image_name=="IR.nii.gz")or (self.image_name=="IR.nii") ):
            self.data_registrate=k_means(self.data_registrate,2, 10)
            imageUploaded = nib.load('Patient/Registered_'+self.image_name)
            affine = imageUploaded.affine
            reconstructed_image = nib.Nifti1Image(self.data_registrate.astype(np.float32), affine)
            output_path = os.path.join("Patient", "Final_"+self.image_name)
            nib.save(reconstructed_image, output_path)
            self.data_registrate=nib.load("Patient/Final_"+self.image_name).get_fdata()
        self.plotAx()
       
    def display_selected(self, *args):
        
            if(self.Axis.get()=="x"):
                
                max=self.data_registrate.shape[0]-1
            elif(self.Axis.get()=="y"):
                max=self.data_registrate.shape[1]-1
                
            elif(self.Axis.get()=="z"):
                max=self.data_registrate.shape[2]-1
    
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
                 self.ax.imshow(self.data_registrate[:,:,30])
            else:
                if(self.Axis.get()=="x"):
                    self.ax_x=int(self.var_ax.get())
                    self.ax_y=-1
                    self.ax_z=-1
                    self.ax.imshow(self.data_registrate[self.ax_x,:,:])
                    
            
                if(self.Axis.get()=="y"):
                    self.ax_x=-1
                    self.ax_y=int(self.var_ax.get())
                    self.ax_z=-1
                    self.ax.imshow(self.data_registrate[:,self.ax_y,:])
                    
                if(self.Axis.get()=="z"):
                    self.ax_x=-1
                    self.ax_y=-1
                    self.ax_z=int(self.var_ax.get())
                    self.ax.imshow(self.data_registrate[:,:,self.ax_z])

            self.ax.set_aspect("auto",adjustable="box")
            self.canvas_widget.draw() 
    