import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
from process_image import ProcessImage
from line_helper import extend_to_bottom_top, get_slope, intersection_or_ymax


def pre_process_image(img_path):

    process_img = ProcessImage(img_path)

    image = process_img.read_image()
    plt.imshow(image)
    process_img.apply_gaussian_blur((5, 5))
    edges = process_img.apply_canny_edge_detection(40, 120)
    plt.imshow(edges)
    maksed_img = process_img.apply_mask_to_img()
    plt.imshow(maksed_img)
    return image, edges, maksed_img


def detect_lines(image, edges, masked_img):

    # Define the Hough transform parameters

    rows, cols = masked_img.shape

    # parameters for filtering lines
    left = 0.12 * cols
    right = 0.94 * cols
    top = 0.55 * rows

    left_min = left
    left_max = 0.2 * cols
    right_min = 0.86 * cols
    right_max = right

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid

    threshold = 20  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 200  # minimum number of pixels making up a line
    max_line_gap = 100  # maximum gap in pixels between connectable line segments

    good_lines = []

    # fine tune Hough transform parameters until we get best line pair
    while len(good_lines) != 2 and threshold > 0:

        # apply the Hough Transform on the ``masked_edges`` image

        lines = cv2.HoughLinesP(masked_img, rho, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)

        # process and filter the lines found by the Hough transform
        # sort the lines by their length
        lines = sorted(lines, key=lambda x: np.linalg.norm(x[2:] - x[:2]), reverse=True)

        # extend the lines to the bottom and top of the masked image
        lines = [extend_to_bottom_top(line, rows, top) for line in lines]

        # filter out lines based on their x-coordinates at the bottom and top of the masked image
        lines = [line for line in lines
                 if ((left_min <= line[0][0] <= left_max or right_min <= line[0][0] <= right_max) and
                     0.4 * cols <= line[0][2] <= 0.7 * cols)]

        # if we have more than 1 line, try to choose two lines
        if len(lines) > 1:
            # the first line is the longest line ==> calculate its slope
            m0 = get_slope(lines[0])

            # the second line is the longest line with opposite slope of the first line
            for line in lines:
                m1 = get_slope(line)
                if np.sign(m1) != np.sign(m0):
                    # remove "bad" entries in ``lines``
                    good_lines = [lines[0], line]

                    # get the top endpoints of the lines
                    xy0, xy1 = intersection_or_ymax(good_lines[0], good_lines[1], top)
                    good_lines[0][0][2:] = xy0
                    good_lines[1][0][2:] = xy1
                    break

        # if we didn't find two good lines, then cut the Hough parameters in half and repeat
        threshold //= 2
        min_line_length /= 2
        max_line_gap /= 2

    # Iterate over the output "lines" and draw lines on a blank image
    line_image = np.copy(image) * 0  # creating a blank to draw lines on
    for line in good_lines:
        for x1, y1, x2, y2 in line.astype(np.uint16):
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)

    # Create a "color" binary image to combine with line image
    color_edges = np.dstack((edges, edges, edges))

    # Draw the lines on the edge image
    lines_edges = cv2.addWeighted(image, 0.8, line_image, 1, 0)

    return lines_edges


def main():
    img_path = 'test_images/solidWhiteRight.jpg'
    image, edges, masked_img = pre_process_image(img_path)
    lane_lines = detect_lines(image, edges, masked_img)
    plt.imshow(lane_lines)


if __name__ == "__main__":
    main()
