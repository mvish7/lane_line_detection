# **Finding Lane Lines on the Road**

This project is based on Udacity's Self Driving car Nanodegree

### 1. Describe your pipeline. As part of the description.

My pipeline consisted of 5 steps:

1. Convert the image to grayscale and apply a Gaussian blur.  For the parameters, I used `kernel_size = (5, 5)`.
![alt text](./output_images/Figure_2.png?raw=true)

2. Apply Canny edge detection.  In line with the recommended 3:1 ratio of thresholds, I used `low_threshold = 40` 
and `  high_threshold = 120`.

![alt text](./output_images/Figure_3.png?raw=true)

3. Apply a mask to the image outputted by Canny image detection.  I applied a simple mask of trapezoid shape. 
![alt text](./output_images/Figure_4.png?raw=true)

4. Apply the Hough Transform to the masked image from step 3. 

5. Process and filter the lines found by the Hough Transform.
![alt text](./output_images/Figure_5.png?raw=true)

Steps 4 and 5 were performed in an iterative fashion. The Hough Transform parameters were initialized. Since the output of the Hough Transform is a potential candidates  named `lines`, I extended these lines to the top and bottom of the masked image region. The lines were also sorted as per their length. I created a virtual zone for acceptable *x* coordinates of the endpoints of the line, and I removed entries in the `lines` list whose endpoints fell outside these intervals.  I declared the longest line in `lines` to be one of the two lane lines, and for the other I took the longest remaining line whose slope was of the opposite sign as that of `lines[0]`.

If this process did not yield two lines, then I altered the parameters for hough transform and repeated steps 4 and 5.



### 2. Identify potential shortcomings with your current pipeline

This is a simple lane detection pipeline, and as such it has a number of potential shortcomings.

* First, since we are fitting lines (not curves) to the lane lines, this pipeline may yield poor results on urban roads with sharp turns. 
* Second, it may struggle when there are signs in the road, such as arrows etc. 
* This pipeline may not be robust to different lighting.



### 3. Suggest possible improvements to your pipeline

To more accurately detect the lane lines, it would be beneficial to fit a Clothoid curve curve to the lanes, instead of fitting a line.
