import pygame
import numpy as np
from collections import Counter

pygame.init()
screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption('KNN')
font = pygame.font.Font(None, 30)

exit = False
mouse_button_down = False
points = []
keys = {
    pygame.K_0: 0,
    pygame.K_1: 1,
    pygame.K_2: 2,
    pygame.K_3: 3,
    pygame.K_4: 4,
    pygame.K_5: 5,
    pygame.K_6: 6,
    pygame.K_7: 7,
    pygame.K_8: 8,
    pygame.K_9: 9,
}
classes = {}
colors = {
    0: 'red',
    1: 'green',
    2: 'blue',
    3: 'pink',
    4: 'purple',
    5: 'orange',
    6: 'grey',
    7: 'gold',
    8: 'yellow',
    9: 'coral'
}
space_pressed = False
additional_points = []
k = None


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = 'black'
        self.cls = None

    def __eq__(self, other):
        if self.color == other.color and self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.x, self.y, self.color))

    def __str__(self):
        return f'Point({self.x}, {self.y}, {self.color})'

    def __repr__(self):
        return f'Point({self.x}, {self.y}, {self.color})'

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 5)


def dist(x1, y1, x2, y2):
    return np.sqrt((x1-x2) ** 2 + (y1-y2) ** 2)


def classify(target_point):
    distances = {}
    for point in points:
        distances[point] = dist(target_point.x, target_point.y, point.x, point.y)
    distances = dict(sorted(distances.items(), key=lambda x: x[1]))
    l = list(distances.keys())
    result_classes = []
    for i in range(int(k)):
        result_classes.append(l[i].cls)
    cnt = dict(Counter(result_classes))
    cnt = dict(sorted(cnt.items(), key=lambda x: x[1], reverse=True))
    target_point.cls = list(cnt.keys())[0]
    target_point.color = colors[target_point.cls]


while not exit:
    pygame.time.delay(100)
    screen.fill((255, 255, 255))
    for point in points:
        point.draw(screen)
    for additional_point in additional_points:
        additional_point.draw(screen)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not mouse_button_down and not space_pressed:
                coors = event.pos
                point = Point(coors[0], coors[1])
                points.append(point)
                point.draw(screen)
                pygame.display.update()
                mouse_button_down = True
            elif not mouse_button_down and space_pressed:
                coors = event.pos
                point = Point(coors[0], coors[1])
                additional_points.append(point)
                point.draw(screen)
                pygame.display.update()
                mouse_button_down = True

        if event.type == pygame.KEYDOWN:
            if event.key in keys.keys() and mouse_button_down and not space_pressed:
                if keys[event.key] not in classes:
                    classes[keys[event.key]] = 1
                else:
                    classes[keys[event.key]] += 1

                points[-1].cls = keys[event.key]
                mouse_button_down = False

            if event.key == pygame.K_SPACE and not space_pressed:
                for point in points:
                    point.color = colors[point.cls]
                    point.draw(screen)
                pygame.display.update()
                space_pressed = True
                k = np.sqrt(len(points))

            if event.key == pygame.K_RETURN and mouse_button_down and space_pressed:
                classify(additional_points[-1])
                additional_points[0].draw(screen)
                pygame.display.update()
                mouse_button_down = False
