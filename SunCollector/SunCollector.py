import cv2
import numpy as np
import pyautogui
import keyboard
import time
from numba import jit

pyautogui.FAILSAFE = True

image_paths = [
    
    r'C:\Users\mlavo\Downloads\Sun.png',
    r'C:\Users\mlavo\Downloads\Money1.png',
    r'C:\Users\mlavo\Downloads\money2.png',
    r'C:\Users\mlavo\Downloads\Money3.png'

    # Добавьте пути к другим изображениям здесь
]

#object_image = cv2.imread(r'C:\Users\mlavo\Downloads\Sun.png', cv2.IMREAD_COLOR) # Изображение объекта 

# Размеры и положение региона, который вы снимаете
region_x, region_y, region_width, region_height = 0, 0, 1920, 1080 #825, 425, 300, 300

isCollected = True

# Изменения координат объекта, найденные на скриншоте, к координатам на основном экране
#@jit(fastmath = True, NoPython = True, NoGIL = True, parallel = True)
def convert_coordinates(x, y):
    global region_x, region_y
    return x + region_x, y + region_y

#jit(fastmath = True, NoPython = True, NoGIL = True, parallel = True)
while True:
    timer = time.perf_counter()

    for image_path in image_paths:
        # Загрузите изображение объекта, который вы хотите найти
        object_image = cv2.imread(image_path)

        # Сделайте скриншот заданной области экрана
        screenshot = pyautogui.screenshot()
        screen_image = np.array(screenshot)

        # Преобразуйте изображение в формат BGR (OpenCV)
        screen_image = cv2.cvtColor(screen_image, cv2.COLOR_RGB2BGR)

        # Попытайтесь найти объект на скриншоте
        result = cv2.matchTemplate(screen_image, object_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        threshold = 0.8  # Порог совпадения (может потребоваться настройка)
        # Двигаем мышь
        if max_val > threshold:
            start_x, start_y = pyautogui.position()
            h, w, _ = object_image.shape
            center_x, center_y = convert_coordinates(max_loc[0] + w // 2, max_loc[1] + h // 2)
            pyautogui.moveTo(center_x, center_y)
            pyautogui.click()
            pyautogui.moveTo(start_x, start_y)

    '''
    if keyboard.is_pressed('e'):
        isCollected = False
    else: 
        isCollected = True

    # Скрин
    screenshot = pyautogui.screenshot()

    # Массив и преобразовка
    screenshot_np = np.array(screenshot)
    screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

    # Поиск
    result = cv2.matchTemplate(screenshot_rgb, object_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Двигаем мышь
    if max_val > 0.7 and isCollected:
        start_x, start_y = pyautogui.position()
        h, w, _ = object_image.shape
        center_x, center_y = convert_coordinates(max_loc[0] + w // 2, max_loc[1] + h // 2)
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()
        pyautogui.moveTo(start_x, start_y)

    '''

    print(time.perf_counter() - timer)
