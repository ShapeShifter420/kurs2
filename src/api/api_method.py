import os
import sys

from fastapi import FastAPI
import uvicorn
from image_work.manager_image_group import ImageProcessor

from api.models import ColorSpaces, RectanglesCords, FrequencyFiltering, Images, ImageCipher,Image
from api.logger_configuration import get_logger


app = FastAPI()
manager = ImageProcessor()
log = get_logger('Main_logger')


def log_this(e: Exception) -> None:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    log.info(f'Выполнение было прервано в файле {file_name}:{exc_tb.tb_lineno} с ошибкой {str(e)}')


@app.post('/api/bw_braitness')
async def bw_braitnes():
    pass


@app.post('/api/new_color_space')
async def new_color_space(color_spaces: ColorSpaces):
    """Получить изображение в новом цветовом пространстве."""
    try:
        color_spaces_img = []

        manager.load_image(color_spaces.image)
        path_to_new_image = manager.create_pictures_different_color_space(color_spaces.color_spaces)

        for path, color_space in path_to_new_image:
            color_spaces_img.append({'path': path, 'color_space': color_space})

        return color_spaces_img
    except Exception as ex:
        log_this(ex)


@app.post('/api/search_all_rectangles_of_color')
async def search_all_rectangles_of_color(rectangles_cords: RectanglesCords):
    """Получить все прямоугольники одного цвета."""
    try:

        manager.load_image(rectangles_cords.image)

        image_with_frames, cords = manager.get_all_rectangles_of_color(rectangles_cords.color_range)

        return {"path": image_with_frames, "rectangles_cords": cords}
    except Exception as ex:
        log_this(ex)


@app.post('/api/fold_images')
async def fold_images(images: Images):
    try:
        images = images.images

        manager.load_image(images[0])

        for image in images[1:]:
            manager.add_image(image)

        return manager.save_image()

    except Exception as ex:
        log_this(ex)


@app.post('/api/frequency_filtering')
async def frequency_filtering(filtering: FrequencyFiltering):
    try:

        manager.load_image_as_gray(filtering.image)

        return manager.frequency_filtering(filtering.filtration_purity)
    except Exception as ex:
        log_this(ex)


@app.get('/api/get_color_spaces')
async def get_color_spaces():
    """Получить все доступные цветовые пространства."""
    try:
        return manager.get_color_spaces
    except Exception as ex:
        log_this(ex)


@app.get('/api/get_color_ranges')
async def get_color_ranges():
    try:
        return manager.get_color_range
    except Exception as ex:
        log_this(ex)


@app.post('/api/color_noize')
async def post_noisy_image(image: Image):
    """Возврат защумленного изображения, можно регулировать параметр защумления от 0 до 1"""
    try:
        manager.load_image(image.path)
        return manager.noisy_image()
    except Exception as ex:
        log_this(ex)


@app.post('/api/pencel')
async def post_pensel(image: Image):
    try:
        manager.load_image_as_gray(image.path)
        return manager.pensel_generation()
    except Exception as ex:
        log_this(ex)


@app.post('/api/cipher')
async def post_cipher(image: ImageCipher):
    try:
        manager.load_image(image.path)
        if image.encode is True:
            return manager.encode_image()
        else:
            return manager.decode_image()
    except Exception as ex:
        log_this(ex)


@app.post('/api/topbrait')
async def post_topbrite(images: Images):
    try:
        images = images.images

        manager.load_image(images[0])

        for image in images[1:]:
            manager.top_brait(image)

        return manager.save_image()

    except Exception as ex:
        log_this(ex)


def server_run():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == '__main__':
    server_run()
