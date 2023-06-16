
import numpy as np


def k_means(image, k,iterations):
    # Initialize the centroids
    centroids = np.linspace(np.amin(image), np.amax(image), num=k)
    
    for i in range(iterations):
        # Compute the distances from each point to each centroid
        distances = np.abs(image[..., np.newaxis] - centroids)
        
        # Assign each point to the closest centroid
        segmentation = np.argmin(distances, axis=-1)
        
        # Update the centroids
        for group in range(k):
            centroids[group] = image[segmentation == group].mean()
    
    return segmentation
# def k_means(image, ks,iteracion):
        
#         # Inicialización de valores k
#         k_values = np.linspace(np.amin(image), np.amax(image), ks)
#         for i in range(iteracion):
#             d_values = [np.abs(k - image) for k in k_values]
#             segmentationr = np.argmin(d_values, axis=0)

#             for k_idx in range(ks):
#                 k_values[k_idx] = np.mean(image[segmentationr == k_idx])

#         return segmentationr


