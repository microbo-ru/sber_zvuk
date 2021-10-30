# coding: utf-8

from __future__ import annotations
import cv2


class BlurFrame:
    def __init__(self, frame, corner_points: list):
        """
        This function requires a frame and the corner_points for applying blur
        :param frame: the image input
        :param corner_points: points will be the array of bottom left and top right points\
        each index of corner_points contains an array of two sets, each set represents a point\
        the first set will represent the corner_1 i.e lower left corner\
        the second set will represent the corner_2 i.e. upper right corner
        """
        self.frame = frame
        self.corner_points = corner_points

    def blur_frame(self) -> BlurFrame:
        """
        This function will apply bur on images, the functionality is really simple it will take the corners and will\
        draw a rectangular blur on specific area, looping through all the points.
        :return: image with blurred regions.
        """
        for i in range(len(self.corner_points)):
            bottom_left = self.corner_points[i][1]  # corner_1
            top_right = self.corner_points[i][0]  # corner_2

            x, y = top_right[0], top_right[1]
            w, h = top_right[0] - bottom_left[0], bottom_left[1] - top_right[1]

            # Grab ROI with Numpy slicing and blur
            roi = self.frame[y:y + h, x - w:x]
            blur = cv2.GaussianBlur(roi, (51, 51), 0)

            # Insert ROI back into image
            self.frame[y:y + h, x - w:x] = blur
        return self.frame
