import pygame
import numpy as np
from find_digits import recognize_number

pygame.init()
(width, height) = (200, 200)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('GUI for Number Recognition')

file_name = 'sample_image.png'

points = np.empty((0, 2), dtype='f')
c_radius = 1
c_color = (255, 255, 255)
c_thickness = 0
jet_radius = 5
jet_thr = 0

bg_color = (0, 0, 0)

running = True
pushing = False
exit = False
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pushing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            pushing = False

    if pushing and np.random.uniform(0, 1) > jet_thr:
        (x, y) = pygame.mouse.get_pos()
        r = np.random.uniform(0, jet_radius)
        phi = np.random.uniform(0, 2 * np.pi)
        coord = [x + r * np.cos(phi), height - y + r * np.sin(phi)]
        points = np.append(points, [coord], axis=0)

    screen.fill(bg_color)
    for point in points:
        pygame.draw.circle(screen, c_color, (int(point[0]), height - int(point[1])), c_radius, c_thickness)
    pygame.display.flip()

pygame.image.save(screen, file_name)
print(f'Result - {recognize_number(file_name)}')
pygame.quit()
