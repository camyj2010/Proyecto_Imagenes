from tkinter.font import Font
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from thresholdind import thres
from kMeans import k_means

class Main():
    def __init__(self):
        self.file_path=""
       #General Config
        self.window=tk.Tk()
        self.window.geometry("1000x600")
        #Image fond
        bgimg= tk.PhotoImage(file = "fondo_2.png")
        limg= Label(self.window, image=bgimg)
        limg.place(x = -50, y =-50)
        self.window['bg'] = "#000000"
        #Font
        self.bigFont=Font(family="MS Reference Sans Serif", size=30, weight="bold", slant="roman", underline=0, overstrike=0)
        self.bigFont1=Font(family="PT Bold Heading", size=12, slant="roman", underline=0, overstrike=0)
        self.bigFont2=Font(family="PT Bold Heading", size=9, slant="roman", underline=0, overstrike=0)

        # Define the style for combobox widget
        style= ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground= "#000000", background= "white")

        options_list = ["Thresholdind", "K-means","Region Growing"]
        self.ax_list=["x","y","z"]
        #Title
        title=tk.Label(self.window,text= "IMAGE PROCESSOR",fg="white",bg = "#000000", font=self.bigFont)
        title.pack(pady = 30)

        self.window.title("Image Processor")
        # Crear un botón para abrir la ventana de selección de archivo
        img_boton = tk.PhotoImage(file="search.png")
        l_upload=tk.Label(self.window,text= "Upload Image",fg="white",bg = "#000000", font=self.bigFont1)
        l_ax=tk.Label(self.window,text= "Axis",fg="white",bg = "#000000", font=self.bigFont1)
        
        l_algorimt=tk.Label(self.window,text= "Segmentation",fg="white",bg = "#000000", font=self.bigFont1)
        
        
        self.segmentation_method =  tk.StringVar(self.window)
        self.segmentation_method.set("Select an Option")
         # default value
        question_menu = tk.OptionMenu(self.window,  self.segmentation_method, *options_list, command=self.select_algorithm)

        self.Axis =  tk.StringVar(self.window)
        self.Axis.set("x") # default value
        ax_menu = tk.OptionMenu(self.window, self.Axis, *self.ax_list,command=self.display_selected)
        boton = tk.Button(self.window,image=img_boton, command=self.open_file,bg = "#000000",borderwidth=0)
        
        question_menu.place(x=850, y=225)
        l_algorimt.place(x=700, y=220)
        #box_algoritm.place(x=850, y=255)
        l_ax.place(x=700, y=100)
        ax_menu.place(x=800, y=105)
        #box_ax.place(x=800, y=105)
        l_upload.place(x=50, y=110)
        boton.place(x=190, y=100)

    
        # Crear un lienzo para mostrar la imagen
        self.canvas = tk.Canvas(self.window,bg = "#000000")
        self.canvas.place( x=300, y=190,width=380, height=380)
            # Title


        self.window.mainloop()



    def open_file(self):
    
        

        # Obtener la ruta del archivo seleccionado
        self.file_path = filedialog.askopenfilename()

        # Cargar la imagen nii utilizando nibabel
        self.img = nib.load(self.file_path)
        self.data = self.img.get_fdata()
        self.init_plot()
        # Mostrar la imagen en un lienzo

    def init_plot(self):
        self.canvas.delete("all")
        # Crear una figura y un objeto de plot
        self.fig, self.ax = plt.subplots()
        # Mostrar la imagen en el plot
        self.ax.imshow(self.data[:,:,5])


        #    Convertir la figura en un widget de Tkinter y mostrarla en el canvas
        self.canvas_widget = FigureCanvasTkAgg(self.fig, self.canvas)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().place( x=0, y=0,width=380, height=380)

    def display_selected(self, *args):
        if(self.file_path==""):
            messagebox.showerror(message="No image loaded", title="ERROR")
        else:
            if(self.Axis.get()=="x"):
                
                max=self.data.shape[0]-1
            elif(self.Axis.get()=="y"):
                max=self.data.shape[1]-1
                
            elif(self.Axis.get()=="z"):
                max=self.data.shape[2]-1
    
            self.var_ax = DoubleVar()
            ax_scale=Scale(
            self.window,
            variable=self.var_ax,
            from_=0,
            to=max,
            orient=HORIZONTAL,
            bg= "#000000",fg="white", font=self.bigFont2,borderwidth=0,troughcolor="white", command=self.plot)

            ax_scale.place(x=800, y=150,width=150, height=50)

    # Define the select_algorithm function
    def select_algorithm(self, *args):
        if(self.file_path==""):
            messagebox.showerror(message="No image loaded", title="ERROR")
        else:
            if(self.segmentation_method.get()=="Thresholdind"):
                 self.ax.imshow(thres(self.data,1, 150)[:, :, 100]) 
                # self.tolerance = tk.StringVar(self.window)
                # self.tolerance.set(1)
                # self.taoo = tk.StringVar(self.window)
                # self.taoo.set(150)
                # l_tao = tk.Label(self.window, text="Tao", fg="white", bg="#000000", font=self.bigFont1)
                # l_tol = tk.Label(self.window, text="Tolerance", fg="white", bg="#000000", font=self.bigFont1)
                # self.tol_text = ttk.Spinbox(from_=20, to=150, increment=10, textvariable=self.tolerance, command=self.tol)
                # self.tao_text = ttk.Spinbox(from_=20, to=150, increment=10, textvariable=self.taoo, command=self.tao)

                # self.tol_text.place(x=800, y=320, width=100, height=25)
                # self.tao_text.place(x=800, y=280, width=100, height=25)

                # l_tao.place(x=700, y=280)
                # l_tol.place(x=700, y=320)

                

            elif(self.segmentation_method.get()=="K-means"):
                self.ax.imshow(k_means(self.data,1, 150)[:, :, 100])

            elif(self.segmentation_method.get()=="z"):
                x = self.data.shape[2] - 1
            self.canvas_widget.draw()

    def tol(self, *args):
        if(self.tol_text.get()):
            self.tolerance = int(self.tol_text.get()[:2])
            if(self.taoo!=150):
                    print("cccc")
                    
                    img_boton_play = tk.PhotoImage(file="play.png")
                    boton_play = tk.Button(self.window, image=img_boton_play, bg="#000000", borderwidth=0, command=lambda: thres(self.data, self.tolerance.get(), self.taoo.get()))
                    boton_play.place(x=700, y=320)
            return self.tolerance

    def tao(self, *args):
        if(self.tao_text.get()):
            self.taoo = int(self.tao_text.get())
            if(self.tolerance!=1):
                    print("cccc")
                    
                    img_boton_play = tk.PhotoImage(file="play.png")
                    boton_play = tk.Button(self.window, image=img_boton_play, bg="#000000", borderwidth=0, command=lambda: thres(self.data, self.tolerance.get(), self.taoo.get()))
                    boton_play.place(x=700, y=320)
            return self.taoo
        
    def plot(self, *args ):
            self.canvas.delete("all")
            
            if(self.Axis.get()=="x"):
                    self.ax.imshow(self.data[int(self.var_ax.get()),:,:])
                
            if(self.Axis.get()=="y"):
                    self.ax.imshow(self.data[:,int(self.var_ax.get()),:])
                    
            if(self.Axis.get()=="z"):
                    self.ax.imshow(self.data[:,:,int(self.var_ax.get())])

            
            self.canvas_widget.draw()
            
    
         

        

Main()    




