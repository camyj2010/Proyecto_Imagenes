
import numpy as np


def k_means(image,tol,tau):
  k1 = np.amin(image)
  k2 = np.mean(image)
  k3 = np.amax(image)

  for i in range(0,3):
    d1 = np.abs(k1 - image)
    d2 = np.abs(k2 - image)
    d3 = np.abs(k3 - image)

    segmentation = np.zeros_like(image)
    segmentation[np.multiply(d1 < d2, d1 < d3)] = 0
    segmentation[np.multiply(d2 < d1, d2 < d3)] = 1
    segmentation[np.multiply(d3 < d1, d3 < d2)] = 2

    k1 = image[segmentation == 0].mean()
    k2 = image[segmentation == 1].mean()
    k3 = image[segmentation == 2].mean()
  return segmentation