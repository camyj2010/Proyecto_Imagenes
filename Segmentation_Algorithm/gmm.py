import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def gaussianMixture(image_data):
    # Each component has a weight (wi), a mean (mui), and a standard deviation (sdi)
    w1 = 1/3
    w2 = 1/3
    w3 = 1/3
    mu1 = 0
    sd1 = 50
    mu2 = 100
    sd2 = 50
    mu3 = 150
    sd3 = 50

    seg = np.zeros_like(image_data)
    for iter in range(1, 5) :

        # Compute likelihood of belonging to a cluster
        p1 = 1/np.sqrt(2*np.pi*sd1**2) * np.exp(-0.5*np.power(image_data - mu1, 2) / sd1**2)
        p2 = 1/np.sqrt(2*np.pi*sd2**2) * np.exp(-0.5*np.power(image_data - mu2, 2) / sd2**2)
        p3 = 1/np.sqrt(2*np.pi*sd3**2) * np.exp(-0.5*np.power(image_data - mu3, 2) / sd3**2)

        # Normalise probability
        r1 = np.divide(w1 * p1, w1 * p1 + w2 * p2 + w3 * p3)
        r2 = np.divide(w2 * p2, w1 * p1 + w2 * p2 + w3 * p3) 
        r3 = np.divide(w3 * p3, w1 * p1 + w2 * p2 + w3 * p3) 

        # Update parameters
        w1 = r1.mean()
        w2 = r2.mean()
        w3 = r3.mean()
        mu1 = np.multiply(r1, image_data).sum() / r1.sum()
        sd1 = np.sqrt(np.multiply(r1, np.power(image_data - mu1, 2)).sum() / r1.sum())
        mu2 = np.multiply(r2, image_data).sum() / r2.sum()
        sd2 = np.sqrt(np.multiply(r2, np.power(image_data - mu2, 2)).sum() / r2.sum())
        mu3 = np.multiply(r3, image_data).sum() / r3.sum()
        sd3 = np.sqrt(np.multiply(r3, np.power(image_data - mu3, 2)).sum() / r3.sum())

    # Perform segmentation
    seg[np.multiply(r1 > r2, r1 > r3)] = 0
    seg[np.multiply(r2 > r1, r2 > r3)] = 1
    seg[np.multiply(r3 > r1, r3 > r2)] = 2
    return seg