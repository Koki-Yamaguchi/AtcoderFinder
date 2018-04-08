import requests, re, webbrowser, glob, sqlite3, time, json, sys, io, codecs
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer
from operator import itemgetter
import classifier
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

#FOR DEBUG
CODES_PER_PROBLEM = 10
RANGE_LEFT = 2          
RANGE_RIGHT = 3
MAKE_DATABASE = True

def get_all_data(type):
    html = requests.get('http://kenkoooo.com/atcoder/atcoder-api/info/problems')
    soup = BeautifulSoup(html.text, 'lxml')
    json_data_raw = soup.find("p").string
    json_dict = json.loads(json_data_raw, encoding = 'utf-8')
    pat = ['agc', 'abc', 'arc', 'apc']
    if type == 0 or type == 2 or type == 3:
        res = []
        cnt = 0
        for data in json_dict:
            '''
            d = data['id'][0:6]
            if d == 'arc015':
                res.append([data['id'], data['contest_id'], data['title']])
            continue
            '''
            if data['id'][0:3] == pat[type]:
                res.append([data['id'], data['contest_id'], data['title']])
                cnt += 1
        res.sort()
        return res
    elif type == 4:
        res = []
        for data in json_dict:
            t = data['id'][0:3]
            if t not in pat:
                res.append([data['id'], data['contest_id'], data['title']])
        res.sort(key = lambda x:(x[1],x[2]))
        return res
    elif type == 1: #ABC
        res = []
        for number in range(1, 10000):
            numstr = str(number)
            if len(numstr) == 1:
                numstr = '00' + numstr
            elif len(numstr) == 2:
                numstr = '0' + numstr
            url = 'https://beta.atcoder.jp/contests/abc' + numstr + '/tasks'
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'lxml')
            tab= soup.table
            if tab == None:
                break
            elems = tab.find_all('a')
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
                            break
                        elif data['id'][0:3] == 'arc':
                            if data['id'][-1] == 'a' or data['id'][-1] == 'b':
                                res.append([data['id'], data['contest_id'], data['title']])
                                break
        return res
    else:
        assert false

def tokenize(text):
    list = []
    #t = Tokenizer("/usr/share/nginx/html/userdic.csv", udic_enc="utf8")
    t = Tokenizer("./userdic.csv", udic_enc="utf8")
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
    #stop_words = codecs.open('/usr/share/nginx/html/stop_words.txt', 'r', 'utf-8')
    stop_words = codecs.open('./stop_words.txt', 'r', 'utf-8')
    result = [word for word in texts if word not in stop_words]
    stop_words.close()
    return result

def get_statement(data):
    url = 'https://beta.atcoder.jp/contests/' + data[1] + '/tasks/' + data[0]
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
    words2 = []
    for i in range(1, len(words)):
        if words[i - 1] != 'include':
            words2.append(words[i])
    return words2

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
            if cnt >= CODES_PER_PROBLEM:
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

def make_database(tag_list, type):
    pat = ["AGC", "ABC", "ARC", "APC", "Others"]
    '''
    #sql = sqlite3.connect('/usr/share/nginx/html/database/problems.db')
    sql = sqlite3.connect('./database/problems3.db')
    sql.execute("delete from " + pat[type])
    sql.commit()
    sql.close()
    '''
    for data_tags in tag_list:
        d = data_tags[0]
        url = 'https://beta.atcoder.jp/contests/' + d[1] + '/tasks/' + d[0]
        problem_id = d[0]
        tags0 = ' '.join(data_tags[1])
        tags1 = ' '.join(data_tags[2])
        name = d[2][3:]
        id = ''
        if type == 0 or type == 2 or type == 3:
            id = id + d[0][0:3].upper() + ' ' + d[0][3:6] + ' ' + d[2][0]
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
        data = [problem_id, id, name, url, tags0, tags1]
        if not MAKE_DATABASE:
            continue
        #sql = sqlite3.connect('/usr/share/nginx/html/database/problems.db')
        sql = sqlite3.connect('./database/problems3.db')
        sql.execute("create table if not exists " + pat[type] + "(problem_id, id, name, url, tags0, tags1)")
        sql.execute("insert into " + pat[type] + " values(?, ?, ?, ?, ?, ?)", data)
        sql.commit()
        sql.close()

if __name__ == '__main__':
    for type in range(RANGE_LEFT, RANGE_RIGHT): #AGC:0, ABC:1, ARC:2, APC:3, Others:4
        all_data = get_all_data(type) #[[id, contest_id, title], ... ]
        if type == 1:
            for i in range(0, len(all_data)):
                if all_data[i][1][0:3] == 'arc':
                    all_data[i][1] = all_data[i - 2][1]
        if type == 2:
            for data in all_data:
                data[1] = data[0][0:6]
        tag_list = [] #[[data, [tag0_0, tag0_1, ...], [tag1_0, tag1_1, ...]], [data, ...]]
        for data in all_data:
            statement = get_statement(data)
            if len(statement) == 0:
                continue
            codes = get_codes(data)
            tags0 = classifier.classify(statement, codes)
            tags1 = classifier.classify_code(codes)
            print(data[0], tags0, tags1, flush=True)
            tag_list.append([data, tags0, tags1])
        make_database(tag_list, type)
    print("Success")
