#遺伝アルゴリズム

import math
import random
import copy
import matplotlib.pyplot as plt

#要素数
num = 37
#個体数
pop_num = 200
#世代数
generation_num = 200
#トーナメントサイズ
tournament_size = 10
#トーナメントサイズで選択する個体数
tournament_select_num = 2
#エリート主義で選択する個体数
elite_select_num = 1
#交叉確率
crossover_prob = 50
#突然変異確率
mutation_prob = 3

def city_info(num, pop_num):
    x_cityinfo = [23,8,34,12,42,6,1,12,4,13,23,7,11,6,28,10,3,4,3]
    y_cityinfo = [39,44,36,30,37,35,15,25,39,42,13,39,5,44,45,7,16,19,39]
    x_cityinfo2 = [23,0,19,5,8,20,2,20,16,24,9,5,30,2,21,22,3,11,14]
    y_cityinfo2 = [39,2,21,43,34,39,50,26,36,30,40,22,35,0,36,28,33,36,34]

    cityinfo = [[x_cityinfo[i],y_cityinfo[i]] for i in range(num/2+1)]
    cityinfo2 = [[x_cityinfo2[i],y_cityinfo2[i]] for i in range(num/2+1)]
    position_info = {}
    position_info2 = {}
    for i in range(num):
        position_info[i] = cityinfo[i]
        position_info2[i] = cityinfo2[i]

    #初期の巡回順序作成
    select_num = [i for i in range(num/2+1)]
    all_route = [random.sample(select_num, num/2+1) for _ in range(pop_num)]

    return position_info, position_info2, all_route

def evaluate(position_info, all_route, loop=0):
    """ ユークリッド距離の総和を計算し評価値とする。 """

    evaluate_value = []
    for i in range(len(all_route)):
        temp_evaluate_value = []
        x_coordinate = [position_info[all_route[i][x]][0] for x in range(len(all_route[i]))]
        y_coordinate = [position_info[all_route[i][y]][1] for y in range(len(all_route[i]))]
        for j in range(len(all_route[i])):
            if j == len(all_route[i]) - 1:
                distance = math.sqrt(
                    pow((x_coordinate[j] - x_coordinate[0]), 2) + pow((y_coordinate[j] - y_coordinate[0]), 2))
            else:
                distance = math.sqrt(
                    pow((x_coordinate[j] - x_coordinate[j + 1]), 2) + pow((y_coordinate[j] - y_coordinate[j + 1]), 2))
            temp_evaluate_value.append(distance)
        evaluate_value.append(sum(temp_evaluate_value))

    # 一番優秀な個体をmatplotで描画
    excellent_evaluate_value = min(evaluate_value)
    draw_pop_index = evaluate_value.index(excellent_evaluate_value)

    show_route(position_info, all_route[draw_pop_index],int(excellent_evaluate_value), loop=loop + 1)

    return evaluate_value

def selection(all_route, evaluate_value, tournament_select_num, tournament_size, elite_select_num, ascending=False):
    """ トーナメント選択とエリート保存を行う"""

    select_pop = []
    elite_pop = []
    # トーナメント選択
    while True:
        select = random.sample(evaluate_value, tournament_size)
        select.sort(reverse=ascending)
        for i in range(tournament_select_num):
            value = select[i]
            index = evaluate_value.index(value)
            select_pop.append(all_route[index])

        # 個体数の半数個選択するまで実行
        if len(select_pop) >= len(all_route) / 2:
            break

    # エリート保存
    sort_evaluate_value = copy.deepcopy(evaluate_value)
    sort_evaluate_value.sort(reverse=ascending)
    for i in range(elite_select_num):
        value = sort_evaluate_value[i]
        index = evaluate_value.index(value)
        elite_pop.append(all_route[index])

    return select_pop, elite_pop

def crossover(select_pop, crossover_prob):
    ''' 確率的に順序交叉を実行する '''

    cross_pop = random.sample(select_pop, 2)
    pop_1 = cross_pop[0]
    pop_2 = cross_pop[1]

    check_prob = random.randint(0, 100)
    if check_prob <= crossover_prob:

        # 順序交叉
        new_pop_1 = []
        cut_index = random.randint(1, len(pop_1) - 2)
        new_pop_1.extend(pop_1[:cut_index])
        for i in range(len(pop_1)):
            if pop_2[i] not in new_pop_1:
                new_pop_1.append(pop_2[i])

        new_pop_2 = []
        new_pop_2.extend(pop_1[cut_index:])
        for i in range(len(pop_1)):
            if pop_2[i] not in new_pop_2:
                new_pop_2.append(pop_2[i])

        return new_pop_1, new_pop_2

    else:
        return pop_1, pop_2

def mutation(pop, mutation_prob):
    """ 循環経路の順番をランダムで入れ替える """

    check_prob = random.randint(0, 100)

    if check_prob <= mutation_prob:
        select_num = [i for i in range(num)]
        select_index = random.sample(select_num, 2)

        a = pop[select_index[0]]
        b = pop[select_index[1]]
        pop[select_index[1]] = a
        pop[select_index[0]] = b

    return pop

def show_route(position_info, route, excellent_evaluate_value,  loop=0):
    """ matplotlibで循環経路を描画 """

    x_coordinate = [position_info[route[i]][0] for i in range(len(route))]
    y_coordinate = [position_info[route[i]][1] for i in range(len(route))]
    x_coordinate.append(position_info[route[0]][0])
    y_coordinate.append(position_info[route[0]][1])

    plt.scatter(x_coordinate, y_coordinate)
    plt.plot(x_coordinate, y_coordinate, label=excellent_evaluate_value)
    plt.title("Generation: {}".format(loop))
    plt.legend()

    plt.savefig("img/tsp{}".format(loop))  # pngとして保存。カレントディレクトリにimgフォルダを置く必要あり。
    plt.show()


if __name__ == "__main__":
    #書き写しと初期ルート作成
    position_info, position_info2, all_route = city_info(num, pop_num)
    #評価
    evaluate_value  = evaluate(position_info, all_route)
    evaluate_value2 = evaluate(position_info2,all_route)

    for loop in range(generation_num):
        #選択
        select_pop, elite_pop = selection(
            all_route, evaluate_value, tournament_select_num, tournament_size, elite_select_num, ascending=False
        )
        select_pop2, elite_pop2 = selection(
            all_route, evaluate_value2, tournament_select_num, tournament_size, elite_select_num, ascending=False
        )

        #選択した個体の中から2個体交換し交叉や突然変異を適用する
        next_pop  = []
        next_pop2 = []
        while True:
            #交叉
            pop_1, pop_2 = crossover(select_pop, crossover_prob)
            pop_3, pop_4 = crossover(select_pop2,crossover_prob)
            #突然変異
            pop_1 = mutation(pop_1, mutation_prob)
            pop_2 = mutation(pop_2, mutation_prob)
            pop_3 = mutation(pop_3, mutation_prob)
            pop_4 = mutation(pop_4, mutation_prob)

            next_pop.append(pop_1)
            next_pop.append(pop_2)
            next_pop2.append(pop_3)
            next_pop2.append(pop_4)

            if len(next_pop) >= pop_num -elite_select_num:
                break

        #エリート主義
        next_pop.extend(elite_pop)
        next_pop2.extend(elite_pop2)

        #評価
        evaluate_value = evaluate(position_info, next_pop, loop=loop + 1)
        evaluate_value2 = evaluate(position_info2, next_pop2, loop=loop + 1)

        #更新
        all_route = next_pop

    print(all_route)
