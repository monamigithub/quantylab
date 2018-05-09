title: 파이썬으로 URL 파싱하기
date: 2017-11-07
category: python
tags: python, url, parsing
slug: url_parsing

파이썬에서 URL을 파싱할 때 주로 파이썬 자체 모듈인 `urllib`을 사용합니다.

LG전자 채용 사이트인 `http://apply.lg.com/main/Intro.rpi`을 파싱 해보겠습니다.

```python
from urllib import parse
parse.urlparse('http://apply.lg.com/main/Intro.rpi')
```
```
ParseResult(scheme='http', netloc='apply.lg.com', path='/main/Intro.rpi', params='', query='', fragment='')
```

출력을 보니까 `netloc` (`hostname`)이 `apply.lg.com` 입니다.

이는 `sub-domain`, `domain`, `top-level domain (TLD)`를 모두 포함하고 있습니다.

여기서 `domain`과 `TLD`만 가져오려면 어떻게 하면 될까요? 간단하지 않습니다. `sub-domain`의 개수도 여러개가 될 수 있고, `TLD`도 여러 요소로 구성될 수 있기 때문입니다.

예를 들어서, `TLD`는 `com`, `co.kr`, `edu`, `ac.kr` 등 다양합니다.

그래서 `TLD` 목록을 가지고 있어야 정확한 파싱이 가능할 것 같습니다.

[tldextract](https://github.com/john-kurkowski/tldextract)을 사용하면 `sub-domain`, `domain`, `TLD`를 구분할 수 있습니다.

먼저 `tldextract`을 설치 합니다.
```
pip install tldextract
```

```python
import tldextract
tldextract.extract('http://apply.lg.com/main/Intro.rpi')
```

```
ExtractResult(subdomain='apply', domain='lg', suffix='com')
```

이제 `doamin` + `TLD`를 쉽게 만들 수 있습니다.

```python
url_comps = tldextract.extract('http://apply.lg.com/main/Intro.rpi')
"{}.{}".format(url_comps.domain, url_comps.suffix)
```

```
'lg.com'
```
