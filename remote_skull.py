import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import SimpleITK as sitk
from Segmentation_Algorithm.kMeans import k_means
from Denoise_Algorithm.median_filter_borders import Median_filter_borders
from tkinter import messagebox
import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import SimpleITK as sitk
import os




def remote():
    if (os.path.exists('Patient/registered_IR.nii.gz')and os.path.exists('Patient/registered_T1.nii.gz') ):
        # Cargar la imagen NIfTI

        nifti_img = nib.load(
        "Patient/registered_IR.nii.gz")
        # Asegúrate de ajustar la ruta y el nombre del archivo

        # Obtener los datos de la imagen
        data = nifti_img.get_fdata()

        # Definir escalas espaciales
        scales = [7.5]  # Escalas para aplicar filtros gaussianos

        # Aplicar filtros gaussianos en diferentes escalas
        filtered_images = []
        for scale in scales:
            # Aplicar filtro gaussiano
            filtered = ndimage.gaussian_filter(data, sigma=scale)
            filtered = k_means(filtered, 2,15)
            # Crear una nueva imagen nibabel con el cerebro extraído
            brain_extracted_image = nib.Nifti1Image(
            filtered, affine=nifti_img.affine, dtype=np.int16
            )

            # Guardar la imagen con el cerebro extraído en un nuevo archivo
            nib.save(brain_extracted_image,  "Patient/IR_skull.nii.gz")
            filtered_images.append(filtered)

        # RESTAR UNA IMAGEN

        # Cargar las imágenes
        imagen_original = sitk.ReadImage(
        "Patient/registered_T1.nii.gz")
    
        imagen_referencia = sitk.ReadImage("Patient/IR_skull.nii.gz")

        # Modify the metadata of image2 to match image1
        imagen_referencia.SetOrigin(imagen_original.GetOrigin())
        imagen_referencia.SetSpacing(imagen_original.GetSpacing())
        imagen_referencia.SetDirection(imagen_original.GetDirection())

        # Realizar segmentación basada en umbral adaptativo
        otsu_filter = sitk.OtsuThresholdImageFilter()
        otsu_filter.SetInsideValue(1)
        otsu_filter.SetOutsideValue(0)
        mascara_referencia = otsu_filter.Execute(imagen_referencia)

        # Aplicar la máscara a la imagen original
        imagen_sin_craneo = sitk.Mask(imagen_original, mascara_referencia)

        # Obtener los datos de la imagen sin el cráneo
        # Obtener los datos de la imagen sin el cráneo
        data_sin_craneo = sitk.GetArrayFromImage(imagen_sin_craneo)

        # Obtener los datos de la máscara
        data_mascara = sitk.GetArrayFromImage(mascara_referencia)

        # Crear una máscara booleana para los valores cero dentro del cerebro
        mascara_cero_cerebro = (data_sin_craneo == 0) & (data_mascara != 0)

        # Asignar un valor distinto a los valores cero dentro del cerebro
        valor_distinto = 4
        data_sin_craneo[mascara_cero_cerebro] = valor_distinto

        # Crear una nueva imagen SimpleITK con los datos modificados
        imagen_sin_craneo_modificada = sitk.GetImageFromArray(data_sin_craneo)
        imagen_sin_craneo_modificada.CopyInformation(imagen_sin_craneo)

        # Guardar la imagen sin el cráneo

        sitk.WriteImage(
            imagen_sin_craneo_modificada,"Patient/FLAIR_skull.nii.gz")

        # ----------------------------------------------------------------------------------
        # Quitar cráneo a FLAIR Original
        # ----------------------------------------------------------------------------------
        # Cargar las imágenes
        imageno= nib.load("Patient/FLAIR.nii.gz")
        imagenx= nib.load("Patient/FLAIR.nii.gz").get_fdata()
        imagenx2=Median_filter_borders(imagenx)

        brain_extracted_image = nib.Nifti1Image(
            imagenx2, affine= imageno.affine, dtype=np.int16
            )

        #     # Guardar la imagen con el cerebro extraído en un nuevo archivo
        nib.save(brain_extracted_image,  "Patient/FLAIR.nii.gz")
        

        imagen_original = sitk.ReadImage("Patient/FLAIR.nii.gz")
        imagen_referencia = sitk.ReadImage("Patient/IR_skull.nii.gz")

        # Realizar segmentación basada en umbral adaptativo
        otsu_filter = sitk.OtsuThresholdImageFilter()
        otsu_filter.SetInsideValue(1)
        otsu_filter.SetOutsideValue(0)
        mascara_referencia = otsu_filter.Execute(imagen_referencia)

        # Aplicar la máscara a la imagen original
        imagen_sin_craneo = sitk.Mask(imagen_original, mascara_referencia)

        # Guardar la imagen sin el cráneo

        sitk.WriteImage(
            imagen_sin_craneo,
           "Patient/FLAIR_original_sin_craneo.nii.gz"
        )

        # ----------------------------------------------------------------------------------
        # Segmentar lesiones
        # ----------------------------------------------------------------------------------

        image = nib.load("Patient/FLAIR_skull.nii.gz")
       
        image_data = image.get_fdata()
        image_data_flair_without_skull = nib.load(
        "Patient/FLAIR_original_sin_craneo.nii.gz").get_fdata()

        image_data_flair_segmented = k_means(image_data_flair_without_skull, 15, 15)

        # Where the values are 3, replace them in the image_data with a value of 3
        image_data_flair_segmented[:,:,:13] = 0
        image_data = np.where(image_data_flair_segmented == 6, 3, image_data)

        for z in range(14 - 1, -1, -1):
            image_data[:,:,z] = np.where(image_data[:,:,z] == 3, 0, image_data[:,:,z])

        affine = image.affine
        # Create a nibabel image object from the image data
        image = nib.Nifti1Image(image_data.astype(np.float32), affine=affine)
        # Save the image as a NIfTI file
        output_path = "Patient/FLAIR_skull_lesion.nii.gz"
        nib.save(image, output_path)

    else:
         messagebox.showerror(message="Images must be registered in Flair format", title="ERROR")
# def remote():
    
    # if (os.path.exists('Patient/registered_IR.nii.gz')and os.path.exists('Patient/registered_T1.nii.gz') ):
    #     #_______________________________________________QUITAR CRANEO__________________________________________________________
    #     # Cargar la imagen NIfTI
    #     nifti_img = nib.load('Patient/registered_IR.nii.gz')  # Asegúrate de ajustar la ruta y el nombre del archivo

    #     # Obtener los datos de la imagen
    #     data = nifti_img.get_fdata()

    #     # Preprocesamiento opcional
    #     # data = cv2.medianBlur(data, 5)  # Ejemplo de suavizado con filtro de mediana

    #     # Definir escalas espaciales
    #     scales = [7.5]  # Escalas para aplicar filtros gaussianos

    #     # Aplicar filtros gaussianos en diferentes escalas
    #     filtered_images = []
    #     for scale in scales:
    #         # Aplicar filtro gaussiano
    #         filtered = ndimage.gaussian_filter(data, sigma=scale)
    #         filtered = k_means(filtered, 2, 10)
    #         # Crear una nueva imagen nibabel con el cerebro extraído
    #         brain_extracted_image = nib.Nifti1Image(filtered, affine=nifti_img.affine, dtype=np.int16)

    #         # Guardar la imagen con el cerebro extraído en un nuevo archivo
    #         nib.save(brain_extracted_image, 'Patient/IR_skull.nii.gz')
    #         filtered_images.append(filtered)

    #     # RESTAR UNA IMAGEN 

    #     # Cargar las imágenes
    #     imagen_original = sitk.ReadImage('Patient/registered_T1.nii.gz')
    #     imagen_referencia = sitk.ReadImage('Patient/IR_skull.nii.gz')

    #     # Realizar segmentación basada en umbral adaptativo
    #     otsu_filter = sitk.OtsuThresholdImageFilter()
    #     otsu_filter.SetInsideValue(1)
    #     otsu_filter.SetOutsideValue(0)
    #     mascara_referencia = otsu_filter.Execute(imagen_referencia)

    #     # Aplicar la máscara a la imagen original
    #     imagen_sin_craneo = sitk.Mask(imagen_original, mascara_referencia)

    #     # Guardar la imagen sin el cráneo
    #     sitk.WriteImage(imagen_sin_craneo, 'Patient/T1_FLAIR_skull.nii.gz')
        
    #     #______________________________________PRODUCE IMAGEN ESACALADA IR PARA RETIRAR EL CRANEO___________________________________
    #     # Cargar la imagen NIfTI
    #     nifti_img = nib.load('Patient/registered_IR.nii.gz')  # Asegúrate de ajustar la ruta y el nombre del archivo

    #     # Obtener los datos de la imagen
    #     data = nifti_img.get_fdata()

    #     # Preprocesamiento opcional
    #     # data = cv2.medianBlur(data, 5)  # Ejemplo de suavizado con filtro de mediana

    #     # Definir escalas espaciales
    #     scales = [7.5]  # Escalas para aplicar filtros gaussianos

    #     # Aplicar filtros gaussianos en diferentes escalas
    #     filtered_images = []
    #     for scale in scales:
    #     # Aplicar filtro gaussiano
    #         filtered = ndimage.gaussian_filter(data, sigma=scale)
    #         filtered=k_means(filtered,2,10)
    #         # Create a new nibabel image with the extracted brain
    #         brain_extracted_image = nib.Nifti1Image(filtered, affine=nifti_img.affine, dtype=np.int16)

    #         # Save the image with the extracted brain to a new file
    #         nib.save(brain_extracted_image, 'Patient/FLAIR_skull.nii.gz')
    #         filtered_images.append(filtered)
    #     #_____________________________________RESTAR LA IMAGEN ESCALADA CON IR CON LA FLAIR ORIGINAL_________________________________________
    #     #PARA RETIRAR EL CRANEO A LA FLAIR ORIGINAL

    #     # Cargar las imágenes
    #     imagen_original = sitk.ReadImage('Patient/FLAIR.nii.gz')
    #     magen_referencia = sitk.ReadImage('Patient/FLAIR_skull.nii.gz')

    #     # Realizar segmentación basada en umbral adaptativo
    #     otsu_filter = sitk.OtsuThresholdImageFilter()
    #     otsu_filter.SetInsideValue(1)
    #     otsu_filter.SetOutsideValue(0)
    #     mascara_referencia = otsu_filter.Execute(imagen_referencia)

    #     # Aplicar la máscara a la imagen original
    #     imagen_sin_craneo = sitk.Mask(imagen_original, mascara_referencia)

    #     # Guardar la imagen sin el cráneo
    #     sitk.WriteImage(imagen_sin_craneo, 'Patient/FLAIR_original_sin_craneo.nii.gz')
    #     #_______________________CREA LA MASCARA DE LAS LESIONES DE MATERIA BLANCA EXTRALLENDOLA DE LA FLAIR________________________________
    #     #             ----------------------------------------------------------------------------------
    #     # Segmentar lesiones
    #     # ----------------------------------------------------------------------------------

    #     image = nib.load('Patient/FLAIR_original_sin_craneo.nii.gz').get_fdata()
    #     image = Median_filter_borders(image)
    #     image=k_means(image,6,15)

    #     #image = Z_score(image)
        
    #     #image = k_means(image, 4, 10)
    #     image[:,:,:13] = 0
    #     mask = image == 3
    #     mask = mask.astype(np.float32)  # Convert mask to unsigned 8-bit integer type

    #     # Create a new nibabel image with the extracted brain
    #     brain_extracted_image = nib.Nifti1Image(mask, affine=nifti_img.affine, dtype=np.int16)

    #     # Save the image with the extracted brain to a new file
    #     nib.save(brain_extracted_image, 'Patient/mask.nii.gz')
    
    #     #______________________________EXTRAE LAS MASCARAS DE LA IMAGEN T1 REGISTRADA SIN CRANEO____________________________
    #     image = nib.load('Patient/T1_FLAIR_skull.nii.gz').get_fdata()
    #     # image=k_means(image,3,10)

    #     #image = Z_score(image)
    #     #image = Median_filter(image)
    #     #image = k_means(image, 4, 10)
    #     for i in range (0,3):
    #         mask = image == i
    #         mask = mask.astype(np.float32)  # Convert mask to unsigned 8-bit integer type

    #         # Create a new nibabel image with the extracted brain
    #         brain_extracted_image = nib.Nifti1Image(mask, affine=nifti_img.affine, dtype=np.int16)

    #         # Save the image with the extracted brain to a new file
    #         nib.save(brain_extracted_image, 'Patient/'+str(i)+'_mask.nii.gz')
    #     #________________________________________JUNTAR TODAS LAS CAPAS LAS DE T1 Y LA DE LAS LESIONES DE FLAIR_________________

    #     imagenes = [ 'Patient/1_mask.nii.gz', 'Patient/2_mask.nii.gz','Patient/mask.nii.gz']
    #     nombres = ['Mask', 'Referencia', 'Imagen3', 'Imagen4']
    #     salida = 'Patient/imagen_segmentada.nii.gz'
    #     # Carga los datos de las imágenes
    #     datos_imagenes = []
    #     for imagen in imagenes:
    #         imagen_nifti = nib.load(imagen)
    #         datos_imagen = imagen_nifti.get_fdata()
    #         datos_imagen = (datos_imagen > 0).astype(np.float32)
    #         datos_imagenes.append(datos_imagen)

    #     # Etiqueta las regiones con valores únicos
    #     imagen_segmentada = np.zeros_like(datos_imagenes[0], dtype=np.float32)
    #     for i, datos_imagen in enumerate(datos_imagenes):
    #         mask = datos_imagen > 0
    #         imagen_segmentada += mask * np.float32(i + 1)

    #     # Crea una nueva imagen NIfTI a partir de la imagen segmentada
    #     imagen_segmentada_nifti = nib.Nifti1Image(imagen_segmentada, imagen_nifti.affine, header=imagen_nifti.header)

    #     # Guarda la imagen segmentada en formato NIfTI
    #     nib.save(imagen_segmentada_nifti, salida)

    #     # Cargar las imágenes
    #     imagen_original = sitk.ReadImage("Patient/imagen_segmentada.nii.gz")
    #     imagen_referencia = sitk.ReadImage( "Patient/IR_skull.nii.gz")

    #     # Modify the metadata of image2 to match image1
    #     imagen_referencia.SetOrigin(imagen_original.GetOrigin())
    #     imagen_referencia.SetSpacing(imagen_original.GetSpacing())
    #     imagen_referencia.SetDirection(imagen_original.GetDirection())

    #     # Realizar segmentación basada en umbral adaptativo
    #     otsu_filter = sitk.OtsuThresholdImageFilter()
    #     otsu_filter.SetInsideValue(1)
    #     otsu_filter.SetOutsideValue(0)
    #     mascara_referencia = otsu_filter.Execute(imagen_referencia)

    #     # Aplicar la máscara a la imagen original
    #     imagen_sin_craneo = sitk.Mask(imagen_original, mascara_referencia)

    #     # Obtener los datos de la imagen sin el cráneo
    #     # Obtener los datos de la imagen sin el cráneo
    #     data_sin_craneo = sitk.GetArrayFromImage(imagen_sin_craneo)

    #     # Obtener los datos de la máscara
    #     data_mascara = sitk.GetArrayFromImage(mascara_referencia)

    #     # Crear una máscara booleana para los valores cero dentro del cerebro
    #     mascara_cero_cerebro = (data_sin_craneo == 0) & (data_mascara != 0)

    #     # Asignar un valor distinto a los valores cero dentro del cerebro
    #     valor_distinto =  np.max(imagen_original)+2.0
    #     data_sin_craneo[mascara_cero_cerebro] = valor_distinto

    #     # Crear una nueva imagen SimpleITK con los datos modificados
    #     imagen_sin_craneo_modificada = sitk.GetImageFromArray(data_sin_craneo)
    #     imagen_sin_craneo_modificada.CopyInformation(imagen_sin_craneo)

    #     # Guardar la imagen sin el cráneo

    #     sitk.WriteImage(imagen_sin_craneo_modificada,"Patient/FLAIR_skull_lesion.nii.gz")
    # else:
    #      messagebox.showerror(message="Images must be registered in Flair format", title="ERROR")


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# # Mostrar las imágenes filtradas
# for i, filtered in enumerate(filtered_images):
#     # Seleccionar una imagen 2D de la matriz 3D
#     slice_image = filtered[:, :, 10]  # Puedes ajustar la selección del plano deseado

#     plt.figure()
#     plt.imshow(slice_image, cmap='gray')
#     plt.title(f'Filtro Escala {scales[i]}')

# plt.show()