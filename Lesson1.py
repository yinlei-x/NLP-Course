import random
import networkx
import matplotlib.pyplot as plt



#
# 最后一题
#
print("#1")

#定义语法内容
grammar = """
sentence = adj noun verb adj noun2
adj = adj_single 和 adj_single 的 | null
adj_single = 漂亮  | 蓝色 | 好看
adv = 安静地 | 静静地
noun = 猫 | 女人 | 男人
verb = adv 看着 | adv 坐着 
noun2 = 桌子 | 皮球 
"""

#定义语法创建函数：从语法内容中读取语法规则并映射到创建的字典，键值为声明，值为表达式
def build_grammar(grammar_str, split='='):
    grammar_pattern = {}
    for line in grammar_str.split('\n'):
        if not line: continue
        stmt, expr = line.split(split)
        grammar_pattern[stmt.strip()] = [e.split() for e in expr.split('|')]
    return grammar_pattern

grammar_pattern = build_grammar(grammar)
print(grammar_pattern)


# 定义生成符合某声明的函数：
def generate(grammar_pattern, target):
    if target not in grammar_pattern: return target

    expr = random.choice(grammar_pattern[target])

    tokens = [generate(grammar_pattern, e) for e in expr]  # 递归调用自己，直到表达式中不含有已声明内容

    return ''.join([t for t in tokens if t != 'null'])

print(generate(grammar_pattern, 'sentence'))


#
# A simpler solution
#
print("#2")

def adj(): return random.choice('漂亮 | 蓝色 | 好看'.split('|')).strip()

def noun(): return  random.choice('猫 | 女人 | 男人'.split('|')).strip()

def verb(): return random.choice('看着 | 坐着 '.split('|')).strip()

def noun2(): return random.choice('桌子 | 皮球'.split('|')).strip()

def sentence(): return ''.join([adj(), noun(), verb(), noun2()])


print(sentence())


#
# Search Based Intelligence
#
print("#3")

#定义无向图
graph = {
    'A' :'B B B C',
    'B' : 'A C',
    'C' : 'A B D E',
    'D' : 'C',
    'E' : 'C F',
    'F' : 'E'
}

#去重
for k in graph:
    graph[k] = set(graph[k].split())

#集合通过split后不维持之前的顺序，但也不是随机的
for element in set('1 2 3 4 5 6 7 8 9 10 100000 元素'.split()):
    print(element)

Graph = networkx.Graph(graph)
networkx.draw(Graph, with_labels=True)

plt.show()


#
# Breadth First Search
#
print("#4")

seen=set()
need_visited = ['A']
while need_visited:
    node = need_visited.pop(0)
    if node in seen:
            print('{} has been seen'.format(node))
            continue
    print('   I am looking at : {}'.format(node))
    need_visited += graph[node]
    seen.add(node)


#
# Depth First Search
#
print("#5")

#定义无向长图
graph_long = {
    '1': '2 7',
    '2': '3',
    '3': '4',
    '4': '5',
    '5': '6 10',
    '7': '8',
    '6': '5',
    '8': '9',
    '9': '10',
    '10': '5 11',
    '11': '12',
    '12': '11',
}

for n in graph_long: graph_long[n] = graph_long[n].split()

Graph_long = networkx.Graph(graph_long)
networkx.draw(Graph_long, with_labels=True)

plt.show()



#
# Repetition is the mother of evil
#
print("#6")

print("#6.1")

# 合并广度优先和深度优先解法
def search(graph, concat_func):
    seen = set()
    need_visited = ['1']

    while need_visited:
        node = need_visited.pop(0)
        if node in seen:
            print('{} has been seen'.format(node))
            continue
        print('   I am looking at : {}'.format(node))
        seen.add(node)
        new_discoveried = graph[node]
        need_visited = concat_func(new_discoveried, need_visited)

def treat_new_discover_more_important(new_discoveried, need_visited):
    return new_discoveried + need_visited

def treat_already_discoveried_more_important(new_discoveried, need_visited):
    return need_visited + new_discoveried

print(search(graph_long, treat_already_discoveried_more_important))

print("#6.2")

print(search(graph_long, treat_new_discover_more_important))

print("#6.3")

from functools import partial

dfs = partial(search, concat_func=treat_new_discover_more_important)

print(dfs(graph_long))

print("#6.4")

bfs = partial(search, concat_func=treat_already_discoveried_more_important)
print(bfs(graph_long))


#
# Mapping
#
print("#7")

BJ = 'Beijing'
SZ = 'Shenzhen'
GZ = 'Guangzhou'
WH = 'Wuhan'
HLG = 'Heilongjiang'
NY = 'New York City'
CM = 'Chiangmai'
SG = 'Singapore'

air_route = {
    BJ : {SZ, GZ, WH, HLG, NY},
    GZ : {WH, BJ, CM, SG},
    SZ : {BJ, SG},
    WH : {BJ, GZ},
    HLG : {BJ},
    CM : {GZ},
    NY : {BJ}
}

air_route = networkx.Graph(air_route)

networkx.draw(air_route, with_labels=True)

plt.show()


def search_destination(graph, start, destination):
    pathes = [[start]]
    seen = set()
    chosen_pathes = []
    while pathes:
        path = pathes.pop(0)
        frontier = path[-1]
        if frontier in seen: continue
        # get new lines

        for city in graph[frontier]:
            new_path = path + [city]
            pathes.append(new_path)
            if city == destination: return new_path

        seen.add(frontier)
    return chosen_pathes

def draw_route(cities): return ' ✈️ -> '.join(cities)

print(draw_route(search_destination(air_route, SZ, CM)))

