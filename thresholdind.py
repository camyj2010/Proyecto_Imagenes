
import numpy as np


def thres(image, tol, ta):	
		tau = ta
		istrue=True
		while istrue:
			#print(tau)

			segmentation = image >= tau
			mBG = image[np.multiply(image > 10, segmentation == 0)].mean()
			mFG = image[np.multiply(image > 10, segmentation == 1)].mean()

			tau_post = 0.5 * (mBG + mFG)

			if np.abs(tau - tau_post) < tol:
				istrue=False
				return segmentation
			if (not tau_post) :
				istrue=False
				return segmentation
			else:
				tau = tau_post