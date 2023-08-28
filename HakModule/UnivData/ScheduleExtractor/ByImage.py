"""
Currently a Work-in-Progress (WIP) due to lower recognition accuracy.
Pausing for improvements.
"""
# TODO: Address the low recognition accuracy issue and improve the text extraction process.
from colorthief import ColorThief
from collections import namedtuple
import pytesseract
import cv2
import numpy as np
import os

import pprint

ImageBox2D = namedtuple('ImageBox2D', ['x', 'y', 'w', 'h'])
ColorRGB = namedtuple('ColorRGB', ['r', 'g', 'b'])


def filter_colors(colors: list[ColorRGB], limit: int = 50) -> list[ColorRGB]:
    """
    Filter a list of RGB colors based on a limit.

    Parameters
    ----------
    colors : list of ColorRGB
        List of RGB colors to be filtered.
    limit : int, optional
        The limit used for filtering, by default 50.

    Returns
    -------
    list of ColorRGB
        Filtered list of RGB colors.

    """
    result = []
    for r_one, g_one, b_one in colors:
        can_add_result: bool = True
        for r_two, g_two, b_two in result:
            if ((r_one - r_two) ** 2 + (g_one - g_two) ** 2 + (b_one - b_two) ** 2) < limit * limit:
                can_add_result = False
                break
        if can_add_result:
            result.append(ColorRGB(r_one, g_one, b_one))
    return result


def show_color_palette(colors: list[ColorRGB], wait: bool = True, size: int = 70, columns: int = 5):
    """
    Display a color palette with the given list of RGB colors.

    Parameters
    ----------
    colors : list of ColorRGB
        List of RGB colors to display in the palette.
    wait : bool, optional
        Whether to wait for a key press before closing the window, by default True.
    size : int, optional
        Size of each color rectangle in pixels, by default 70.
    columns : int, optional
        Number of columns in the palette, by default 5.

    Returns
    -------
    None

    Notes
    -----
    This function uses OpenCV (cv2) for displaying the color palette.

    """
    color_count: int = len(colors)
    rows = (color_count + columns - 1) // columns
    result_img = np.full((size * rows, size * columns, 3), 255, np.uint8)

    for index, color in enumerate(colors):
        row = index // columns
        col = index % columns
        top_left = (col * size, row * size)
        bottom_right = ((col + 1) * size, (row + 1) * size)
        cv2.rectangle(result_img, top_left, bottom_right, color, -1)

    cv2.imshow('Color Palette', result_img)
    if wait:
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def get_contour_boxes_by_color(image, rgb_color) -> list[ImageBox2D]:
    """
    Given an image and RGB color, find contours based on the color and return the bounding boxes.

    Parameters:
    - image: Input image
    - rgb_color: Target RGB color for contour detection

    Returns:
    - List of bounding boxes [(x1, y1, w1, h1), (x2, y2, w2, h2), ...]
    """

    # Convert the given RGB color to HSV for better color segmentation
    hsv_color = cv2.cvtColor(np.uint8([[list(rgb_color)]]), cv2.COLOR_RGB2HSV)[0][0]

    # Masking image based on the given color
    lower_bound = np.array([hsv_color[0] - 20, 50, 50])
    upper_bound = np.array([hsv_color[0] + 20, 255, 255])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Finding contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bounding_boxes = []
    for contour in contours:
        if cv2.contourArea(contour) > 5000:  # Filtering small contours
            x, y, w, h = cv2.boundingRect(contour)
            bounding_boxes.append(ImageBox2D(x, y, w, h))

    return bounding_boxes


def get_contour_boxes_by_colors(image, colors: list[ColorRGB]) -> list[tuple[ColorRGB, list[ImageBox2D]]]:
    """
    Find contours based on specified colors in the image and return the corresponding bounding boxes.

    Parameters
    ----------
    image : numpy.ndarray
        Input image in NumPy array format.
    colors : list of ColorRGB
        List of RGB colors to be used for contour detection.

    Returns
    -------
    list of tuple[ColorRGB, list[ImageBox2D]]
        List of tuples containing RGB color and corresponding image boxes.

    """
    result = []
    for color in colors:
        result.append((color, get_contour_boxes_by_color(image, color)))
    return result


def draw_boxes_on_image_by_color(image, rgb_color, box_color=(255, 0, 0), paint_image=None):
    """
    Draw bounding boxes on the image based on the given RGB color.

    Parameters:
    - image: Input image
    - rgb_color: Target RGB color for contour detection

    Returns:
    - Image with drawn bounding boxes
    """
    if paint_image is None:
        paint_image = image
    # Get the bounding boxes
    boxes = get_contour_boxes_by_color(image, rgb_color)

    # Draw the boxes on the image
    for (x, y, w, h) in boxes:
        cv2.rectangle(paint_image, (x, y), (x + w, y + h), box_color, 2)  # Drawing in blue color

    return paint_image


def calculate_overlap(box1: ImageBox2D, box2: ImageBox2D) -> float:
    """
    Calculate the overlap ratio between two image boxes.

    Parameters
    ----------
    box1 : ImageBox2D
        The first image box.
    box2 : ImageBox2D
        The second image box.

    Returns
    -------
    float
        The ratio of overlap between the two boxes.

    """
    x1 = max(box1.x, box2.x)
    y1 = max(box1.y, box2.y)
    x2 = min(box1.x + box1.w, box2.x + box2.w)
    y2 = min(box1.y + box1.h, box2.y + box2.h)

    if x2 <= x1 or y2 <= y1:
        return 0.0

    intersection_area = (x2 - x1) * (y2 - y1)
    box1_area = box1.w * box1.h
    box2_area = box2.w * box2.h
    overlap_ratio = intersection_area / min(box1_area, box2_area)

    return overlap_ratio


def remove_overlapping_boxes(boxes: list[ImageBox2D], overlap_threshold: float = 0.5) -> list[ImageBox2D]:
    """
    Remove overlapping boxes from the given list of image boxes.

    Parameters
    ----------
    boxes : list of ImageBox2D
        List of image boxes.
    overlap_threshold : float
        The threshold overlap ratio above which a box is considered for removal.

    Returns
    -------
    list of ImageBox2D
        List of image boxes with overlapping boxes removed.

    """
    valid_boxes = []
    for index_box, box in enumerate(boxes):
        is_valid = True
        for index_valid_box, valid_box in enumerate(valid_boxes):
            if index_box != index_valid_box:
                overlap_ratio = calculate_overlap(box, valid_box)
                if overlap_ratio >= overlap_threshold:
                    is_valid = False
                    break
        if is_valid:
            valid_boxes.append(box)

    return valid_boxes


def show_palette_and_image(path: str):
    """
    Load an image, extract its color palette, and display the color palette and image with boxes.

    Parameters
    ----------
    path : str
        Path to the input image.

    Returns
    -------
    None

    """
    image = cv2.imread(path)
    small_image = cv2.resize(image, dsize=(0, 0), fx=resize, fy=resize)

    colorthief = ColorThief(path)
    palettes = colorthief.get_palette(color_count=120, quality=100)
    palettes = filter_colors(palettes, limit=50)
    # show_color_palette(palettes, wait=False, size=70, x_length=7)

    # cv2.imshow("small_origin", small_image)

    boxed_image1 = small_image.copy()
    for color in palettes:
        boxed_image1 = draw_boxes_on_image_by_color(small_image, color, box_color=color, paint_image=boxed_image1)

    cv2.imshow("box", boxed_image1)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def preprocess_image(image):
    """
    Preprocess the image by making the background bright and text dark.

    Parameters
    ----------
    image : numpy.ndarray
        Input image in NumPy array format.

    Returns
    -------
    numpy.ndarray
        Preprocessed image.

    """
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to make the background bright and text dark
    threshold_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                            cv2.THRESH_BINARY, 11, 2)

    return threshold_image


def extract_text_from_image(image, boxes, lang: str = 'kor+eng', show_image: bool = False):
    """
    Extract text from image using Tesseract OCR for the specified boxes.

    Parameters
    ----------
    image : numpy.ndarray
        Input image in NumPy array format.
    boxes : list of ImageBox2D
        List of image boxes.
    lang : str, optional
        Tesseract OCR language(s), by default 'kor+eng'.
    show_image : bool
        show image by default False.

    Returns
    -------
    list of str
        List of extracted texts corresponding to the specified boxes.

    """
    extracted_texts = []
    images = []
    for box in boxes:
        x, y, w, h = box
        cropped_image = image[y:y + h, x:x + w]

        # Preprocess the cropped image
        preprocessed_image = preprocess_image(cropped_image)

        # Extract text using Tesseract OCR
        extracted_text = pytesseract.image_to_string(preprocessed_image, lang=lang)
        if show_image:
            images.append(preprocessed_image)
        # Remove spaces and newlines from the extracted text
        processed_text = extracted_text.replace(" ", "").replace("\n", "")

        extracted_texts.append(processed_text)
    if show_image:
        show_resized_images_in_row(images, 120)
    return extracted_texts


def show_resized_images_in_row(image_list, target_width):
    """
    Display a row of resized images horizontally.

    Args:
        image_list (list): A list of NumPy ndarray images to display.
        target_width (int): The target width for resizing images.

    Returns:
        None
    """
    # Resize images to the target width while maintaining aspect ratio
    resized_images = [cv2.resize(img, (target_width, int(img.shape[0] * target_width / img.shape[1]))) for img in
                      image_list]

    # Ensure all images have the same number of channels
    for i in range(len(resized_images)):
        if len(resized_images[i].shape) == 2:
            resized_images[i] = cv2.cvtColor(resized_images[i], cv2.COLOR_GRAY2BGR)

    # Concatenate resized images horizontally
    total_width = sum(img.shape[1] for img in resized_images)
    max_height = max(img.shape[0] for img in resized_images)
    concatenated = np.zeros((max_height, total_width, 3), dtype=np.uint8)

    x_offset = 0
    for img in resized_images:
        concatenated[:img.shape[0], x_offset:x_offset + img.shape[1]] = img
        x_offset += img.shape[1]

    # Display the concatenated image
    cv2.imshow('Concatenated Resized Images', concatenated)


class ImageToText:

    def __init__(self, image_path: str):
        """
        Initialize an instance of TextInScheduleImage.

        Parameters
        ----------
        image_path : str
            Path to the input image.

        """
        self.image_path: str = image_path
        self.original_image: np.ndarray = cv2.imread(self.image_path)
        self.colors: list[ColorRGB] = []
        self.boxes: list[ImageBox2D] = []
        self.texts: list[str] = []

    def clear(self):
        """
        Clear all attributes of the TextInScheduleImage instance.

        Returns
        -------
        None

        """
        self.image_path = ""
        self.original_image: np.ndarray = np.ndarray([])
        self.colors.clear()
        self.boxes.clear()
        self.texts.clear()

    def set_path(self, image_path: str):
        """
        Set the path to the input image.

        Parameters
        ----------
        image_path : str
            Path to the input image.

        Returns
        -------
        None

        """
        self.image_path: str = image_path
        self.original_image: np.ndarray = cv2.imread(self.image_path)

    def run_setting_box(
            self,
            palette_color_count: int = 120,
            palette_color_quality: int = 100,
            filter_colors_limit: int = 50,
            show_palette: bool = False,
            show_boxes: bool = False,
            box_contour_color: ColorRGB = (255, 0, 0),
            box_overlap_threshold: float = 0.4,
            show_box_resize: float = 0.4,
            wait: bool = True,
    ):
        """
        Run the process of setting bounding boxes based on colors in the image.

        This function extracts a color palette from the input image and then detects contours
        corresponding to each color in the palette. Bounding boxes are generated for the detected
        contours, and overlapping boxes are removed based on the specified overlap threshold.

        Parameters
        ----------
        palette_color_count : int, optional
            Number of colors in the palette, by default 120.
        palette_color_quality : int, optional
            Quality of color extraction from the palette, by default 100.
        filter_colors_limit : int, optional
            Threshold for filtering similar colors in the palette, by default 50.
        show_palette : bool, optional
            Whether to display the extracted color palette, by default False.
        show_boxes : bool, optional
            Whether to display the detected bounding boxes on an image, by default False.
        box_contour_color : ColorRGB, optional
            RGB color for drawing bounding box contours, by default (255, 0, 0) (blue).
        box_overlap_threshold : float, optional
            Threshold for removing overlapping boxes, by default 0.4.
        show_box_resize : float, optional
            Resize factor for displaying bounding box image, by default 0.4.
        wait : bool, optional
            Whether to wait for a key press before closing windows, by default True.

        Returns
        -------
        None

        """
        colorthief = ColorThief(self.image_path)
        self.colors = filter_colors(
            colorthief.get_palette(color_count=palette_color_count, quality=palette_color_quality),
            limit=filter_colors_limit
        )
        if show_palette:
            show_color_palette(self.colors, wait=False)

        self.boxes = []
        color_boxes = get_contour_boxes_by_colors(self.original_image, self.colors)
        for color, boxes in color_boxes:
            self.boxes.extend(boxes)

        self.boxes.sort(key=lambda image_box: image_box.w * image_box.h)

        self.boxes = remove_overlapping_boxes(self.boxes, overlap_threshold=box_overlap_threshold)

        if show_boxes:
            box_image = self.original_image.copy()
            for box in self.boxes:
                cv2.rectangle(box_image, (box.x, box.y), (box.x + box.w, box.y + box.h), box_contour_color, 2)
            box_image = cv2.resize(box_image, dsize=(0, 0), fx=show_box_resize, fy=show_box_resize)
            cv2.imshow("box", box_image)

        if wait:
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def run_get_texts(self, show_image=False):
        """
        Run the process of extracting text from the image based on the defined boxes.

        Parameters
        ----------
        show_image : bool, optional
            Whether to display intermediate images, by default False.

        Returns
        -------
        None

        """
        self.texts = extract_text_from_image(self.original_image, self.boxes, show_image=show_image)


if __name__ == "__main__":
    DIR_PATH: str = r'./HakFile/Test/HanyangImage'

    resize: float = 0.4

    for file in os.listdir(DIR_PATH)[:4]:
        print(file)
        boxx = ImageToText(f"{DIR_PATH}/{file}")
        boxx.run_setting_box(box_contour_color=(0, 0, 255), show_boxes=True, wait=False, box_overlap_threshold=0.5)
        boxx.run_get_texts(show_image=True)
        pprint.pprint(boxx.texts)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
