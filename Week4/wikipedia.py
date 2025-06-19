import sys
import collections

# que,stackを使うためライブラリを使用
from collections import deque

# assertで重みの合計値を確認
# 課題1 2pass
# 課題2 日本がNo1
# 最長経路問題　グラフ探索問題の一般化をよく理解。特にpの選び方。

# クラス名:Wikipedia
# titles = IDとtitleの関係
# links = ID同士の繋がり

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.

    # ページタイトルからIDを取得する関数
    def getIdFromTitles(self,input_title):
        titles = self.titles
        for id,title in titles.items():
            if title == input_title:
                return id
            elif id == len(titles):
                print(f"{input_title} is Not found")
                exit(1)

    def find_shortest_path(self, start, goal):
        # start/goalのIDを取得
        startID = self.getIdFromTitles(start)
        goalID = self.getIdFromTitles(goal) 

        stack = deque()
        visited = {}
        links = self.links
        visited[startID] = True
        # IDと距離を保存
        stack.append((startID,0))
        while stack:
            current_id,current_distance = stack.popleft()

            if current_id == goalID:
                print(f"The shortest path between {start} and {goal} is {current_distance}")
                return current_distance
            # currentノードがgoalと一致しなければ、distanceを1増やす
            current_distance += 1
            for child in links[current_id]:
                if not child in visited:
                    visited[child] = True
                    stack.append((child,current_distance))
        return "Not found"

    # ページランクtop10を求める関数
    def top_10_ranks(self,dictionary):
        roop_cnt = 0
        while roop_cnt < 10 and 0 < len(dictionary):
            max_rank = 0
            max_id = []
            for id in dictionary.keys():
                current_rank = dictionary[id]
                if max_rank < current_rank:
                    max_rank = current_rank
                    max_id = [id]
                elif max_rank == current_rank:
                    max_id.append(id)

            titles = self.titles
            max_titles = []
            for id in max_id:
                del dictionary[id]
                max_titles.append(titles[id])

            print(f"ページランク{roop_cnt+1}位は{max_titles}、ページランクは{max_rank}です")
            roop_cnt += 1


    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        links = self.links
        # 全てのnodeの数を保持
        all_node = len(self.titles)

        # 現在のページランクとIDの関係を保存する辞書
        current_page_ranks = {}
        # 次のページランクとIDの関係を保存する辞書
        next_page_ranks = {}

        for id in links.keys():
            current_page_ranks[id] = 1
            next_page_ranks[id] = 0

        # 各IDが持つ隣接リンクの個数
        link_count = {}

        for id,link in links.items():
            link_count[id] = len(link)



        # page_rankを更新
        while True:
            all_pagerank = 0

            # 孤立点のpage rankをカウント
            no_link_pagerank = 0
            for id,link in links.items():
                if len(link) == 0:
                    no_link_pagerank += current_page_ranks[id]

            for id in links:
                current_page_rank = current_page_ranks[id]
                current_link_count = link_count[id]
                # 無条件で0.15を保持
                next_page_ranks[id] += 0.15 + (no_link_pagerank / all_node) * 0.85

                
                # 隣接ノードを持たない場合は、全ノードに0.85を分配
                

                '''
                else:
                    for link_id in links[id]:
                        next_page_ranks[link_id] += current_page_rank * 0.85 / current_link_count
                '''
                for link_id in links[id]:
                    next_page_ranks[link_id] += current_page_rank * 0.85 / current_link_count

            # 収束判定
            # 前回との差
            difference_ranks = 0
            for id in links:
                difference_ranks += (current_page_ranks[id] - next_page_ranks[id])**2
                #print("id:",id,difference_ranks,current_page_ranks[id],next_page_ranks[id])
                all_pagerank += next_page_ranks[id]

            if difference_ranks < 0.01:
                self.top_10_ranks(next_page_ranks)
                break

            current_page_ranks = next_page_ranks.copy()

            for id in links.keys():
                next_page_ranks[id] = 0
            # ページランクが保存しているか確認
            print(all_pagerank,all_node)
            assert(all_pagerank - all_node < 0.001)

    
    


    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    # HW2の関数が使えそう
    def find_longest_path(self, start, goal):
        startID = self.getIdFromTitles(start)
        goalID = self.getIdFromTitles(goal) 

        queue = deque()
        visited = {}
        links = self.links
        visited[startID] = True
        # IDとpathと距離を保存
        queue.append((startID,[startID],0))

        # 最長pathを保存するリスト
        longest_path = []
        max_length = -1
        end_cnt = 0

        while queue:
            current_id,current_path,current_distance = queue.pop()
            # popしたタイミングでvisitに変更
            visited[current_id] = True

            if current_id == goalID:
                print(current_path)
                if current_distance > max_length:
                    longest_path = current_path.copy()
                    max_length = current_distance
                    end_cnt += 1
                    # max_lengthを10回更新したら終了
                    if end_cnt == 10:
                        break
                    continue

            # currentノードがgoalと一致しなければ、distanceを1増やす
            current_distance += 1
            for child in links[current_id]:
                if not child in visited:
                    queue.append((child,current_path + [child],current_distance))

        if longest_path:
            self.assert_path(longest_path,start,goal)
            print(f"The longest path between {start} and {goal} is {max_length}")
            return longest_path
        return "Not found"
        


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])



if __name__ == "__main__":
    pages_file_name = "pages_large.txt"
    links_file_name = "links_large.txt"
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    #wikipedia.find_longest_titles()
    # Example
    #wikipedia.find_most_linked_pages()

    # Homework #1
    #wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_shortest_path("渋谷", "小野妹子")
    #wikipedia.find_shortest_path("A", "B")
    
    # Homework #2
    #wikipedia.find_most_popular_pages()
    
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")
    