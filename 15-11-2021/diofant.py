import random
from collections import Counter

PAIRS_NUM = 5
ITERATIONS_COUNT = 100


def get_dist(params, coefs, res):
    dist = {}
    for idx, param in enumerate(params):
        sum = 0
        for x, y in zip(param, coefs):
            sum += x * y
        dist[idx] = abs(sum - res)

    return dist


def get_probs(distances):
    sum = 0
    for dist in distances.values():
        sum += 1 / dist

    probs = {}
    for k, v in distances.items():
        probs[k] = (1 / v) / sum

    return probs


def get_parent_pairs(probs):
    parts = {}
    for k, v in probs.items():
        parts[k] = int(v * 100)

    line = []
    for k, v in parts.items():
        for i in range(v):
            line.append(k)

    random.shuffle(line)

    parent_pairs = []
    for _ in range(PAIRS_NUM):
        parents_pair = random.sample(line, 2)
        while parents_pair[0] == parents_pair[1] or parents_pair in parent_pairs:
            parents_pair = random.sample(line, 2)

        parent_pairs.append(parents_pair)

    return parent_pairs


def cross_over(parent_pairs, params):
    cos = []
    for pair in parent_pairs:
        delimiter = random.randint(1, len(params[0]) - 1)
        co = []
        x = params[pair[0]]
        y = params[pair[1]]
        idx = 0
        while idx < delimiter:
            co.append(x[idx])
            idx += 1
        idx = delimiter
        while idx < len(params[0]):
            co.append(y[idx])
            idx += 1
        cos.append(co)
    return cos


def duplicates_exist(params):
    p = []
    for param in params:
        p.append(tuple(param))
    cnt = Counter(p)
    count = 0
    for value in cnt.values():
        if value > 1:
            count += value

    return False if count < PAIRS_NUM // 2 else True


def solve(coefs, res):
    best_solution = None
    params = None
    found = False

    it = 1
    while not found and it <= ITERATIONS_COUNT:
        print('--------------')
        print(f'Поколение {it}')
        print('--------------')
        if params is None:
            params = []
            for i in range(PAIRS_NUM):
                p = []
                for _ in range(len(coefs)):
                    p.append(random.randint(1, res + 1))
                params.append(p)
        print('Родители')
        for param in params:
            print(param)

        if duplicates_exist(params):
            print(f'Более половины родителей повторяются. Поиск остановлен')
            return best_solution

        # Отклонения
        distances = get_dist(params, coefs, res)

        # Вероятности выживаемости
        probs = get_probs(distances)

        # Родительские пары, основанные на вероятности выживаемости
        parent_pairs = get_parent_pairs(probs)
        print(parent_pairs)

        print('Потомки')
        cos = cross_over(parent_pairs, params)
        for co in cos:
            print(co)

        # Коэффициенты выживаемости
        live_coefs = get_dist(cos, coefs, res)

        if best_solution is None:
            best_solution = (list(live_coefs.keys())[0], live_coefs[list(live_coefs.keys())[0]])
        for k, v in live_coefs.items():
            if v == 0:
                found = True
                best_solution = (cos[k], v)
                break

            if best_solution[1] > v:
                best_solution = (cos[k], v)

        params = cos
        it += 1

    return best_solution


if __name__ == '__main__':
    coefs = [int(i) for i in input().split(' ')]
    result = int(input())
    solution = solve(coefs, result)
    if solution[1] != 0:
        print(f'Самое лучшее решение - {solution[0]} с отклонением {solution[1]}')
    else:
        print(f'Решение найдено - {solution[0]}')
