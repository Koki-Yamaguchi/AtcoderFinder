import sqlite3

def fixed_part1():
    print("""<!DOCTYPE html>
<html>
<head>
    <title>Atcoder Finder</title>
    <meta charset="UTF-8">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.3.0/dist/semantic.min.js"></script>
    <script defer src="https://use.fontawesome.com/releases/v5.0.8/js/all.js"></script>
    <script src="./js/filter.js"></script>
    <script src="./js/top.js"></script>
    <script src="./js/reactive_judge.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.3.0/dist/semantic.min.css">
    <link rel="stylesheet" href="./css/style.css">
</head>
<body>
    <p id="page-top"><a href="#wrap">トップに戻る</a></p>

    <div class="ui inverted menu">
        <a class="active item">
            <h3>Atcoder Finder</h3>
        </a>
        <a class="active item" href="https://github.com/Koki-Yamaguchi/Koki-Yamaguchi.github.io">
            <h3>Source</h3>
        </a>
    </div>
    <div class="ui container">""")

def form():
    print("""
    <form id="userid">
        <div class="ui action input">
            <input autocomplete="off" type="text" name="user" value="" placeholder="Search user ID" />
            <button class="ui icon button" type="submit" id="btn">
                <i class="search icon"></i>
            </button>
        </div>
    </form>
""")

def filter():
    tags = ['グラフ', '数論', '幾何', '動的計画法', 'データ構造', '文字列', '確率・組合せ', 'ゲーム', 'その他']
    print("        <h4 class='ui top attached header'>タグを選ぶ</h4>")
    print("        <div class='ui attached segment'>")
    print("            <div class='filter-container'>")
    print("                <div class='filters ui form'>")
    print("                    <div class='inline fields'>")
    for i in range(len(tags)):
        print("                        <div class='field'>")
        print("                            <div class='ui checkbox'>")
        print("                                <input type='checkbox' name='タグ' placeholder='タグ' value='" + tags[i] + "' id = 'tag" + str(i) + "'><label for='tag" + str(i) + "'>" + tags[i] + "</label>")
        print("                            </div>")
        print("                        </div>")
    print("                    </div>")
    print("                </div>")
    print("            </div>")
    print("        </div>")

def table(type):
    if type == 0:
        print("        <h3 class='ui block header'>Atcoder Grand Contest</h3>")
    elif type == 1:
        print("        <h3 class='ui block header'>Atcoder Beginner Contest</h3>")
    elif type == 2:
        print("        <h3 class='ui block header'>Atcoder Regular Contest</h3>")

    print("""        <table class="ui striped table">
            <thead>
                <tr>
                    <th>問題番号</th>
                    <th>問題名</th>
                    <th>タグ</th>
                </tr>
            </thead>""")
    print("            <tbody>")


    sql = sqlite3.connect('./database/problems.db')
    cur = sql.cursor()
    if type == 0:
        cur.execute("SELECT * FROM sqlite_master where type='table' and name='AGC'")
        ok = cur.fetchone()
        if ok != None:
            cur.execute('select * from AGC')
    elif type == 1:
        cur.execute("SELECT * FROM sqlite_master where type='table' and name='ABC'")
        ok = cur.fetchone()
        if ok != None:
            cur.execute('select * from ABC')
    else:
        cur.execute("SELECT * FROM sqlite_master where type='table' and name='ARC'")
        ok = cur.fetchone()
        if ok != None:
            cur.execute('select * from ARC')
    res = cur.fetchall()
    for row in res:
        print('                <tr>')
        print('                    <td>' + row[1] + '</td>')
        print('                    <td id="' + row[0] + '"><a href="' + row[3] + '" target="_blank">' + row[2] + '</a></td>')
        print('                    <td>' + row[4] + '</td>')
        print('                </tr>')
    cur.close()
    sql.close()

    print("            </tbody>")
    print("        </table>")

def fixed_part2():
    print("""    </div>
    <div class="ui inverted vertical footer segment">
        <div class="ui center aligned container">
            <h4 class="ui inverted header">Created by Koki Yamaguchi</h4>
            <p>Twitter @Ymgch_K</p>
        </div>
    </div>
</body>
</html>""")

def generate():
    fixed_part1()
    form()
    filter()
    table(0)
    table(1)
    table(2)
    fixed_part2()

if __name__ == '__main__':
    generate()
