from scipy.signal import find_peaks
from scipy import stats as st
import statistics as stat
import numpy as np

# Calcular el histograma
def White_stripe(image_data):
    hist, bin_edges = np.histogram(image_data.flatten(), bins=100)


    # Encontrar los picos del histograma
    picos, _ = find_peaks(hist, height=100)
    val_picos=bin_edges[picos]
    #print(val_picos[1])

    # Imagen reecalada
    image_data_rescaled=image_data/val_picos[1]
    return image_data_rescaled