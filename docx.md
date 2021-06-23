# Method API

## post

Изменение цветового пространства:

    /api/new_color_space 
        ->
        path: str - директория с файлом || урл в облаке
        color_space: List[str] - лист 
        
        <-
        [
        path: str - директория с обработанным изображением || урл в облаке 
        color_space: str - цветовое пространстов этого файла
        ]

Выделение рамок:

    /api/search_all_rectangles_of_color
        -> 
        path: str
        color_range: List[List[int, int, int], List[int, int, int]] все 0 <= int <= 255

        <-
        path: str
        rectangles_cords: Dict{area: List[x0, y0] List[x1, y1]}

Сложение изображений по принципу: на изображении остается только наиболее яркий пиксель.

    /api/fold_images
        -> 
        images: List[str]

        <-
        image: str

Изменение частотного окна через преобразование фурье. 
    
    /api/frequency_filtering
        ->
        image: str 
        filtration_purity: int
        
        <-
         image: str       

## get 

Получение всех доступных цветовых пространств.

    /api/get_color_spaces
        color_space: List[str] - отдет названия всех доступных цветовы пространств.

    /api/get_default_color_range
        color_ranges: List[List[int, int, int], List[int, int, int]]