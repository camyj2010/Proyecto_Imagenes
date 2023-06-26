import SimpleITK as sitk
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import os


def register_algorithm(fixed_image_path, moving_image_path,moving_seg_image_path):
        print("hola1")
        # Load fixed and moving images
        # Obtener la ruta absoluta del archivo
        ruta_absolutafixed_image = os.path.abspath(fixed_image_path)
        print(fixed_image_path)
        fixed_image = sitk.ReadImage(ruta_absolutafixed_image)
        moving_image = sitk.ReadImage(moving_image_path)
        moving_seg_image=sitk.ReadImage(moving_seg_image_path)
        print("hola11")
        # Convert image types
        fixed_image = sitk.Cast(fixed_image, sitk.sitkFloat32)
        moving_image = sitk.Cast(moving_image, sitk.sitkFloat32)
        moving_seg_image= sitk.Cast(moving_seg_image, sitk.sitkFloat32)
        # Define the registration components
        registration_method = sitk.ImageRegistrationMethod()

        # Similarity metric - Mutual Information
        registration_method.SetMetricAsMattesMutualInformation()
        print("hola111")
        # Interpolator
        registration_method.SetInterpolator(sitk.sitkNearestNeighbor)

        # Optimizer - Gradient Descent
        registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100,
                                                     estimateLearningRate=registration_method.EachIteration)
        print("hola1111")
        # Initial transform - Identity
        initial_transform = sitk.Transform()
        registration_method.SetInitialTransform(initial_transform)

        # Setup for the registration process
        registration_method.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
        registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
        registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()
        print("hola11111")
        # Perform registration
        final_transform = registration_method.Execute(fixed_image, moving_seg_image)
        print("hola2")
        # Resample the moving image to match the fixed image dimensions and orientation
        reference_image = fixed_image
        interpolator = sitk.sitkNearestNeighbor
        default_pixel_value = 0.0
        resampled_image = sitk.Resample( moving_image,reference_image, final_transform,
                                    interpolator, default_pixel_value)

        # Convert the resampled image to Numpy array
        resampled_array = sitk.GetArrayFromImage(resampled_image)

        # Save the resampled image as NIfTI
        output_image_path = 'Patient/Registered_FLAIR.nii.gz'
        sitk.WriteImage(resampled_image, output_image_path)
        print("hola3")
        return output_image_path