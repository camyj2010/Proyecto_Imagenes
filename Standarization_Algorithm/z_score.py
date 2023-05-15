import nibabel as nib
import numpy as np

def Z_score(image_data):
    mean_value = image_data[image_data > 10].mean()
    standard_deviation_value = image_data[image_data > 10].std()

    # print(mean_value)
    # print(standard_deviation_value)

    image_data_rescaled = (image_data - mean_value) / (standard_deviation_value)
    return image_data_rescaled