import header, footer

def about():
    print("""        <h3 class='ui top attached header'>Atcodr Finderについて</h3>
        <div class='ui attached segment'>
        <p>Atcoder Finderは過去に<a href='https://atcoder.jp/'>Atcoder</a>で出題された問題に自動的にタグをつけるサービスです。
        特定のジャンルの問題を探したいときなどにご活用ください。</p>

        </div>
        <h3 class='ui top attached header'>主な機能</h3>
        <div class='ui attached segment'>
        <div class="ui list">
            <div class="item">・Atcoderの過去問にタグを自動的につけます。</div>
            <div class="item">・タグを選択すると、そのタグを含む問題だけをフィルタリングできます。</div>
            <div class="item">・Specificなタグ選択をするとより詳細なアルゴリズムによるフィルタリングができます。ただし、ネタバレには十分注意してご使用ください。</div>
            <div class="item">・User IDを入れると、そのユーザの各問題のAC状況がわかります。</div>
        </div>
        </div>
        <h3 class='ui top attached header'>分類について</h3>
        <div class='ui attached segment'>
        <p>各問題は、その問題文とその問題に対する正解コードの情報から自動的に分類されています。
        正解コードも使って分類しているため、ネタバレになる可能性があるので、注意してご使用ください。<br>
        また、現時点ではまだ分類の精度があまりよくない場合があることをご了承ください。</p>
        </div>
        <h3 class='ui top attached header'>作者</h3>
        <div class='ui attached segment'>
        <p>
            Koki Yamaguchi @Ymgch_K
        </p>
        </div>
        <h3 class='ui top attached header'>謝辞</h3>
        <div class='ui attached segment'>
        <p>本開発には@kenkooooさんによる<a href="http://beta.kenkoooo.com/atcoder/">Atcoder Finder</a>のAPIを利用してます。
        また、kimiyukiさん(@a3VtYQo)より技術的なアドバイスを頂いています。ここに感謝の意を記します。
        </p>
        </div>
        <h3 class='ui top attached header'>連絡先</h3>
        <div class='ui attached segment'>
        <p>何か不具合や要望等がありましたら<br>
        ・Twitter: @Ymgch_K<br>
        ・Gmail: yk49at21.gmail.com<br>
        ・<a href="https://github.com/Koki-Yamaguchi/AtcoderFinder/issues">Github Issues</a><br>
        のいずれかよりご連絡いただけると嬉しいです。
        </p>
        </div>""")

def generate():
    header.generate()
    about()
    footer.generate()

if __name__ == '__main__':
    generate()
