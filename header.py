def generate():
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
        <a class="item" href="./index.html">
            <h3>Atcoder Finder</h3>
        </a>
        <a class="item" href="./specific.html">
            <h3>Specific</h3>
        </a>
        <a class="item" href="./about.html">
            <h3>About</h3>
        </a>
        <a class="item" href="https://github.com/Koki-Yamaguchi/AtcoderFinder">
            <h3>Source</h3>
        </a>
    </div>
    <div class="ui container">""")
