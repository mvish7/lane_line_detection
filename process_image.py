import cv2
import numpy as np
import matplotlib.pyplot as plt

class ProcessImage():

    def __init__(self, image_path):
        self.test_img_filename = image_path

    def read_image(self):
        """
        reads and converts the image to gray
        :return:
        """
        image = cv2.imread(self.test_img_filename)
        self.gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def apply_gaussian_blur(self, kernel_size):
        """
        applies gaussian blur
        :param kernel_size: tuple denoting kernel size
        :return:
        """

        self.blur_gray = cv2.GaussianBlur(self.gray_img, kernel_size, 0)
        plt.imshow(self.blur_gray)

    def apply_canny_edge_detection(self, low_threshold, high_threshold):
        """
        applies canny edge detector
        :param low_threshold:
        :param high_threshold:
        :return:
        """

        self.edge_img = cv2.Canny(self.blur_gray, low_threshold, high_threshold)
        return self.edge_img

    def apply_mask_to_img(self):
        """
        applies mask to edge detected image
        :return:
        """

        rows, cols = self.edge_img.shape

        # parameters for the image mask and for filtering lines
        left = 0.12 * cols
        right = 0.94 * cols
        top = 0.55 * rows
        top_width = 0.05 * cols

        # a mask to be applied to the image
        top_left = (left + right - top_width) / 2
        top_right = (left + right + top_width) / 2
        vertices = np.array([[(left, rows), (top_left, top), (top_right, top), (right, rows)]],
                            dtype=np.int32)

        masked_edges = self.region_of_interest(vertices)
        return masked_edges

    def region_of_interest(self, vertices):
        """
        Applies an image mask. function was provided in udacity clasroom

        Only keeps the region of the image defined by the polygon
        formed from `vertices`. The rest of the image is set to black.
        """
        # defining a blank mask to start with
        mask = np.zeros_like(self.edge_img)

        # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
        if len(self.edge_img.shape) > 2:
            channel_count = self.edge_img.shape[2]  # i.e. 3 or 4 depending on your image
            ignore_mask_color = (255,) * channel_count
        else:
            ignore_mask_color = 255

        # filling pixels inside the polygon defined by "vertices" with the fill color
        cv2.fillPoly(mask, vertices, ignore_mask_color)

        # returning the image only where mask pixels are nonzero
        masked_image = cv2.bitwise_and(self.edge_img, mask)
        return masked_image

