import random
from sklearn.svm import SVC
import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption('SVM')
font = pygame.font.Font(None, 30)

exit = False
points_initialized = False
initial_points = []
colors = {
    0: 'yellow',
    1: 'green'
}
fitted = False
mouse_button_down = False
additional_points = []
clf = SVC(kernel='linear')
line_coors_upper = None
line_coors_down = None


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


def generate_points(number_of_points_in_class):
    points = []
    padding_x = 0
    padding_y = 0
    for cls in range(2):
        for i in range(number_of_points_in_class):
            x = random.randint(150 * (cls + 1) + padding_x, 150 * (cls + 1) + 201 + padding_x)
            y = random.randint(50 * (cls + 1) + padding_y, 50 * (cls + 1) + 201 + padding_y)
            points.append(Point(x, y, color=colors[cls], cls=cls))
        padding_x += 100
        padding_y += 100
    global points_initialized
    points_initialized = True
    return points


def fit():
    points = []
    classes = []
    for point in initial_points:
        points.append([point.x, point.y])
        classes.append(point.cls)
    global clf
    print(f'Distinct classes {classes}')
    clf.fit(points, classes)


def get_line_coors():
    w = clf.coef_[0]
    a = - w[0] / w[1]
    x_coors = np.linspace(0, 700)
    y_coors = a * x_coors - clf.intercept_[0] / w[1]
    return (x_coors[0], y_coors[0]), (x_coors[-1], y_coors[-1])


while not exit:
    if not points_initialized:
        initial_points = generate_points(15)

    pygame.time.delay(100)
    screen.fill((255, 255, 255))
    for initial_point in initial_points:
        initial_point.draw(screen)
    for additional_point in additional_points:
        additional_point.draw(screen)
    if line_coors_upper is not None and line_coors_down is not None:
        pygame.draw.line(screen, 'black', line_coors_upper, line_coors_down, 2)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not fitted:
                fit()
                fitted = True
                print('SVC fitted')
                line_coors_upper, line_coors_down = get_line_coors()

            if event.key == pygame.K_RETURN and mouse_button_down and fitted:
                point = additional_points[-1]
                cls = clf.predict([[point.x, point.y]])
                point.cls = cls[0]
                point.color = colors[point.cls]
                mouse_button_down = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not mouse_button_down and fitted:
                coors = event.pos
                point = Point(coors[0], coors[1])
                additional_points.append(point)
                point.draw(screen)
                pygame.display.update()
                mouse_button_down = True