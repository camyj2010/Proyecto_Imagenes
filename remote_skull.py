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

        image_data_flair_segmented = k_means(image_data_flair_without_skull, 3, 15)

        # Where the values are 3, replace them in the image_data with a value of 3
        image_data_flair_segmented[:,:,:13] = 0
        image_data_flair_segmented[:,:,40:] = 0

        lession_label=2
        image_data = np.where(image_data_flair_segmented == lession_label, 3, image_data)

          # Cambiar los labels para que queden acorde a la segmentación de Jose Bernal
        bg = image_data == 0
        grey_matter = np.logical_and(image_data > 0.95, image_data <= 1.5)
        white_matter = np.logical_and(image_data > 1.5, image_data <= 2.5)
        lessons = np.logical_and(image_data > 2.5, image_data <= 3.5)
        cfr_liquid = np.logical_or(
            np.logical_and(image_data > 3.5, image_data <= 4.5),
            np.logical_and(image_data > 0.05, image_data <= 0.95),
        )

        image_data[bg] = 0
        image_data[cfr_liquid] = 1
        image_data[grey_matter] = 2
        image_data[white_matter] = 3
        image_data[lessons] = 4

        # Ajustar un poco las segmentaciones para mejorar el volumen (A los primeros planos eliminar segmentación y así reducir error de cráneo)
        image_data[:, :, :3] = 0
        image_data[:, :, 43:] = 0


        # Ajustar un poco las segmentaciones para mejorar el volumen (A los primeros planos eliminar segmentación y así reducir error de cráneo)
        image_data[:, :, :3] = 0
        image_data[:, :, 43:] = 0

        affine = image.affine
        # Create a nibabel image object from the image data
        image = nib.Nifti1Image(image_data.astype(np.float32), affine=affine)
        # Save the image as a NIfTI file
        output_path = "Patient/FLAIR_skull_lesion.nii.gz"
        nib.save(image, output_path)

    else:
         messagebox.showerror(message="Images must be registered in Flair format", title="ERROR")
