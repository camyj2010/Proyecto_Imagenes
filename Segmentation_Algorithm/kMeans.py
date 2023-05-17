
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
