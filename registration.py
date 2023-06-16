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
from Standarization_Algorithm.z_score import Z_score
from Denoise_Algorithm.median_filter_borders import Median_filter_borders
from remote_skull import remote
from volume import volumes
# from register_algoritm.registration_algorithm import register_algorithm
class Registration():
    
    def __init__(self, window, image_data, ax_x, ax_y, ax_z, bigfont2, canvas, axx, canvas_widget, axis, listAxis,image_name, path, bigfont1):
        self.window = window
        self.data = image_data
        self.ax_x = ax_x
        self.ax_y = ax_y
        self.ax_z = ax_z
        self.bigFont2 = bigfont2
        self.bigFont1= bigfont1
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


        self.count1=""

        # Menu para estandarizar
        self.registation_frame = tk.Frame(self.window, bg="#000000")
        
        
        self.button_registrate = customtkinter.CTkButton(self.registation_frame, text="Registrate",font=("PT Bold Heading",12), width=200,height=40, command=self.registrate)
        self.button_registrate.place(x=55, y=100)
        self.button_remove_skull = customtkinter.CTkButton(self.registation_frame, text="Remove skull",font=("PT Bold Heading",12), width=200,height=40, command=self.remove)
        self.button_remove_skull.place(x=55, y=200)

        
        l_ax=tk.Label(self.registation_frame,text= "Axis",fg="white",bg = "#000000", font=self.bigFont2)
        ax_menu = tk.OptionMenu(self.registation_frame, self.Axis, *self.ax_list, command=self.display_selected)
        ax_menu.place(x=50, y=30)
        l_ax.place(x=0, y=30)
        #self.registation_frame_l_register = tk.Label(self.standarization_frame, text="Image to registrate", fg="white", bg="#000000", font=self.bigFont2)
        # self.standarization_frame_question_menu = tk.OptionMenu(self.standarization_frame, self.combobox, *options_list)
        # self.standarization_frame_question_menu.place(x=120, y=85)
        

        # Agregar el marco al window
        self.registation_frame.place(x=690, y=70, relwidth=1, relheight=1)

    def remove(self):
        remote()
        self.otro()

    def otro(self):
        self.data_registrate = nib.load("Patient/FLAIR_skull_lesion.nii.gz").get_fdata()
        counts=volumes("Patient/FLAIR_skull_lesion.nii.gz")
       
        print(counts)

        self.volumes_frame = tk.Frame(self.registation_frame, bg="#000000")
        label =tk.Label(self.volumes_frame,text= "Volumes",fg="white",bg = "#000000", font=self.bigFont1)
        label.place(x=0, y=0)

        label_0 =tk.Label(self.volumes_frame,text= "Label 0",fg="white",bg = "#000000", font=self.bigFont2)
        label_0.place(x=15, y=30)
        label_1 =tk.Label(self.volumes_frame,text= "Label 1",fg="white",bg = "#000000", font=self.bigFont2)
        label_1.place(x=15, y=60)
        label_2 =tk.Label(self.volumes_frame,text= "Label 2",fg="white",bg = "#000000", font=self.bigFont2)
        label_2.place(x=15, y=90)
        label_3 =tk.Label(self.volumes_frame,text= "Label 3",fg="white",bg = "#000000", font=self.bigFont2)
        label_3.place(x=15, y=120)
        label_4 =tk.Label(self.volumes_frame,text= "Label 4",fg="white",bg = "#000000", font=self.bigFont2)
        label_4.place(x=15, y=150)
        # label_5 =tk.Label(self.volumes_frame,text= "Label 5",fg="white",bg = "#000000", font=self.bigFont2)
        # label_5.place(x=15, y=180)
        # label_6 =tk.Label(self.volumes_frame,text= "Label 6",fg="white",bg = "#000000", font=self.bigFont2)
        # label_6.place(x=15, y=210)

        label_11 =tk.Label(self.volumes_frame,text= counts[0],fg="white",bg = "#000000", font=self.bigFont1)
        label_11.place(x=70, y=25)
        label_21 =tk.Label(self.volumes_frame,text= counts[1],fg="white",bg = "#000000", font=self.bigFont1)
        label_21.place(x=70, y=55)
        label_31 =tk.Label(self.volumes_frame,text= counts[2],fg="white",bg = "#000000", font=self.bigFont1)
        label_31.place(x=70, y=85)
        label_41 =tk.Label(self.volumes_frame,text= counts[3],fg="white",bg = "#000000", font=self.bigFont1)
        label_41.place(x=70, y=115)
        label_51 =tk.Label(self.volumes_frame,text= counts[4],fg="white",bg = "#000000", font=self.bigFont1)
        label_51.place(x=70, y=145)
        # label_61 =tk.Label(self.volumes_frame,text= counts[5],fg="white",bg = "#000000", font=self.bigFont1)
        # label_61.place(x=70, y=175)
        # label_71 =tk.Label(self.volumes_frame,text= counts[6],fg="white",bg = "#000000", font=self.bigFont1)
        # label_71.place(x=70, y=215)
        self.volumes_frame.pack()
        self.volumes_frame.place(x=0, y=300, relwidth=1, relheight=1)

        self.plotAx()
    def registrate(self):
        
        
        image = nib.load(self.file_path).get_fdata()
        image=Z_score(image)
        image=Median_filter_borders(image)
        
        
        if((self.image_name=="T1.nii.gz")or (self.image_name=="T1.nii") ):
            
            segmentate = k_means(image, 4, 10)
        if((self.image_name=="IR.nii.gz")or (self.image_name=="IR.nii") ):
             segmentate=k_means(image,2, 10)
        print("4")
        

        imageUploaded = nib.load('Patient/'+self.image_name)
        affine = imageUploaded.affine
        reconstructed_image = nib.Nifti1Image(segmentate.astype(np.float32), affine)
        output_path = os.path.join("Patient", "seg_"+self.image_name)
        nib.save(reconstructed_image, output_path)


        file_name = os.path.basename('Patient/FLAIR.nii.gz')
        name, ext = os.path.splitext(file_name) 

        # Load fixed and moving images
        fixed_image = sitk.ReadImage('Patient/FLAIR.nii.gz')
        moving_seg_image = sitk.ReadImage('Patient/seg_'+self.image_name)
        moving_image=sitk.ReadImage(self.file_path)

        # Convert image types
        fixed_image = sitk.Cast(fixed_image, sitk.sitkFloat32)
        moving_image = sitk.Cast(moving_image, sitk.sitkFloat32)
        moving_seg_image= sitk.Cast(moving_seg_image, sitk.sitkFloat32)
        
        # Define the registration components
        registration_method = sitk.ImageRegistrationMethod()

        # Similarity metric - Mutual Information
        registration_method.SetMetricAsMattesMutualInformation()

        # Interpolator
        registration_method.SetInterpolator(sitk.sitkNearestNeighbor)

        # Optimizer - Gradient Descent
        registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100,
                                                        estimateLearningRate=registration_method.EachIteration)

        # Initial transform - Identity
        initial_transform = sitk.Transform()
        registration_method.SetInitialTransform(initial_transform)

        # Setup for the registration process
        registration_method.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
        registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
        registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

        # Perform registration
        final_transform = registration_method.Execute(fixed_image, moving_image)

        # Resample the moving image to match the fixed image dimensions and orientation
        reference_image = fixed_image
        interpolator = sitk.sitkNearestNeighbor
        default_pixel_value = 0.0
        resampled_image = sitk.Resample( moving_seg_image,reference_image, final_transform,
                                        interpolator, 0.0, reference_image.GetPixelID())

        # Convert the resampled image to Numpy array
        resampled_array = sitk.GetArrayFromImage(resampled_image)

        # Save the resampled image as NIfTI
        # imageUploaded = nib.load('Patient/FLAIR.nii.gz')
        # affine = imageUploaded.affine
        # reconstructed_image = nib.Nifti1Image(resampled_array.astype(np.float32), affine)
        # output_path = os.path.join("Patient", "registered_"+self.image_name)
        # nib.save(reconstructed_image, output_path)

        sitk.WriteImage(resampled_image, "Patient/registered_"+self.image_name)

        self.segmentate_register()
        
       
    def segmentate_register(self):
        self.data_registrate = nib.load('Patient/registered_'+self.image_name).get_fdata()
        # if((self.image_name=="T1.nii.gz")or (self.image_name=="T1.nii") ):
        #     # self.data_registrate=k_means(self.data_registrate,4, 10)
        #     imageUploaded = nib.load('Patient/Registered_'+self.image_name)
        #     affine = imageUploaded.affine
        #     reconstructed_image = nib.Nifti1Image(self.data_registrate.astype(np.float32), affine)
        #     output_path = os.path.join("Patient", "Final_"+self.image_name)
        #     nib.save(reconstructed_image, output_path)
        #     self.data_registrate=nib.load("Patient/Final_"+self.image_name).get_fdata()
        # if((self.image_name=="IR.nii.gz")or (self.image_name=="IR.nii") ):
        #     # self.data_registrate=k_means(self.data_registrate,2, 10)
        #     imageUploaded = nib.load('Patient/Registered_'+self.image_name)
        #     affine = imageUploaded.affine
        #     reconstructed_image = nib.Nifti1Image(self.data_registrate.astype(np.float32), affine)
        #     output_path = os.path.join("Patient", "Final_"+self.image_name)
        #     nib.save(reconstructed_image, output_path)
        #     self.data_registrate=nib.load("Patient/Final_"+self.image_name).get_fdata()
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
            self.original = nib.load("Patient/FLAIR.nii.gz").get_fdata()
            if (self.Axis.get()=="select"):
                 
                 self.ax.imshow(self.data_registrate[:,:,30])
                 self.ax.imshow(self.original[:,:,30], cmap='gray',alpha=0.2)
            else:
                if(self.Axis.get()=="x"):
                    self.ax_x=int(self.var_ax.get())
                    self.ax_y=-1
                    self.ax_z=-1
                    
                    self.ax.imshow(self.data_registrate[self.ax_x,:,:])
                    self.ax.imshow(self.original[self.ax_x,:,:], cmap='gray',alpha=0.2)
            
                if(self.Axis.get()=="y"):
                    self.ax_x=-1
                    self.ax_y=int(self.var_ax.get())
                    self.ax_z=-1
                    
                    self.ax.imshow(self.data_registrate[:,self.ax_y,:])
                    self.ax.imshow(self.original[:,self.ax_y,:], cmap='gray',alpha=0.2)
                if(self.Axis.get()=="z"):
                    self.ax_x=-1
                    self.ax_y=-1
                    self.ax_z=int(self.var_ax.get())
                    
                    self.ax.imshow(self.data_registrate[:,:,self.ax_z])
                    self.ax.imshow(self.original[:,:,self.ax_z], cmap='gray',alpha=0.2)
            self.ax.set_aspect("auto",adjustable="box")
            self.canvas_widget.draw() 
    