import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import random


def dist(x1, y1, x2, y2):
    return np.sqrt((x1-x2) ** 2 + (y1-y2) ** 2)


def generate_points_file(points_count, filename):
    x = np.random.randint(0, 100, points_count)
    y = np.random.randint(0, 100, points_count)
    with open(filename, 'w') as file:
        file.write('x,y\n')
        for item_x, item_y in zip(x, y):
            file.write(f'{item_x},{item_y}\n')


def read_points(file_name):
    return pd.read_csv(file_name)


def centroids(points, k, m):
    centrs = [[], []]

    for i in range(k):
        sum_x = 0
        sum_y = 0
        for x, y, cluster in zip(points['x'], points['y'], points[f'cluster_0_{i}']):
            sum_x += x * pow(cluster, m)
            sum_y += y * pow(cluster, m)

        sum_u = 0
        for index, point in points.iterrows():
            sum_u += pow(point[f'cluster_0_{i}'], m)

        centrs[0].append(sum_x / sum_u)
        centrs[1].append(sum_y / sum_u)

    return centrs


def calculate_relations(points, centrs, k, m):
    power = 2 / (1 - m)

    sums = []
    for i in range(k):
        sums.append([])

    for index, point in points.iterrows():
        distances = []
        for i in range(k):
            distances.append(dist(point['x'], point['y'], centrs[0][i], centrs[1][i]))

        for i in range(k):
            sum = 0
            for j in range(k):
                if distances[j] != 0.0:
                    sum += pow(distances[i] / distances[j], power)
                else:
                    sum += 0
            sums[i].append(sum)

    for i in range(k):
        points[f'cluster_1_{i}'] = sums[i]


def difference(points, k, e):
    difference_count = []
    for i in range(k):
        cluster_0 = []
        cluster_1 = []
        for index, point in points[f'cluster_0_{i}'].iteritems():
            cluster_0.append(float(point))

        for index, point in points[f'cluster_1_{i}'].iteritems():
            cluster_1.append(float(point))

        count = 0
        for i, j in zip(cluster_0, cluster_1):
            if abs(i - j) > e:
                count += 1
        difference_count.append(count)
    return sum(difference_count)


def replace(points, k):
    for i in range(k):
        points[f'cluster_0_{i}'] = points[f'cluster_1_{i}']
        points.drop(f'cluster_1_{i}', axis=1)


def fit_relations(points, k):
    n = len(points['x'])

    for i in range(k):
        points[f'cluster_0_{i}'] = [random.random() for i in range(n)]

    summary = []
    for i in range(n):
        sum = 0
        for j in range(k):
            sum += points.iloc[i][f'cluster_0_{j}']
        summary.append(sum)

    for i in range(k):
        points[f'cluster_0_{i}'] = points[f'cluster_0_{i}'] / summary


if __name__ == '__main__':
    n = 100
    k = 3
    m = 1.5
    e = 0.001
    max_iters = 100

    filename = 'points.csv'
    generate_points_file(n, filename)
    points = read_points(filename)

    fit_relations(points, k)

    brk = False
    for i in range(max_iters):
        print(points.head(10))
        centrs = centroids(points, k, m)
        calculate_relations(points, centrs, k, m)
        difference_count = difference(points, k, e)
        replace(points, k)
        if difference_count == 0:
            print(f'Count of iterations = {i}')
            brk = True
            break

    if not brk:
        print(f'The loop has reached the maximum number of iterations = {max_iters}')

    # print(points.head(20))
