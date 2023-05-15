import nibabel as nib
import numpy as np

def Rescaling(image_data):
    min_value = image_data.min()
    max_value = image_data.max()

    image_data_rescaled = (image_data - min_value) / (max_value - min_value)
    return image_data_rescaled 
