import random

import pygame
import numpy as np
from collections import Counter

pygame.init()
screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption('KNN')
font = pygame.font.Font(None, 30)

exit = False
mouse_button_down = False
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
classes_count = 3
number_generated_points = 10
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
additional_points = []
final_k = None
points_initialized = False
initial_points = []
k_initialized = False
points_for_k = []
prob_final_k = []
matrix = []


class Point:
    def __init__(self, x, y, color='black', cls=None):
        self.x = x
        self.y = y
        self.color = color
        self.cls = cls

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
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def classify(target_point, k):
    distances = {}
    for point in initial_points:
        distances[point] = dist(target_point.x, target_point.y, point.x, point.y)
    distances = dict(sorted(distances.items(), key=lambda x: x[1]))
    l = list(distances.keys())
    result_classes = []
    for i in range(k):
        result_classes.append(l[i].cls)
    cnt = dict(Counter(result_classes))
    cnt = dict(sorted(cnt.items(), key=lambda x: x[1], reverse=True))
    return list(cnt.keys())[0]


def generate_points(number_of_points_in_class, number_of_classes):
    points = []
    padding = 0
    for cls in range(number_of_classes):
        for i in range(number_of_points_in_class):
            x = random.randint(100 * (cls + 1) + padding, 100 * (cls + 1) + 101 + padding)
            y = random.randint(100 * (cls + 1) + padding, 100 * (cls + 1) + 101 + padding)
            points.append(Point(x, y, color=colors[cls], cls=cls))
        padding += 50
    return points


while not exit:
    if not points_initialized:
        initial_points = generate_points(number_generated_points, classes_count)
        d = {}
        i = 0
        for k, v in keys.items():
            d[k] = v
            i += 1
            if i == classes_count:
                break
        keys = d
        for i in range(len(initial_points)):
            matrix.append([])
        points_initialized = True

    pygame.time.delay(100)
    screen.fill((255, 255, 255))
    for initial_point in initial_points:
        initial_point.draw(screen)
    for point_for_k in points_for_k:
        point_for_k.draw(screen)
    for additional_point in additional_points:
        additional_point.draw(screen)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not mouse_button_down and not k_initialized:
                coors = event.pos
                point = Point(coors[0], coors[1])
                points_for_k.append(point)
                point.draw(screen)
                pygame.display.update()
                mouse_button_down = True

            if not mouse_button_down and k_initialized:
                coors = event.pos
                point = Point(coors[0], coors[1])
                additional_points.append(point)
                point.draw(screen)
                pygame.display.update()
                mouse_button_down = True

        if event.type == pygame.KEYDOWN:
            if event.key in keys.keys() and mouse_button_down and not k_initialized:
                points_for_k[-1].cls = keys[event.key]
                points_for_k[-1].color = colors[keys[event.key]]
                points_for_k[-1].draw(screen)
                pygame.display.update()
                for k in range(1, len(initial_points)):
                    c = classify(points_for_k[-1], k)
                    if c == points_for_k[-1].cls:
                        matrix[k].append(True)
                    else:
                        matrix[k].append(False)
                mouse_button_down = False

            if event.key == pygame.K_RETURN and not mouse_button_down and not k_initialized:
                d = {}
                for k, row in enumerate(matrix[1:]):
                    print(f'For K = {k + 1} result = {row}')
                    cnt = dict(Counter(row))
                    d[k + 1] = cnt[True]
                d = dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
                idx = 0
                for i in range(len(list(d.keys())) - 1):
                    if list(d.values())[i] != list(d.values())[i + 1]:
                        idx = i // 2
                        break
                final_k = list(d.keys())[idx]
                initial_points.extend(points_for_k)
                points_for_k.clear()
                print(f'K initialized to {final_k}')
                k_initialized = True

            if event.key == pygame.K_RETURN and mouse_button_down and k_initialized:
                target_class = classify(additional_points[-1], final_k)
                additional_points[-1].cls = target_class
                additional_points[-1].color = colors[target_class]
                additional_points[-1].draw(screen)
                pygame.display.update()
                mouse_button_down = False
