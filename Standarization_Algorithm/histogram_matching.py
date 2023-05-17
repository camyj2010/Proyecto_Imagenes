import numpy as np
import nibabel as nib

def histogram_matching(reference_data, transform_data,k):
    
    reference_flat = reference_data.flatten()
    transform_flat = transform_data.flatten()
    
    reference_landmarks = np.percentile(reference_flat, np.linspace(0, 100, k))
    transform_landmarks = np.percentile(transform_flat, np.linspace(0, 100, k))

    
    piecewise_func = np.interp(transform_flat, transform_landmarks, reference_landmarks)
    transformed_data = piecewise_func.reshape(transform_data.shape)

    return transformed_data
