from typing import List, Tuple

from pathlib import Path

import cv2

import numpy as np

from image_work.image import Image
from image_work import image_work


class ImageProcessor:
    image: Image

    color_space = {'HVS': cv2.COLOR_BGR2HSV,
                  'YCrCb': cv2.COLOR_BGR2YCrCb,
                  'XYZ': cv2.COLOR_BGR2XYZ,
                  'RGB': cv2.COLOR_BGRA2RGB,
                  'GRAY': cv2.COLOR_BGR2GRAY}

    color_ranges = {'black': [[0, 0, 0], [10, 10, 10]],
                    'grey': [[110, 50, 50], [130, 255, 255]]}

    image_color_space = {}

    def load_image(self, url: str):
        self.image = Image(url)

    def load_image_as_gray(self, url: str):
        self.image = Image(url, 0)

    def save_image(self) -> Path:
        return self.image.save_image_cv2(self.image.image, 'save_image')

    def add_image(self, image_url: str):
        self.image.image = \
            image_work.add_image_light_pixel_rule(self.image.image, Image(image_url).image)

    @property
    def get_color_spaces(self) -> List[str]:
        return list(self.color_space.keys())

    @property
    def get_color_range(self) -> List[str]:
        return list(self.color_ranges.keys())

    def create_pictures_different_color_space(self, color_space_names: List[str]) -> List[Tuple[Path, str]]:
        """
        Метод создает на основе начального изображения изображения, в других цветовых пространствах.
        Метод так же проверят переданные ему цветовые названия цветовых пространств на корректность.
        :param color_space_names: Имена цветовых пространств.
        :return: Список из таплов в котором лежит путь до файла и его цветовое пространство.
        """
        path_to_new_image = []

        exists_color_space_names = self._get_only_existing_color_spaces(color_space_names)

        for name_color_space in exists_color_space_names:
            image_in_new_color_space = self._convert_image_space_color(name_color_space)
            path = self.image.save_image_cv2(image_in_new_color_space, name_color_space)

            path_to_new_image.append((path, name_color_space))

        return path_to_new_image

    def _get_only_existing_color_spaces(self, color_space_names: List[str]) -> List[str]:
        return list(set(color_space_names).intersection(set(self.color_space.keys())))

    def _convert_image_space_color(self, name_color_space) -> np.ndarray:
        color_space = self.color_space.get(name_color_space)
        new_image = image_work.get_image_different_color_space(self.image.image, color_space)

        return new_image

    def get_all_rectangles_of_color(self, name_color_range: str) -> Tuple[Path, dict]:
        """
        Получить координаты всех прямоугольников цвета `name_color_range`, а так же нарисовать их на изображении.
        :param name_color_range: Название цвета (Это скорее название диапазона.)
        :return:
        """
        color_rectangels = self.color_ranges.get(name_color_range)
        image_with_frames, cords = image_work.search_rectangles_of_color(self.image.copy_image(),  color_rectangels)
        image_with_frames_path = self.image.save_image_cv2(image_with_frames, 'rect')

        return image_with_frames_path, cords

    def dims_colors_in_image_except(self, name_color_range: str) -> Path:
        """
        Затемняет изображение кроме тех мест, где есть переданный цвет (диапазон).
        :param name_color_range: Название цвета (Это скорее название диапазона.)
        :return: путь до изоражения.
        """
        remaining_color = self.color_ranges.get(name_color_range)
        image = image_work.darkening_colors(self.image.copy_image(), remaining_color)

        image_path = self.image.save_image(image, f'dark_image_{name_color_range}.png')

        return image_path

    def noisy_image(self):
        image = image_work.noisy_image_processing(self.image.image)
        return self.image.save_image_cv2(image, 'Noisy')

    def pensel_generation(self):
        image = image_work.paint_processing(self.image.image)
        return self.image.save_image_cv2(image, 'Pensel')

    def encode_image(self):
        image = image_work.encode_image(self.image.image)
        return self.image.save_image_cv2(image, 'Encode')

    def decode_image(self):
        image = image_work.decode_image(self.image.image)
        return self.image.save_image_cv2(image, 'Decode')

    def frequency_filtering(self, filtration_purity:str):
        image_with_filter = image_work.frequency_filtering(self.image.image, int(filtration_purity))
        return self.image.save_image_plt(image_with_filter, f'pur{filtration_purity}')

    def top_brait(self,image_url):
        self.image.image = \
            image_work.make_top_braight(self.image.image, Image(image_url).image)