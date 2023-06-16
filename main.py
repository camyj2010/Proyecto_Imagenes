from tkinter.font import Font
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import shutil
import os
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from standarization import Standarization
from segmentation import Segmentation
from registration import Registration
import customtkinter


class Main():
    def __init__(self):
        # Borra archivos previos
        archivos = os.listdir("Patient/")
        for archivo in archivos:
            ruta_archivo = os.path.join("Patient/", archivo)
            if os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)
        self.file_path=""
       #General Config
        self.window=tk.Tk()
        self.window.geometry("1000x630")
        #Image fond
        # bgimg= tk.PhotoImage(file = "fondo_2.png")
        # limg= Label(self.window, image=bgimg)
        # limg.place(x = -50, y =-50)
        self.window['bg'] = "#000000"
        #Font
        self.bigFont=Font(family="MS Reference Sans Serif", size=30, weight="bold", slant="roman", underline=0, overstrike=0)
        self.bigFont1=Font(family="PT Bold Heading", size=12, slant="roman", underline=0, overstrike=0)
        self.bigFont2=Font(family="PT Bold Heading", size=9, slant="roman", underline=0, overstrike=0)

        # Define the style for combobox widget
        style= ttk.Style()
        style.theme_use('clam')
        # style.configure("TCombobox", fieldbackground= "#000000", background= "white")

        self.ax_list=["x","y","z"]

        #Title

        title=tk.Label(self.window,text= "IMAGE PROCESSOR",fg="white",bg = "#000000", font=self.bigFont)
        title.pack(pady = 30)

        self.window.title("Image Processor")
        # Crear un botón para abrir la ventana de selección de archivo
        img_boton = tk.PhotoImage(file="images/search_1.png")
        l_upload=tk.Label(self.window,text= "Upload Image",fg="white",bg = "#000000", font=self.bigFont1)
        img_select = tk.PhotoImage(file="images/images.png")
        l_select=tk.Label(self.window,text= "Select an Image",fg="white",bg = "#000000", font=self.bigFont1)
        #l_ax=tk.Label(self.window,text= "Axis",fg="white",bg = "#000000", font=self.bigFont2)
        #l_ax.place(x=690, y=100)


        self.Axis =  tk.StringVar(self.window)
        self.Axis.set("select") # default value
        
        #ax_menu = tk.OptionMenu(self.window, self.Axis, *self.ax_list,command=self.display_selected)
        boton = tk.Button(self.window,image=img_boton, command=self.load_images,bg = "#000000",borderwidth=0)
        boton1 = tk.Button(self.window,image=img_select, command=self.select_file,bg = "#000000",borderwidth=0)
        

       
        #ax_menu.place(x=745, y=105)

        l_upload.place(x=50, y=110)
        boton.place(x=190, y=110)
        l_select.place(x=50, y=160)
        boton1.place(x=210, y=150)
        
        #Botones de los pasos 
        button_Standarization = customtkinter.CTkButton(self.window, text="Pre-Processing ",font=("PT Bold Heading",12), width=200,height=40, command=self.button_event)
        button_Segmentation = customtkinter.CTkButton(self.window, text="Segmentation",font=("PT Bold Heading",12), width=200,height=40, command=self.button_segmentation)
        button_PosgtSegmentation = customtkinter.CTkButton(self.window, text="Register",font=("PT Bold Heading",12), width=200,height=40, command=self.button_post)
        button_Standarization.place(x=50, y=220)
        button_Segmentation.place(x=50,y=270)
        button_PosgtSegmentation.place(x=50,y=320)
        # Crear un lienzo para mostrar la imagen
        self.canvas = tk.Canvas(self.window,bg = "#000000")
        self.canvas.place( x=300, y=190,width=380, height=380)
        #variables
        self.Ax_x= -1
        self.Ax_y= -1
        self.Ax_z= -1
        self.registration=FALSE
        self.segmentation=FALSE
        self.standarization=FALSE
        self.window.mainloop()

    
    def button_event(self):
            if(self.file_path==""):
                messagebox.showerror(message="No image loaded", title="ERROR")
            else:
                self.registration=FALSE
                self.segmentation=FALSE
                self.standarization=TRUE
                Standarization(self.window, self.data,self.Ax_x,self.Ax_y, self.Ax_z, self.bigFont2,self.canvas,self.ax,self.canvas_widget,self.Axis,self.ax_list,self.image_name)

    def button_segmentation(self):
            if(self.file_path==""):
                messagebox.showerror(message="No image loaded", title="ERROR")
            else:
                self.registration=FALSE
                self.segmentation=TRUE
                self.standarization=FALSE
                Segmentation(self.window, self.data,self.Ax_x,self.Ax_y, self.Ax_z, self.bigFont2,self.canvas,self.ax,self.canvas_widget,self.Axis,self.ax_list)
            
    def button_post(self):
        if(self.file_path==""):
            messagebox.showerror(message="No image loaded", title="ERROR")
        else:
            self.registration=TRUE
            self.segmentation=FALSE
            self.standarization=FALSE
            Registration(self.window, self.data,self.Ax_x,self.Ax_y, self.Ax_z, self.bigFont2,self.canvas,self.ax,self.canvas_widget,self.Axis,self.ax_list,self.image_name,self.file_path,self.bigFont1)

                 
    # def open_file(self):

    #     # Obtener la ruta del archivo seleccionado
    #     self.file_path = filedialog.askopenfilename()
    #     self.image_name = os.path.basename(self.file_path)
    #     # print(self.image_name)
    #     # Cargar la imagen nii utilizando nibabel
    #     self.img = nib.load(self.file_path)
    #     self.data = self.img.get_fdata()

    #     folder_path = "Patient/"
    #     destination_path = os.path.join(folder_path, self.image_name)
    #     shutil.copyfile(self.file_path, destination_path)

    #     self.init_plot()
    def load_images(self):
        # Obtener las rutas de los archivos seleccionados
        file_paths = filedialog.askopenfilenames()
        self.num_images = 0
        for file_path in file_paths:
            # Obtener el nombre de la imagen
            image_name = os.path.basename(file_path)
            # Cargar la imagen nii utilizando nibabel
            img = nib.load(file_path)
            data = img.get_fdata()

            folder_path = "Patient/"
            destination_path = os.path.join(folder_path, image_name)
            shutil.copyfile(file_path, destination_path)
            self.num_images += 1
        # Mostrar la imagen en un lienzo

    def select_file(self):
        # Obtener la ruta de la carpeta "Patient"
        folder_path = "Patient/"
        # Abrir la carpeta "Patient"
        root = Tk()
        root.withdraw()
        self.file_path = filedialog.askopenfilename(initialdir=folder_path)

        if self.file_path:
                # Obtener la ruta del archivo seleccionado
            self.image_name = os.path.basename(self.file_path)
            # Cargar la imagen nii utilizando nibabel
            self.img = nib.load(self.file_path)
            self.data = self.img.get_fdata()

            # Aquí puedes hacer algo con la imagen cargada, como mostrarla o procesarla
            self.init_plot()

    def init_plot(self):
        self.canvas.delete("all")
        # Crear una figura y un objeto de plot
        self.fig, self.ax = plt.subplots()
        # Mostrar la imagen en el plot
        self.ax.imshow(self.data[:,:,30], cmap="gray")
        self.ax.set_aspect("auto",adjustable="box")
        #    Convertir la figura en un widget de Tkinter y mostrarla en el canvas
        self.canvas_widget = FigureCanvasTkAgg(self.fig, self.canvas)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().place( x=0, y=0,width=380, height=380)
        if(self.standarization==TRUE):
            Standarization(self.window, self.data,self.Ax_x,self.Ax_y, self.Ax_z, self.bigFont2,self.canvas,self.ax,self.canvas_widget,self.Axis,self.ax_list,self.image_name)
        if(self.segmentation==TRUE):
            Segmentation(self.window, self.data,self.Ax_x,self.Ax_y, self.Ax_z, self.bigFont2,self.canvas,self.ax,self.canvas_widget,self.Axis,self.ax_list)
        if(self.registration==TRUE):    
            Registration(self.window, self.data,self.Ax_x,self.Ax_y, self.Ax_z, self.bigFont2,self.canvas,self.ax,self.canvas_widget,self.Axis,self.ax_list,self.image_name,self.file_path,self.bigFont1)

    # def display_selected(self, *args):
    #     if(self.file_path==""):
    #         messagebox.showerror(message="No image loaded", title="ERROR")
    #     else:
    #         if(self.Axis.get()=="x"):
                
    #             max=self.data.shape[0]-1
    #         elif(self.Axis.get()=="y"):
    #             max=self.data.shape[1]-1
                
    #         elif(self.Axis.get()=="z"):
    #             max=self.data.shape[2]-1
    
    #         self.var_ax = DoubleVar()
    #         ax_scale=Scale(
    #         self.window,
    #         variable=self.var_ax,
    #         from_=0,
    #         to=max,
    #         orient=HORIZONTAL,
    #         bg= "#000000",fg="white", font=self.bigFont2,borderwidth=0,troughcolor="white", command=self.plot)

    #         ax_scale.place(x=800, y=97,width=150, height=50)


        
    # def plot(self, *args ):
    #         self.canvas.delete("all")
            
    #         if(self.Axis.get()=="x"):
    #                 self.Ax_x=int(self.var_ax.get())
    #                 self.Ax_y=-1
    #                 self.Ax_z=-1
    #                 self.ax.imshow(self.data[self.Ax_x,:,:])
                    
            
    #         if(self.Axis.get()=="y"):
    #                 self.Ax_x=-1
    #                 self.Ax_y=int(self.var_ax.get())
    #                 self.Ax_z=-1
    #                 self.ax.imshow(self.data[:,self.Ax_y,:])
                    
    #         if(self.Axis.get()=="z"):
    #                 self.Ax_x=-1
    #                 self.Ax_y=-1
    #                 self.Ax_z=int(self.var_ax.get())
    #                 self.ax.imshow(self.data[:,:,self.Ax_z])

            
    #         self.canvas_widget.draw()
            
    
         

        

Main()    




