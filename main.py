import cv2
import numpy as np
from tensorflow.keras.models import load_model
import pygame 


model = load_model('Devanagari detection.h5')
pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Whiteboard")
running = True
is_writing = False
screen.fill((0, 0, 0))
mx_lst, my_lst = [], []
bbox = [0, 0, 0, 0]


img_lst = []
for i in range(0, 46):
    img_lst.append(pygame.image.load('image/' + str(i) + '.png'))



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION and is_writing:
            mx, my = pygame.mouse.get_pos()
            mx_lst.append(mx)
            my_lst.append(my)
            pygame.draw.circle(screen, (255, 255, 255), (mx, my), 5, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            is_writing = True
            mx_lst, my_lst = [], []

        if event.type == pygame.MOUSEBUTTONUP:
            is_writing = False
            x = sorted(mx_lst)
            y = sorted(my_lst)
            x = list(set(x))
            y = list(set(y))
            x1, y1, x2, y2 = min(x) - 10, min(y) - 10, max(x) + 10, max(y) + 10
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x1, y1, x2-x1, y2-y1), 1)

            x, y = [], []
            img = pygame.PixelArray(screen)
            img_array = np.array(img)[x1:x2, y1:y2].T.astype(np.float32)
            img_array = cv2.resize(img_array, (32, 32))
            img_array = img_array.reshape((-1, 32, 32, 1))
            prediction = model.predict(img_array)
            prediction = np.argmax(prediction)
            pygame.PixelArray.close(img)
            screen.blit(img_lst[prediction], (x1, y1))
            
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'q':
                screen.fill((0, 0, 0))
                mx_lst, my_lst = [], []

    pygame.display.update()