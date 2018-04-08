import header, footer, table, form, ACfilter

def filter():
    tags = ['Dijkstra', 'UnionFind', 'フロー', 'セグメント木', '重心分解', 'LCA', 'HL分解']
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

def generate():
    header.generate()
    form.generate()
    filter()
    ACfilter.generate()
    for i in range(5):
        table.generate(i, 1)
    footer.generate()

if __name__ == '__main__':
    generate()
