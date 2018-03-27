def classify(statement, codes):
    #print(statement)
    tags = ['グラフ', '数論', '幾何', '動的計画法', 'データ構造', '文字列', '確率・組合せ', 'ゲーム']
    apparent_keys = [['グラフ', '木', 'パス',],
                     [],
                     ['半径',],
                     [],
                     [],
                     ['文字列',],
                     ['確率',],
                     ['プレイ', 'プレイヤー', '勝ち', '負け'],
                    ]
    good_keys =     [['G', 'g', 'Edge', 'edge', 'Graph', 'graph', 'cycle', 'deg', 'dfs', 'tree', 'dijkstra',],
                     ['gcd', 'lcm', 'extgcd', 'prime', 'phi',],
                     ['point', 'points', 'Point', 'Points', 'line', 'Line', 'imag', 'real', 
                      'circle', 'rad', 'Convexhull', 'Intersect', 'intersect',],
                     ['dp',],
                     ['SegmentTree', 'segmenttree', 'segtree', 'seg', 'Segtree', 'Seg', 
                      'FenwickTree', 'fenwicktree', 'Fenwick', 'fenwick', 'bit', 'BIT', 'BinaryIndexedTree', 
                      'UnionFind', 'UF', 'uf', 'unite', 'same', 'unionfind', 'Unionfind',
                      'LazySegmentTree', 'lazy',
                      'update', 'build', 'query',],
                     [],
                     ['C', 'inv', 'Inv', 'fact', 'invfact', 'Fact', 'Invfact', 'choose'],
                     ['grundy', 'gr', 'Alice', 'Bob', 'Takahashi', 'Aoki', 'First', 'Second',
                      'ALICE', 'BOB', 'TAKAHASHI', 'AOKI', 'Draw', 'DRAW',],
                    ]
    not_good_keys = [['gcd', 'r', 'R'],
                     [],
                     [],
                     [],
                     [],
                     [],
                     [],
                     [],
                    ]
    tag_list = []
    for i in range(0, len(tags)):
        ok = False
        for key in apparent_keys[i]:
            if key in statement:
                ok = True
                break
        if not ok:
            yes_cnt = 0
            no_cnt = 0
            for code in codes:
                good = False
                for key in good_keys[i]:
                    if key in code:
                        good = True
                if not good:
                    no_cnt += 1
                else:
                    for key in not_good_keys[i]:
                        if key in code:
                            good = False
                    if not good:
                        no_cnt += 1
                    else:
                        yes_cnt += 1
            if yes_cnt > no_cnt:
                ok = True
        if ok:
            tag_list.append(tags[i])

    if len(tag_list) == 0:
        tag_list.append('その他')
    return tag_list
