import header, footer, table, form, ACfilter

def filter():
    tags = ['グラフ', '数論', '幾何', '動的計画法', 'データ構造', '文字列', '数列', '確率・組合せ', 'ゲーム',]
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
    table.generate(0, 0)
    table.generate(1, 0)
    table.generate(2, 0)
    table.generate(3, 0)
    table.generate(4, 0)
    footer.generate()

if __name__ == '__main__':
    generate()
