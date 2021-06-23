import random
import cv2
import numpy as np
from typing import Tuple
from matplotlib import pyplot as plt


def view_image(image, name_of_window):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_image_different_color_space(image, arg):
    return cv2.cvtColor(image, arg)


def extract_contours(image: np.ndarray, color_range: list) -> np.ndarray:
    """
    Поиск контуров на изображении.
    :param image: предварительно обработанное изображение с нанесенными рамками.
    :return: контуры на изображении.
    """
    # Диапазон цвета которого не может быть в документе (в нашем случае - синий)
    upper_range = np.array(color_range[1])
    lower_range = np.array(color_range[0])

    image_mask = cv2.inRange(image, lower_range, upper_range)

    contours_of_frames, _ = cv2.findContours(
        image_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    return contours_of_frames


def extract_frames(contours_of_frames: np.ndarray) -> list:
    """
    Поиск рамок на изображении.
    :param contours_of_frames: контуры на изображении.
    :return: полученные координаты рамок.
    """
    frames = []

    # перебираем все найденные контуры в цикле
    for contours_of_frame in contours_of_frames:
        rect = cv2.minAreaRect(contours_of_frame)  # пытаемся вписать прямоугольник
        box = cv2.boxPoints(rect)  # поиск четырех вершин прямоугольника
        box = np.int0(box)  # округление координат
        area = int(rect[1][0] * rect[1][1])  # вычисление площади

        if area > 250:
            frames.append(box[[1, 3]])

    return np.array(frames).tolist()


def search_rectangles_of_color(image_for_processing: np.ndarray, color_range: list) -> Tuple[np.ndarray, dict]:
    """
    Поиск рамок цветовых прямоугольников на изображении.
    :param image_for_processing: изображение на котором ведется поиск
    :param color_range: цвет прямоугольник которого ищется.
    :return: (Изображение с рамками, координаты всех рамок.)
    """
    contours_of_frames = extract_contours(image_for_processing, color_range)
    frames = extract_frames(contours_of_frames)

    cords = {str(i): frame for i, frame in enumerate(frames)}

    for location in frames:
        x_0 = location[0][0]
        y_0 = location[0][1]
        x_1 = location[1][0]
        y_1 = location[1][1]

        cv2.rectangle(image_for_processing, (x_0, y_0), (x_1, y_1), (0, 0, 0), 3)

    return image_for_processing, cords


def darkening_colors(image: np.ndarray,  clean_areas_cords: list) -> np.ndarray:
    mask = np.zeros(image.shape, dtype=np.uint8)

    for i in clean_areas_cords:
        contours = np.array(i)
        cv2.fillPoly(mask, pts=[contours], color=(255, 255, 255))

    return cv2.bitwise_and(image, mask)


def _crop_image_to_smaller(img: np.ndarray, len_row: int, column_len: int) -> np.ndarray:
    return img[0:len_row, 0:column_len]


def crop_image_to_smaller(image_1: np.ndarray, image_2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Обрезка изображения под наименьшие границы.
    :param image_1:
    :param image_2:
    :return: np.ndarray
    """
    row1 = len(image_1)
    row2 = len(image_2)
    colonum1 = len(image_1[0])
    colonum2 = len(image_2[0])

    if row1 != row2:
        if row1 > row2:
            image_1 = _crop_image_to_smaller(image_1, row2, len(image_1))
        else:
            image_2 = _crop_image_to_smaller(image_2, row1, len(image_2))

    if colonum1 != colonum2:
        if colonum1 > colonum2:
            image_1 = _crop_image_to_smaller(image_1,  len(image_1), colonum2)
        else:
            image_2 = _crop_image_to_smaller(image_2,  len(image_2), colonum1)

    return image_1, image_2


def add_image_light_pixel_rule(image_1: np.ndarray, image_2: np.ndarray) -> np.ndarray:
    image_1, image_2 = crop_image_to_smaller(image_1, image_2)

    magic = lambda px_1, px_2: np.where(
        0.3 * px_1[0] + 0.59 * px_1[1] + 0.11 * px_1[2] > 0.3 * px_2[0] + 0.59 * px_2[1] + 0.11 * px_2[2],
        px_1, px_2)

    return magic(image_1, image_2)


def frequency_filtering(image: np.ndarray, filtration_purity=60) -> np.ndarray:
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)

    rows, cols = image.shape[0], image.shape[1]
    crow, ccol = rows // 2, cols // 2
    filtration_purity //= 2

    fshift[crow - filtration_purity:crow + filtration_purity, ccol - filtration_purity:ccol + filtration_purity] = 0
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)

    return np.real(img_back)


def noisy_image_processing(image: np.ndarray) -> np.ndarray:
    """
    Алгоритм шума есть выбор рандомного значения яркости канала(оси канала) от 0 до его предыдущего значения
    """
    for line in image:

        for px in line:
            px[0] = random.randint(0, px[0])
            px[1] = random.randint(0, px[1])
            px[2] = random.randint(0, px[2])

    return image


def paint_processing(image: np.ndarray):
    img = cv2.medianBlur(image, 5)
    ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return th1


def encode_image(image: np.ndarray):
    for line in image:
        for px in line:
            if px[0] < 200 and px[1] < 200 and px[2] < 200:
                px[0], px[1], px[2] = 255, 255, 255
            else:
                px[0], px[1], px[2] = 255, 255, 254
    return image


def decode_image(image: np.ndarray):
    for line in image:
        for px in line:
            if px[0] == 255 and px[1] == 255 and px[2] == 254:
                px[0], px[1], px[2] = 0, 0, 0
    return image