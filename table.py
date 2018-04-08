import sqlite3, io, sys
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def generate(type, f_type):
    if type == 0:
        print("        <h3 class='ui block header'>Atcoder Grand Contest</h3>")
    elif type == 1:
        print("        <h3 class='ui block header'>Atcoder Beginner Contest</h3>")
    elif type == 2:
        print("        <h3 class='ui block header'>Atcoder Regular Contest</h3>")
    elif type == 3:
        print("        <h3 class='ui block header'>Atcoder Petrozavodsk Contest</h3>")
    elif type == 4:
        print("        <h3 class='ui block header'>Other Contest</h3>")
    print("""        <table class="ui striped table">
            <thead>
                <tr>
                    <th>問題番号</th>
                    <th>問題名</th>
                    <th>タグ</th>
                </tr>
            </thead>""")
    print("            <tbody>")
    #sql = sqlite3.connect('/usr/share/nginx/html/database/problems.db')
    sql = sqlite3.connect('./database/problems3.db')
    cur = sql.cursor()
    pat = ['AGC', 'ABC', 'ARC', 'APC', 'Others']
    cur.execute("SELECT * FROM sqlite_master where type='table' and name='" + pat[type] + "'")
    ok = cur.fetchone()
    if ok != None:
        cur.execute("select * from " + pat[type])
    res = cur.fetchall()
    for row in res:
        print('                <tr>')
        print('                    <td>' + row[1] + '</td>')
        print('                    <td id="' + row[0] + '"><a href="' + row[3] + '" target="_blank">' + row[2] + '</a></td>')
        print('                    <td>' + row[4 + f_type] + '</td>')
        print('                </tr>')
    cur.close()
    sql.close()
    print("            </tbody>")
    print("        </table>")
