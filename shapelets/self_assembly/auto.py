########################################################################################################################
# Copyright 2023 the authors (see AUTHORS file for full list).                                                         #
#                                                                                                                      #
# This file is part of shapelets.                                                                                      #
#                                                                                                                      #
# Shapelets is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General       #
# Public License as published by the Free Software Foundation, either version 2.1 of the License, or (at your option)  #
# any later version.                                                                                                   #
#                                                                                                                      #
# Shapelets is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied      #
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more  #
# details.                                                                                                             #
#                                                                                                                      #
# You should have received a copy of the GNU Lesser General Public License along with shapelets. If not, see           #
# <https://www.gnu.org/licenses/>.                                                                                     #
########################################################################################################################

import numpy as np
import os
from pathlib import Path
from pickle import Unpickler
from PIL import Image
from time import time

from scipy.signal import fftconvolve
from skimage.filters import threshold_otsu
from sklearn.neural_network import MLPRegressor
import tensorflow as tf

from .convolution import convresponse_n0
from .misc import read_image
from .quant import rdistance
from .wavelength import get_wavelength


def infer(RVs: np.ndarray) -> str:
    r"""
    This function performs pattern inference using a trained CNN model to predict the pattern present in image.
    The shapelets response vectors are otsu thresholded and resized to 256x256 prior to inference.

    Parameters
    ----------
    * RVs: np.ndarray
        Response vectors of channels m = [2, 3, 6].

    Returns
    -------
    * predicted_class: str
        Predicted class name (i.e. 'hex', 'stripe', 'neither')

    Notes
    -----
    TODO: Need to reference paper.

    """
    if not isinstance(RVs, np.ndarray):
        raise ValueError("RVs must be a numpy array")
    if RVs.shape[2] != 3:
        raise ValueError("RVs must have 3 channels")
    if np.min(RVs) < 0 or np.max(RVs) > 1:
        raise ValueError("RVs must be normalized to [0, 1]")

    # Load the best model from train.py
    model_path = r"./self_assembly/models/CNN.h5"
    model = tf.keras.models.load_model(model_path)

    # Apply Otsu thresholding to each channel
    for i in range(3):
        threshold = threshold_otsu(RVs[:, :, i])
        RVs[:, :, i] = np.where(RVs[:, :, i] > threshold, RVs[:, :, i], 0)

    # Resize to 256x256 and convert to float32
    RVs = np.expand_dims(np.array(Image.fromarray((RVs * 255).astype(np.uint8)).resize((256, 256))), axis=0).astype(np.float32)

    # Predict the class index
    predicted_class_index = model(RVs)
    predicted_class_index = np.argmax(predicted_class_index, axis=1)

    # Convert index to class name
    if predicted_class_index == 0:
        predicted_class = "hex"
    elif predicted_class_index == 2:
        predicted_class = "stripe"
    else:
        predicted_class = "neither"

    return predicted_class


def find_reference_region(img, threshold: int = -1, stride: int = 1):
    r"""
    This function performs a convolution operation on the input image to find an ideal reference region based on the minimum sum of the output of several convolutions.

    Parameters
    ----------
    * img: np.ndarray
        Input image
    * threshold : int, optional
        If non-zero number, return information for all possible tiles after applying the stride and taking that top % of the ideal boxes. Default is -1 so no thresholding applied, only returns best box
    * stride: int, optional
        Stride value for selecting stride-separated boxes. Default is 25, should be some number relative to the window_size such as window_size//2 or window_size//4

    Returns
    -------
    * best_box: tuple[tuple[int, int], tuple[int, int]]
        Coordinates of the top-left and bottom-right corners of the ideal box
    * top_left_coords: list[tuple[int, int], ...]
        List of top-left coordinates for each tile (if all_tiles is True).
    * box_sums: list[int]
        - List of sums for each tile (if all_tiles is True).

    Notes
    -----
    TODO: Need to reference paper.

    """
    if not isinstance(img, np.ndarray):
        raise ValueError("img must be a numpy array")
    if img.ndim != 2:
        raise ValueError("img must be a 2D array")
    if np.min(img) < 0 or np.max(img) > 1:
        raise ValueError("img must be normalized to [0, 1]")
    if not (threshold == -1 or (threshold > 0 and threshold < 100)):
        raise ValueError("threshold must be -1 or a number between 0 and 100")
    if not isinstance(stride, int) or stride < 1:
        raise ValueError("stride must be a positive integer")

    # Window size set to 2.5x, where x is characteristic wavelength
    char_wavelength = get_wavelength(image=img, verbose=False)
    window_size = int(char_wavelength * 2.5)

    kernel = np.ones((window_size, window_size), dtype=np.float32)
    convolved_img = fftconvolve(img.astype(np.float32), kernel, mode="valid")

    # Find the location of the minimum sum in the convolved image down to the pixel before stride
    min_sum_idx = np.unravel_index(np.argmin(convolved_img), convolved_img.shape)

    # Calculate the coordinates of the ideal box based on the minimum sum location and stride
    x_start, y_start = min_sum_idx[1], min_sum_idx[0]
    x_end, y_end = x_start + window_size - 1, y_start + window_size - 1
    best_box = ((x_start, y_start), (x_end, y_end))

    # Take only stride-separated boxes
    if stride != 1:
        convolved_img = convolved_img[::stride, ::stride]

    # If multiple regions are to be returned (thresholding mode)
    if threshold != -1:
        # Generate an array of top-left coordinates and their respective sums for each kernel position after stride is applied
        top_left_coords = []
        box_sums = []
        for i in range(convolved_img.shape[0]):
            for j in range(convolved_img.shape[1]):
                box_sum = np.sum(img[i * stride : i * stride + window_size, j * stride : j * stride + window_size])
                box_sums.append(box_sum)
                top_left_coords.append((j * stride, i * stride))

        keep_boxes = []
        keep_sums = []
        sorted_sums = sorted(box_sums)[: int((100 - threshold) / 100 * len(box_sums))]
        for i in range(len(box_sums)):
            if box_sums[i] in sorted_sums:
                keep_boxes.append(top_left_coords[i])
                keep_sums.append(box_sums[i])
        top_left_coords = keep_boxes
        box_sums = keep_sums

        # Return the coordinates of the ideal box, window size, min sum value, and top-left coordinates array
        return best_box, top_left_coords, box_sums

    else:
        return best_box


def predict(pattern_type: str, RVs: np.ndarray, model_path: str):
    r"""
    This function loads a trained MLPRegressor model based on the pattern type and predicts the response distance at each pixel.
    This generates a response distance image that can be used to approximate the response distance method.

    Parameters
    ----------
    * pattern_type : str
        Type of pattern ('hex' or 'stripe') for selecting the appropriate trained model
    * RVs : np.ndarray
        Response vectors
    * model_path : str
        Directory path for the CNN prediction model

    Returns
    -------
    * ideal_box_data: tuple[tuple[int, int], tuple[int, int]]
        Coordinates of the top-left and bottom-right corners of the ideal box and the top_left coords and sums if threshold flag enabled
    * prediction: np.ndarray
        Predicted image's response distance
    * response: np.ndarray
        Shapelet response vectors
    * window_size: int
        Window size determined for reference region bounding box

    Notes
    -----
    TODO: Need to reference paper.

    """
    if not (pattern_type in ["hex", "stripe"]):
        raise ValueError("pattern_type must be 'hex' or 'stripe'")
    if not isinstance(RVs, np.ndarray):
        raise ValueError("RVs must be a numpy array")
    if RVs.shape[2] != 29:
        raise ValueError("RVs must have 29 channels")
    if not isinstance(model_path, str):
        raise ValueError("model_path must be a string")
    if not os.path.exists(model_path):
        raise ValueError("model_path must be a valid file path")

    if pattern_type in ["hex", "stripe"]:
        with open(model_path, "rb") as f:
            regressor = Unpickler(f).load()
    else:
        raise ValueError('pattern_type parameter should be either "hex" or "stripe".')

    # Predict response distance at each pixel then reshape all estimated pixels to image shape
    prediction = regressor.predict(RVs.reshape(-1, 29)).reshape(RVs.shape[:2])

    return prediction


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    # TODO: this test script will be re-organized into a separate method consistent with entry points for shapelets package.

    model = MLPRegressor()

    # file path - ***this assumes you're running it from the 'paper' subdirectory
    dir_path = Path(__file__).parents[1] / "paper" / "cropped"  # / "all"
    save_path = Path(__file__).parents[1] / "paper" / "kmeansData"

    origin = time()
    neither = 0

    hex_correct = 0
    hex_incorrect = 0
    stripe_correct = 0
    stripe_incorrect = 0
    other = 0

    pred_times = []
    RPA_times = []
    rd_times = []
    tot_times = []

    dir = os.listdir(dir_path)
    for file in dir:

        ################################################################################################
        # LOAD IMAGE AND INFERE PATTERN TYPE WITH CNN
        ################################################################################################
        starttime = time()
        file_path = os.path.join(dir_path, file)

        # Load image as PIL image object
        image = read_image(file, dir_path, verbose=False)

        # Compute 29th order shapelets and flatten to pass each pixel through regressor
        shapelet_order = 29
        RVs = convresponse_n0(image=image, shapelet_order=shapelet_order, verbose=False)[0]

        # Get predicted pattern type from CNN inference
        pattern_type = infer(RVs[:, :, [1, 2, 5]])
        print(f"Pattern type: {pattern_type}")

        # check pattern type
        if "hex" in file:
            if pattern_type == "hex":
                hex_correct += 1
            else:
                hex_incorrect += 1
                print(f"hex incorrect: {file}")
        elif "stripe" in file:
            if pattern_type == "stripe":
                stripe_correct += 1
            else:
                stripe_incorrect += 1
                print(f"stripe incorrect: {file}")

        if pattern_type == "neither":
            neither += 1

        else:

            ################################################################################################
            # RUN PREDICTOR AND REGION PROPOSAL ALGORITHM
            ################################################################################################

            # Split the selected filepath into the filename+ext and the rest of the path
            dir_path, filename = os.path.split(file_path)
            # Use predicted pattern type and filepath to get predicted response distance and ideal reference region location
            model_path = os.path.join(Path(__file__).parents[0], f"MLPRegressor-{pattern_type}-denoising-std0.05.pickle")
            prediction = predict(pattern_type, RVs, model_path)
            pred_time = time() - starttime
            print(f"Pred Time: {pred_time}")
            pred_times.append(pred_time)

            start = time()
            # Determine the ideal box
            ideal_data = find_reference_region(prediction, threshold=-1)
            print(f"RPA Time: {time()-start}")
            RPA_times.append(time() - start)
            start = time()

            ################################################################################################
            # RUN REAL SHAPELETS RESPONSE DISTANCE METHOD
            ################################################################################################

            # paper code: for testing:

            # Take the ideal_data from the predictor and split into seperate coords
            top_left, bottom_right = ideal_data[0], ideal_data[1]
            # Apply K-means response distance method on the image using the predicted reference region
            rdist = rdistance(
                image=image,
                num_clusters=20,
                ux=[top_left[0], bottom_right[0]],
                uy=[top_left[1], bottom_right[1]],
                verbose=False,
            )

            # normalize for visualization purposes as done in shapelets.self_assembly.misc.process_output()
            rdist = (rdist - rdist.min()) / (rdist.max() - rdist.min())

            rd_time = time() - start
            print(f"RD Time: {rd_time}")
            rd_times.append(rd_time)
            tot_time = time() - starttime
            print(f"Total Prediction Time: {tot_time}s")
            tot_times.append(tot_time)

            ################################################################################################
            # PLOTTING
            ################################################################################################

            # TODO: should probably put this in a function to process output from this method

            imgs = [image, prediction, rdist]
            lamb = int(get_wavelength(image, verbose=False))
            window_size = int(2.5 * lamb)
            names = [f"Lambda-{lamb}\npredicted-{pattern_type}", f"MLP_RD", "Kmeans_RD"]

            fig, axes = plt.subplots(1, 3)
            for i in range(len(imgs)):
                # Plot each image in a subplot
                axes[i].imshow(1 - imgs[i], cmap="gray")
                axes[i].set_title(names[i])
                # axes[i].axis('off')  # Turn off axis
                axes[i].add_patch(Rectangle(top_left, width=window_size, height=window_size, linewidth=1, edgecolor="g", facecolor="none"))

            # Display the images
            plt.tight_layout()
            fig.savefig(os.path.join(save_path, file), dpi=300)
            plt.close()

    # TODO Reporting, not sure what is needed for verbose portion when running method. leave all for now

    print(f"ALL TIME: {time()-origin}s")
    print(f"Pred Avg: {sum(pred_times)/len(pred_times)}s")
    print(f"RPA Avg: {sum(RPA_times)/len(RPA_times)}s")
    print(f"Kmeans Avg: {sum(rd_times)/len(rd_times)}s")
    print(f"Hex correct: {hex_correct}")
    print(f"Hex incorrect: {hex_incorrect}")
    print(f"Stripe correct: {stripe_correct}")
    print(f"Stripe incorrect: {stripe_incorrect}")
    print(f"Accuracy: {100*(hex_correct+stripe_correct)/(hex_correct+stripe_correct+hex_incorrect+stripe_incorrect)}")
    print(f"NEITHERS: {neither}")
