import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


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


def centroids(points, k):
    x_center = points['x'].mean()
    y_center = points['y'].mean()

    R = dist(x_center, y_center, points['x'][0], points['y'][0])

    for i in range(len(points)):
        R = max(R, dist(x_center, y_center, points['x'][i], points['y'][i]))

    x_c, y_c = [], []
    for i in range(k):
        x_c.append(x_center + R * np.cos(2 * np.pi * i / k))
        y_c.append(y_center + R * np.sin(2 * np.pi * i / k))

    return [x_c, y_c]


def calculate_relation(points, centroids, k, m):
    for point in points:
        for i in range(k):
            point[f'cluster_{i}'] = di


def new_centroinds(points, k):
    result = [[], []]
    for i in range(k):
        result[0].append(points[points.cluster_2 == i]['x'].mean())

    for i in range(k):
        result[1].append(points[points.cluster_2 == i]['y'].mean())

    return result


def nearest_centroid(points, centroids):
    clusters = []
    for x, y in zip(points['x'], points['y']):
        r = np.inf
        index = 0
        for i in range(0, len(centroids[0])):
            d = dist(centroids[0][i], centroids[1][i], x, y)
            if r > d:
                r = d
                index = i
        clusters.append(index)
    return clusters


def count_difference_rows(points):
    df = points[points.columns[-1]] - points[points.columns[-2]]
    count = 0
    for row in df:
        if row != 0:
            count += 1
    return count


def print_graph(points, centroids, k):
    colors = cm.rainbow(np.linspace(0, 1, k))
    # colors = {
    #     0: 'green',
    #     1: 'blue',
    #     2: 'yellow',
    #     3: 'purple',
    #     4: 'brown',
    #
    # }
    plt.scatter(centroids[0], centroids[1], color='black')
    for i in range(k):
        plt.scatter(points[points.cluster_2 == i]['x'], points[points.cluster_2 == i]['y'], color=colors[i])
    plt.show()


def calculate_j(points, centroids):
    sum = 0

    for x, y, cluster in zip(points['x'], points['y'], points['cluster_2']):
        sum += dist(x, y, centroids[0][cluster], centroids[1][cluster])

    return sum


if __name__ == '__main__':
    n = 100 # количество точек
    # k = 4 # количество кластеров

    filename = 'points.csv'
    generate_points_file(n, filename)
    points = read_points(filename)

    js = {}

    # first_iteration
    centrs = centroids(points, 1)

    points['cluster_1'] = nearest_centroid(points, centrs)
    points['cluster_2'] = nearest_centroid(points, centrs)
    js[1] = calculate_j(points, centrs)

    print_graph(points, centrs, 1)

    new_cents = None

    for k in range(2, int(np.sqrt(n)) + 2):
        new_cents = centroids(points, k)
        points['cluster_2'] = nearest_centroid(points, new_cents)

        # i = 1

        while count_difference_rows(points) != 0:
            points['cluster_1'] = points['cluster_2']
            new_cents = new_centroinds(points, k)
            points['cluster_2'] = nearest_centroid(points, new_cents)

            # print(f'Iteration №{i} | Centroids {new_cents}')
            # i += 1

        # print_graph(points, new_cents, k)
        # print(new_cents)
        j_k = calculate_j(points, new_cents)
        js[k] = j_k

    # print(js)

    ds = {}
    for k in range(2, len(js)):
        ds[k] = abs(js[k] - js[k + 1]) / abs(js[k - 1] - js[k])

    # print(ds)

    value_opt = np.inf
    k_opt = 0
    for key, value in zip(ds.keys(), ds.values()):
        if value_opt > value:
            k_opt = key
            value_opt = value

    new_cents = centroids(points, k_opt)
    points['cluster_2'] = nearest_centroid(points, new_cents)

    while count_difference_rows(points) != 0:
        points['cluster_1'] = points['cluster_2']
        new_cents = new_centroinds(points, k_opt)
        points['cluster_2'] = nearest_centroid(points, new_cents)
        print_graph(points, new_cents, k_opt)

    print_graph(points, new_cents, k_opt)

    print(f'D(k) = {ds}')
    print(f'Optimal k = {k_opt}')
