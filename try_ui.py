from dlgo.ui import UI
import pygame

ui = UI()

ui.initialize()
point = (1,2)
ui.draw(point, 'BLACK')
while True:
    pygame.time.wait(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
