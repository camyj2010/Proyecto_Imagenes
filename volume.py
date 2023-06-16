import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import SimpleITK as sitk
from Segmentation_Algorithm.kMeans import k_means
from tkinter import messagebox
def volumes(file_path):
    
    image_data_FLAIR=nib.load(file_path).get_fdata()
    result= np.where(image_data_FLAIR == 4 , 1 , 0)
    unique,counts=np.unique(image_data_FLAIR, return_counts=True)
    print(counts)
    count= np.count_nonzero(image_data_FLAIR.astype(np.int32) == 2)
    print("Cantidad de elementos iguala a 1:", count)
    return counts