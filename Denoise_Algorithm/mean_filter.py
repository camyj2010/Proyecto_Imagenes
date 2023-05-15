
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
# Mean Filter
def Mean_Filter(image_data):
    #print("booooooooooooooo")
    filtered_image_data = np.zeros_like(image_data)
    for x in range(1, image_data.shape[0]-2) :
        for y in range(1, image_data.shape[1]-2) :
            for z in range(1, image_data.shape[2]-2) :
                avg = 0
                for dx in range(-1, 1) :
                    for dy in range(-1, 1) :
                        for dz in range(-1, 1) :
                            avg = avg + image_data[x+dx, y+dy, z+dz]

                filtered_image_data[x+1, y+1, z+1] = avg / 27
    return filtered_image_data