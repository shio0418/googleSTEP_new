#!/usr/bin/env python3

# 近いやつに絞る
import sys
import time

from common import print_tour, read_input, calc_total_length
from solver_greedy import solve as solve_greedy, distance 

def make_dist_list (N,cities):
    dist = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            dist[i][j] = distance(cities[i],cities[j])
            dist[j][i] = dist[i][j]
    return dist

def search_near_cities(N,dist,border):
    near_cities_list = [[] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i != j and dist[i][j] < border:
                near_cities_list[i].append(j)
    return near_cities_list


def solve(cities):
    N = len(cities)
    border_dist = 150
    
    current_tour = solve_greedy(cities)
    # 経路に変化があったか示すフラグ
    changed = True
    
    # 各都市の距離を保存するリスト
    dist = make_dist_list(N, cities)
    print("dist has be created")
    # 各都市における近接都市のみを保持したリスト
    near_cities_list = search_near_cities(N, dist, border_dist)
    print("near_cities_list has be created")
    # print(near_cities_list)


    # 2opt
    while changed:

        changed = False
        # 変化量
        best_diff = 0
        # 交換すべきiとj
        best_i = -1
        best_j = -1
        for i in range(N-1):
            a = current_tour[i]
            b = current_tour[(i+1) % N]
            # 近しいところのみ探索
            for j in near_cities_list[a]:
                if j <= i + 1:
                    continue
                c = current_tour[j]
                d = current_tour[(j+1) % N]
                diff = dist[a][c] + dist[b][d] - (dist[a][b] + dist[c][d])

                if diff < best_diff:
                    best_diff = diff
                    changed = True
                    best_i = i
                    best_j = j
        if changed:
            current_tour[best_i+1:best_j+1] = reversed(current_tour[best_i+1:best_j+1])
        print(calc_total_length(cities,current_tour))
                
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

