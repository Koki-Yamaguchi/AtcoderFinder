import requests, re, webbrowser, glob, sqlite3, time, json, sys, io
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def get_all_data(type):
    #'''get json from the web and write it to local file
    html = requests.get('http://kenkoooo.com/atcoder/atcoder-api/info/problems')
    soup = BeautifulSoup(html.text, 'lxml')
    json_data_raw = soup.find("p").string
    #with open('/usr/share/nginx/html/json/problems.json', mode = 'w', encoding = 'utf-8') as file:
    with open('./json/problems.json', mode = 'w', encoding = 'utf-8') as file:
        file.write(json_data_raw)
    #'''
    #json_data = open('/usr/share/nginx/html/json/problems.json', 'r')
    json_data = open('./json/problems.json', 'r')
    json_dict = json.load(json_data)

    if type == 0 or type == 2 or type == 3: #AGC or ARC or APC
        res = []
        for number in range(1, 3):
            numstr = str(number)
            if len(numstr) == 1:
                numstr = '00' + numstr
            elif len(numstr) == 2:
                numstr = '0' + numstr
            if type == 0:
                for data in json_dict:
                    if data['id'][0:6] == 'agc' + numstr:
                        res.append([data['id'], data['contest_id'], data['title']])
            elif type == 2:
                for data in json_dict:
                    if data['id'][0:6] == 'arc' + numstr:
                        res.append([data['id'], data['contest_id'], data['title']])
            elif type == 3:
                for data in json_dict:
                    if data['id'][0:6] == 'apc' + numstr:
                        res.append([data['id'], data['contest_id'], data['title']])
        res.sort()
        return res

    elif type == 1: #ABC
        res = []
        for number in range(1, 91):
            numstr = str(number)
            if len(numstr) == 1:
                numstr = '00' + numstr
            elif len(numstr) == 2:
                numstr = '0' + numstr
            url = 'https://beta.atcoder.jp/contests/abc' + numstr + '/tasks'
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'lxml')
            elems = soup.table.find_all('a')
            cnt = 0
            titles = []
            char = ''
            for e in elems:
                cnt += 1
                if cnt % 2 == 0:
                    titles.append(char + '. ' + e.string)
                else:
                    char = e.string
            for title in titles:
                for data in json_dict:
                    if data['title'] == title:
                        if data['id'][0:3] == 'abc':
                            res.append([data['id'], data['contest_id'], data['title']])
                            print(data)
                            break
                        elif data['id'][0:3] == 'arc':
                            if data['id'][-1] == 'a' or data['id'][-1] == 'b':
                                res.append([data['id'], data['contest_id'], data['title']])
                                print(data)
                                break
        return res
    elif type == 4:
        res = []
        cnt = 0
        ub = 50000
        for data in json_dict:
            if cnt > ub:
                break
            t = data['id'][0:3]
            if t != 'agc' and t != 'abc' and t != 'arc' and t != 'apc':
                res.append([data['id'], data['contest_id'], data['title']])
                cnt += 1
        res.sort()
        print(len(res))
        return res
    else:
        assert false

def tokenize(text):
    list = []
    t = Tokenizer()
    tokens = t.tokenize(text)
    for token in tokens:
        s = str(token.surface)
        large = True
        for char in s:
            if ord(char) < 128:
                large = False
                break
        if large and token.part_of_speech.split(',')[0] == u'名詞' and token.part_of_speech.split(',')[1] != u'数':
            list.append(s)
    return list

def clean_ja(texts):
    #stop_words_filename = glob.glob('/usr/share/nginx/html/stop_words.txt')
    stop_words_filename = glob.glob('./stop_words.txt')
    f = open(stop_words_filename[0])
    stop_words = f.read()
    result = [word for word in texts if word not in stop_words]
    return result

def get_statement(data):
    url = 'https://beta.atcoder.jp/contests/' + data[1] + '/tasks/' + data[0]
    print(url)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    all_text = soup.find("div", {"id" : "task-statement"})
    get_statement = all_text.find("section")
    if get_statement == None:
        return []
    statement = get_statement.text
    tokenized_statement = tokenize(statement)
    clean_statement = clean_ja(tokenized_statement)
    return clean_statement

def get_stop_words():
    stop_words = ['int', 'double', 'bool', 'include', 'for', 'if', 'else', 'while', 'continue', 'break', 
                  'return', 'namespace', 'algorithm', 'iostream', 'bits', 'std', 'cstdio', 'c', 'h',
                  'typedef', 'define', 'struct', 'using', 'min', 'max', 'const',
                  ]
    return stop_words

def get_words(code):
    words = []
    str = ""
    for w in code:
        if not w.isalpha():
            if str != "":
                words.append(str)
                str = ""
        elif w.isalpha():
            str = str + w
    if str != "":
        words.append(str)
    return words

def clean(words, stop_words):
    clean_words = []
    for w in words:
        if w not in stop_words:
            clean_words.append(w)
    return clean_words

def get_codes(data):
    all_url = 'https://beta.atcoder.jp/contests/' + data[1] + '/submissions?f.Task=' + data[0] + '&f.Language=3003&f.Status=AC&f.User=&page='
    page_number = 1
    submissions_url = []
    upper_bound = 5 #the number of codes to check
    cnt = 0
    end = False
    while not end:
        cur_url = all_url + str(page_number)
        html = requests.get(cur_url)
        soup = BeautifulSoup(html.text, 'lxml')
        elems = soup.find_all("a", text = re.compile("Detail"))
        if len(elems) == 0:
            break
        for e in elems:
            suburl = e.attrs['href']
            submissions_url.append('https://beta.atcoder.jp' + suburl)
            cnt += 1
            if cnt >= upper_bound:
                end = True
                break
        page_number += 1
    codes = []
    for url in submissions_url:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        elems = soup.select("#submission-code")
        codes.append([url, elems[0].getText()])
    stop_words = get_stop_words()
    clean_codes = []
    for url_code in codes:
        words = get_words(url_code[1])
        unique_words = list(set(words))
        clean_words = clean(unique_words, stop_words)
        clean_codes.append(clean_words)
    return clean_codes

def classify(statement, codes):
    print(statement)
    tags = ['グラフ', '数論', '幾何', '動的計画法', 'データ構造', '文字列', '確率・組合せ', 'ゲーム']
    apparent_keys = [['グラフ', '木', '連結', '辺', '頂点', 'パス',],
                     [],
                     ['半径',],
                     [],
                     [],
                     ['文字列',],
                     ['確率',],
                     ['ゲーム', 'プレイ', 'プレイヤー', '勝ち', '負け'],
                    ]
    good_keys =     [['G', 'g', 'Edge', 'edge', 'Graph', 'graph', 'cycle', 'deg', 'dfs', 'tree', 'dijkstra',],
                     ['gcd', 'lcm', 'extgcd', 'prime', 'phi',],
                     ['point', 'points', 'Point', 'Points', 'line', 'Line', 'imag', 'real', 
                      'circle', 'rad', 'EPS', 'eps', 'Convexhull', 'Intersect', 'intersect',],
                     ['dp',],
                     ['SegmentTree', 'segmenttree', 'segtree', 'seg', 'Segtree', 'Seg', 
                      'FenwickTree', 'fenwicktree', 'Fenwick', 'fenwick', 'bit', 'BIT', 'BinaryIndexedTree', 
                      'UnionFind', 'UF', 'uf', 'unite', 'same', 'unionfind', 'Unionfind',
                      'LazySegmentTree', 'lazy',
                      'update', 'build', 'query',],
                     [],
                     ['C', 'inv', 'Inv', 'fact', 'invfact', 'Fact', 'Invfact', 'choose', 'mod', 'MOD'],
                     ['grundy', 'g', 'gr', 'Alice', 'Bob', 'Takahashi', 'Aoki', 'First', 'Second',
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

def make_database(tag_list, type):
    #sql = sqlite3.connect('/usr/share/nginx/html/database/problems.db')
    sql = sqlite3.connect('./database/problems.db')
    if type == 0:
        sql.execute("delete from AGC")
    if type == 1:
        sql.execute("delete from ABC")
    if type == 2:
        sql.execute("delete from ARC")
    if type == 3:
        sql.execute("delete from APC")
    if type == 4:
        sql.execute("delete from Others")
    sql.commit()
    sql.close()
    for data_tags in tag_list:
        d = data_tags[0]
        url = 'https://beta.atcoder.jp/contests/' + d[1] + '/tasks/' + d[0]
        problem_id = d[0]
        tags = ' '.join(data_tags[1])
        name = d[2][3:]

        id = ''
        if type == 0 or type == 2 or type == 3:
            id = id + d[1][0:3].upper() + ' ' + d[1][3:] + ' ' + d[2][0]
        if type == 1:
            id = id + d[1][0:3].upper() + ' ' + d[1][3:]
            if d[0][0:3] == 'arc':
                if d[0][len(d[0]) - 1:] == 'a':
                    id = id + ' C'
                else:
                    id = id + ' D'
            else:
                id = id + ' ' + d[2][0].upper()
        elif type == 4:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'lxml')
            title = soup.find("a", class_="contest-title").string
            id = title + ' ' + d[2][0]

        print(problem_id, id, name, url, tags)

        data = [problem_id, id, name, url, tags]

        #sql = sqlite3.connect('/usr/share/nginx/html/database/problems.db')
        sql = sqlite3.connect('./database/problems.db')
        if type == 0:
            sql.execute("create table if not exists AGC(problem_id, id, name, url, tags)")
            sql.execute("insert into AGC values(?, ?, ?, ?, ?)", data)
        elif type == 1:
            sql.execute("create table if not exists ABC(problem_id, id, name, url, tags)")
            sql.execute("insert into ABC values(?, ?, ?, ?, ?)", data)
        elif type == 2:
            sql.execute("create table if not exists ARC(problem_id, id, name, url, tags)")
            sql.execute("insert into ARC values(?, ?, ?, ?, ?)", data)
        elif type == 3:
            sql.execute("create table if not exists APC(problem_id, id, name, url, tags)")
            sql.execute("insert into APC values(?, ?, ?, ?, ?)", data)
        elif type == 4:
            sql.execute("create table if not exists Others(problem_id, id, name, url, tags)")
            sql.execute("insert into Others values(?, ?, ?, ?, ?)", data)
        sql.commit()
        sql.close()

if __name__ == '__main__':
    for type in range(0, 1): #AGC:0, ABC:1, ARC:2, APC:3, Others:4
        all_data = get_all_data(type) #[[id, contest_id, title], ... ]
        if type == 1:
            for i in range(0, len(all_data)): #modify the contest_id
                if all_data[i][1][0:3] == 'arc':
                    all_data[i][1] = all_data[i - 2][1]
        tag_list = [] #[[data, [tag0, tag1, ...]], ...]
        for data in all_data:
            print(data)
            statement = get_statement(data)
            if len(statement) == 0:
                print("continue")
                continue
            codes = get_codes(data)
            tags = classify(statement, codes)
            tag_list.append([data, tags])
        make_database(tag_list, type)
