def generate():
    print("""        <h4 class='ui top attached header'>ACフィルター</h4>
        <div class='ui attached segment'>
            <div class='filter-container'>
                <div class='filters ui form'>
                    <div class='inline fields'>
                        <div class='field'>
                            <div class='ui checkbox'>
                                <input type='checkbox' name='タグ' placeholder='notAC' value='notAC'><label>ACしていない問題だけを表示する</label>
                            </div>
                        </div>
                        <div class='field'>
                            <div class='ui checkbox'>
                                <input type='checkbox' name='タグ' placeholder='isWA' value='isWA'><label>提出したがACしていない問題だけを表示する</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>""")

