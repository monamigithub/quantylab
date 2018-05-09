title: Google과 Naver에서 동시 검색하는 Chrome Extension 만들기
date: 2017-10-13
category: web
tages: chrome, extension
slug: gn_chrome_ext

Google과 Naver를 동시에 검색해 보고 싶어 졌습니다. 처음에는 `iframe`으로 그냥 띄우면 되지 않을까 했는데 문제가 생겼습니다.
Google과 Naver와 같이 `X-Frame-Options`가 `DENY` 또는 `SAMEORIGIN`으로 설정되어 있는 사이트는 iframe으로 띄울 수가 없습니다.

그래서 생각한 것이 Chrome Extension으로 만들어 보는 것이였습니다. Chrome Extension 개발의 기본적인 사항은 [Getting Started: Building a Chrome Extension](https://developer.chrome.com/extensions/getstarted)에서 확인하시면 됩니다.

코드는 간단합니다. 우선 HTML 코드 입니다.

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Google과 Naver 동시 검색 확장앱</title>
    <link rel="stylesheet" type="text/css" href="lib/bootstrap-4.0.0-beta/css/bootstrap.css">
    <link rel="stylesheet" type="text/css" href="lib/font-awesome-4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="browser.css">

    <script type="text/javascript" src="lib/jquery-3.2.1.min.js"></script>
    <script type="text/javascript" src="lib/popper.min.js"></script>
    <script type="text/javascript" src="lib/bootstrap-4.0.0-beta/js/bootstrap.min.js"></script>
    <script src="browser.js"></script>
</head>
<body>
<div id="layout_srch">
    <div class="row">
        <div class="col">
            <a id="a_back_g" href="#"><i class="fa fa-arrow-left my-control" aria-hidden="true"></i></a>
        </div>
        <div class="col-10">
            <form id="form_srch" class="form-inline">
                <div id="dv_srch" class="form-group">
                    <input id="inp_query" class="form-control mr-2" value="">
                    <button id="btn_srch" class="btn btn-success">
                        <i class="fa fa-search" aria-hidden="true"></i>
                    </button>
                </div>
                <div class="form-check mb-2 mr-sm-2 mb-sm-0">
                    <label class="form-check-label">
                        <input id="ckb_mode" type="checkbox" class="form-check-input">
                        모바일 모드
                    </label>
                </div>
            </form>
        </div>
        <div class="col">
            <a id="a_back_n" href="#"><i class="fa fa-arrow-left my-control" aria-hidden="true" style="float: right"></i></a>
        </div>
    </div>
</div>
<webview id="ifr_g" src="https://www.google.co.kr/search?q="></webview>
<webview id="ifr_n" src="https://search.naver.com"></webview>
</body>
</html>

```

상단에 검색 폼을 두고 왼쪽에는 구글 웹뷰, 오른쪽에는 네이버 웹뷰를 두었습니다.

상단의 검색 폼에서 질의를 입력하고 검색 버튼을 누르면 이 두 웹뷰를 각 URL에 질의를 추가하여 다시 로딩합니다. 이를 위한 JavaScript 코드는 다음과 같습니다.

```javascript
$(function() {
    var webview_g = $('#ifr_g');
    var webview_n = $('#ifr_n');

    var version = navigator.appVersion.substr(navigator.appVersion.lastIndexOf('Chrome/') + 7);
    var match = /([0-9]*)\.([0-9]*)\.([0-9]*)\.([0-9]*)/.exec(version);
    var majorVersion = parseInt(match[1]);
    var buildVersion = parseInt(match[3]);

    var AGENT_PC = webview_g.get(0).getUserAgent();
    var AGENT_MOBILE = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36";

    function search() {
        var query = $('#inp_query').val();

        webview_g.attr('src', "https://www.google.co.kr/search?q="+query);
        webview_n.attr('src', "https://search.naver.com/search.naver?query="+query);
    }

    $('#btn_srch').click(search);

    $('#inp_query').keypress(function(event) {
        if (event.which == 13) {
            document.querySelector('#btn_srch').click();
            event.preventDefault();
        }
    });

    $('#ckb_mode').change(function () {
        var checked = $(this).prop('checked');
        if (checked) {
            webview_g.get(0).setUserAgentOverride(AGENT_MOBILE);
            webview_n.get(0).setUserAgentOverride(AGENT_MOBILE);
        } else {
            webview_g.get(0).setUserAgentOverride(AGENT_PC);
            webview_n.get(0).setUserAgentOverride(AGENT_PC);
        }
        search();
    });

    function adjust_height() {
        var height = window.innerHeight - 60;
        webview_g.css('height', height);
        webview_n.css('height', height);
    }
    adjust_height();
    window.onresize = adjust_height;
});
```

여기서 주의할 점은 웹뷰의 에이전트를 잘 정해줘야 한다는 것입니다. 에이전트가 잘 정의되어 있지 않으면 (구글, 네이버가 막아놔서) 검색이 되지 않을 수도 있습니다.

추가로 CSS도 공유합니다.

```css
body {
    margin: 0;
    padding: 0;
    min-width: 800px;
}

#layout_srch {
    position: fixed;
    top:0px;
    right:0px;
    left:0px;
    height: 60px;
    border-bottom: 1px solid #eee;
}

#layout_srch .my-control {
    color: #fff;
    margin: 10px;
    padding: 10px;
}

#form_srch {
    margin: 0px auto;
    width: 600px;
    padding: 10px;
}

#inp_query {
    width: 400px;
}

#lb_mode {
    color: #fff;
}

#dv_srch {
    width: 80%;
    margin-right: 10px;
}

#ifr_g {
    position: fixed;
    right: 50%;
    top: 60px;
    bottom: 0px;
    width: 50%;
}

#ifr_n {
    position: fixed;
    right: 0px;
    left: 50%;
    top: 60px;
    bottom: 0px;
    width: 50%;
}
```

결과는 다음과 같습니다.

![결과](/img/2017-10-13-gnchromeext.png)
