import numpy as np
import nibabel as nib

def histogram_matching(reference_data, transform_data,k):
    # Reshape the data arrays to 1D arrays
    reference_flat = reference_data.flatten()
    transform_flat = transform_data.flatten()

    # Identify k landmarks (percentiles) on the reference and transform data
    
    reference_landmarks = np.percentile(reference_flat, np.linspace(0, 100, k))
    transform_landmarks = np.percentile(transform_flat, np.linspace(0, 100, k))

    # Generate a piece-wise function with the reference landmarks
    piecewise_func = np.interp(transform_flat, transform_landmarks, reference_landmarks)

    # Map the intensities of the transform image according to the piece-wise function
    transformed_data = piecewise_func.reshape(transform_data.shape)

    return transformed_data
