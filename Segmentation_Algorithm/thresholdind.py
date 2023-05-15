
import numpy as np


def thres(image, tol, ta):	
		

    # print ("se pudo")
    #plt.imshow(self.image_data[:, :, 100])

    while True:
            #print(tau)

        segmentationr = image >= ta
        mBG = image[np.multiply(image > 10, segmentationr == 0)].mean()
        mFG = image[np.multiply(image > 10, segmentationr == 1)].mean()

        tau_post = 0.5 * (mBG + mFG)

        if np.abs(ta - tau_post) < tol:
            break
        else:
            ta = tau_post
    # print(ta)
    # print(segmentationr.shape)
    return segmentationr