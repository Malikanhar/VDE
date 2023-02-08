# Vibrio Detection and Estimation
## Goals
- To count the total number of Vibrio in different color
- To estimate the size of each Vibrio

## Solution
The first thing that I do is exploring the data and find the most suitable approach to solve the problem. The problem is clear enough, that I need to localize the Vibrio from an image and identify the color of it. As far as I see, Vibrio has a circle-like shape with green or yellow color. With this assumption, I can use a shape descriptor and color descriptor to localize the Vibrio. Since there is only 20 samples of Vibrio image and the data is not annotated yet, the best approach is to use a traditional image processing to explore the shape and color of Vibrio.

### Shape Descriptor
I'm using OpenCV's `HoughCircles` method to detect a circle in an image. There are several parameters that I can fine tune to get the best performance of my circle detection such as `minDist`, `minRadius`, and `maxRadius`. And here's what I got after fine tuning those parameters.

<center><img src="https://github.com/Malikanhar/VDE/raw/main/assets/shape_descriptor_out_1.jpg" width="250"></center>

The OpenCV's `HoughCircles` shape descriptor managed to detect some Vibrio, but it's produce a high false negative as it can only detect 6 out of 30 Vibrio, and when I tried it on different images, it also producing some false positive.

<center><img src="https://github.com/Malikanhar/VDE/raw/main/assets/shape_descriptor_out_2.jpg" width="250"></center>

This method is not robust for Vibrio detection / localization, as if I change the parameters, it can detect more false positives.

### Color Descriptor
An image can be seen from a multiple perspective of color space, there are RGB, HSV, and CMYK color space. An RGB image is images that we see the most, but for image processing, HSV colorspace is more favorable because it contain more information like Hue, Saturation, and Brightness of a color in an image.

<center><img src="https://github.com/Malikanhar/VDE/raw/main/assets/hsv_image.png" width="300"></center>

As we can see on the above image, Vibrio is more visible in HSV color space. So, instead of using RGB image, I'm using HSV color space to explore the Vibrio images. And here what I got by converting the Vibrio image into HSV color space and visualizing each channel of the HSV image.

<center><img src="https://github.com/Malikanhar/VDE/raw/main/assets/hue_image.png" width="300"></center>

The first channel is Hue, this channel represents the color being displayed like red-green-blue scale.

<center><img src="https://github.com/Malikanhar/VDE/raw/main/assets/saturation_image.png" width="300"></center>

The second channel is Saturation, this channel represents the purity of a color being displayed. The higher saturation, it will be more sharper and purer. As saturation decreases, colors appear more washed-out or faded.

<center><img src="https://github.com/Malikanhar/VDE/raw/main/assets/value_image.png" width="300"></center>

The last channel is Value or brightness, this channel represents the brightness of a color. This is can be affected by the lighting condition, as if the image get more light it will have higher Value.

To get more information about the range value of each channel (H, S, V), the next thing that I do is visualizing the color distribution of all Vibrios. But I need to crop all Vibrio sample first before getting its color distribution. To achieve this, I'm using [labelImg](https://github.com/heartexlabs/labelImg) annotation tool to annotate all Vibrios in an image, and after then cropping all vibrio objects by using this [notebook](https://github.com/Malikanhar/VDE/blob/main/notebook/Vibrio%20-%20Color%20Distribution.ipynb).

And here's what I got by visualizing the histogram of all Yellow-Vibrios in each HSV color space.

1. <span style="color:yellow"><b>Yellow Vibrio</b></span>

    ![hue_histogram_yellow_vibrio.png](https://github.com/Malikanhar/VDE/raw/main/assets/hue_histogram_yellow_vibrio.png)

    The `Hue` channel has a value range from 10 to 30.

    ![saturation_histogram_yellow_vibrio](https://github.com/Malikanhar/VDE/raw/main/assets/saturation_histogram_yellow_vibrio.png)

    The `Saturation` channel has a value range from 5 to 250.

    ![value_histogram_yellow_vibrio](https://github.com/Malikanhar/VDE/raw/main/assets/value_histogram_yellow_vibrio.png)

    And the `Value` channel has a value range from 75 to 255.

2. <span style="color:green"><b>Green Vibrio</b></span>

    ![hue_histogram_green_vibrio.png](https://github.com/Malikanhar/VDE/raw/main/assets/hue_histogram_green_vibrio.png)

    The `Hue` channel has a value range from 15 to 105.

    ![saturation_histogram_green_vibrio](https://github.com/Malikanhar/VDE/raw/main/assets/saturation_histogram_green_vibrio.png)

    The `Saturation` channel has a value range from 0 to 45.

    ![value_histogram_green_vibrio](https://github.com/Malikanhar/VDE/raw/main/assets/value_histogram_green_vibrio.png)

    And the `Value` channel has a value range from 50 to 255.

#### Conclusion
The Yellow-Vibrio has a HSV range from [10, 5, 75] to [30, 250, 255], and the Green-Vibrio has a HSV range from [15, 0, 50] to [105, 45, 255]. The next step is, I'm going to explore more this value to localize the yellow and green Vibrio.

### Localize the Vibrio using HSV color filtering
To localize the Vibrio, I need to remove all colors other tha vibrio. I'm going to work on Yellow-Vibrio first, and the Green-Vibrio later. As from the previous step, I know that the yellow vibrio has a HSV range from [10, 5, 75] to [30, 250, 255], so that I'm doing a hyper-parameter tuning to find the best value for filtering out non-vibrio color. After some trials and errors, I got a lower and upper HSV value of [15, 120, 110] and [36, 255, 255]. And here's an example after filtering process.

![masked_image](https://github.com/Malikanhar/VDE/raw/main/assets/masked_image.png)

As we can see that there are some noises on the masked image. In order to remove those noises, I'm using an erosion process and here's the result.

![masked_image_erosion](https://github.com/Malikanhar/VDE/raw/main/assets/masked_image_erosion.png)

After the erosion process the Vibrio size is shrinking, so that I'm using dilation process to restore the Vibrio size. Here's the result.

![masked_image_dilation](https://github.com/Malikanhar/VDE/raw/main/assets/masked_image_dilation.png)

Now the noise is reduced and the size of all Vibrios are restored. We have a pretty clear masked image of Vibrio now. The next step is to get all Vibrio from this masked image. One way to do this is by using OpenCV's `findContours`. Finally to eliminate the outliers, I'm filtering out the contour `ratio` that outside of `0.5` to `1.5` range.

Here's the detection results of my solution. This step is done with this [notebook](https://github.com/Malikanhar/VDE/blob/main/notebook/Vibrio%20-%20Color%20Filtering.ipynb)

![detection_contour](https://github.com/Malikanhar/VDE/raw/main/assets/detection_contour.png)

Lastly, to estimate the Vibrio size / diameter, I'm using a simple relativity concept. Given the size of the cup, I can calculate the milimeter per-pixel (`mmpp`), and I can use it to calculate the size (in milimeter) of a Vibrio (from given Vibrio size in pixel).