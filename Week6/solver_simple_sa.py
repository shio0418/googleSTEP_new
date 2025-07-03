# 焼きなまし法の実装
# input7の実装を終わらせるためだけの、めちゃくちゃランダムなアルゴリズム
# 

import sys
import random
import time
import math

from common import print_tour, read_input, calc_total_length
from solver_greedy import solve as solve_greedy, distance 
from solver_random import solve as solve_random

def solve(cities):
    #D = calc_mean_distance(cities)
    # 温度（時間により減少） 大きめの方が精度高い
    T = 100
    #T = D
    # 減少率
    alpha = 0.99
    # Tの境界
    end_T = 0.001
    # diffが大きくなっても変化する確率の最小値
    #border = 0.1
    N = len(cities)

    # 貪欲法で初期条件
    current_tour = solve_greedy(cities)

    # 境界値
    border = 0.01

    # ランダム法で初期条件（貪欲法より精度低かった）
    #current_tour = list(range(N))
    #random.shuffle(current_tour)

    change = 0
    while T > end_T:
        for i in range(10):
            random_i_list = list(range(N-1))
            random.shuffle(random_i_list)
            
            i = random.randint(0, N-1)
            j = random.randint(0,N-1)
            if i == j:
                j = random.randint(0,N-1)

            a = cities[current_tour[i]]
            b = cities[current_tour[(i+1) % N]]
            c = cities[current_tour[j]]
            d = cities[current_tour[(j+1) % N]]

            diff = distance(a,c) + distance(b,d) - (distance(a,b) + distance(c,d))

            possib = math.exp( - (diff/T))

            if (diff < 0 or possib > border):
                current_tour[i+1:j+1] = reversed(current_tour[i+1:j+1])

        # Tを冷却
        T *= alpha 
    #print(change)
    return current_tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    start = time.time()
    tour = solve(cities)
    end = time.time()
    print_tour(tour)
    total = calc_total_length(cities,tour)
    print("Total length is ",total)
    print("Execution time:",end - start)

