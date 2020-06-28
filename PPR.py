from operator import itemgetter


def read_graph(input_file_name):
    with open(input_file_name) as f:
        nodes = set()
        forward = dict()
        backward = dict()
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            v1, v2 = line.strip('\n').split(',')
            nodes.add(v1)
            nodes.add(v2)

            if v1 in forward.keys():
                forward[v1].append(v2)
            else:
                forward[v1] = [v2]
            if v2 in backward.keys():
                backward[v2].append(v1)
            else:
                backward[v2] = [v1]
        return nodes, forward, backward


def read_seed(input_file_name):
    with open(input_file_name) as f:
        seed = dict()
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            v, w = line.strip('\n').split(',')
            seed[v] = float(w)
        return seed


def PPR(input_Graph, input_Seed, damping_factor=0.85, max_iter=100):
    '''
    Personalized PageRank
    '''

    # 读入文件
    nodes, forward, backward = read_graph(input_Graph)
    seed = read_seed(input_Seed)

    # 设置初始状态
    page_rank = dict.fromkeys(nodes, 0)
    for key, val in seed.items():
        page_rank[key] = val

    # 执行幂迭代，“随即游走” Marcov Chain
    for i in range(max_iter):
        delta = 0.0
        for node in nodes:
            rank = 0.0
            if node in backward.keys():
                for v in backward[node]:
                    rank += damping_factor * page_rank[v] / len(forward[v])

            # 个性化
            if node in seed.keys():
                rank += (1 - damping_factor) * seed[node]

            delta += abs(page_rank[node] - rank)
            page_rank[node] = rank

        print("iter:", i, ", delta:", delta)
        # 收敛则退出
        if delta < 1e-10:
            break

    page_rank = list(page_rank.items())
    # 先按字典降序
    ans = sorted(page_rank, key=itemgetter(0), reverse=True)
    # 再按PR值降序
    ans = sorted(ans, key=itemgetter(1), reverse=True)

    node_list = [x[0] for x in ans]
    score_list = [x[1] for x in ans]
    print(node_list[:10])
    print(score_list[:10])
    return node_list


_ = PPR('soc-Epinions-after.txt', 'seed.txt')
