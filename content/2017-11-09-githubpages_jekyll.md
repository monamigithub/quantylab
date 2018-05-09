title: Github Pages와 Jekyll로 무료로 블로그 만들기
date: 2017-11-09
category: web
tags: jekyll, github pages
slug: githubpages_jekyll

저는 Markdown으로 글을 작성하는 것을 선호합니다. 여러 이유가 있지만 크게 다음 3가지 이유 때문입니다.
- 헤더, 리스트, 테이블, 링크, 이미지 등을 키보드만으로 쉽게 작성할 수 있습니다. 대다수의 WYSWYG 에디터에서는 마우스를 많이 쓰게 되서 불편했습니다.
- 스타일을 신경쓰지 않아도 됩니다. Markdown을 HTML로 변환해 주는 엔진에서 알아서 스타일을 맞춰줍니다.
- 소스코드를 언어에 맞게 하이라이팅하기가 쉽습니다. 프로그래밍 관련 글을 많이 쓰는 저로서는 중요한 사항 입니다.

Markdown으로 작성한 글을 웹 상에 올리는데 [Jekyll](https://jekyllrb.com/)을 최근 많이 사용하는 것 같습니다. Jekyll은 정적 (Static) 웹사이트를 만들어 주는 도구이고 Markdown을 HTML로 변환해 줍니다.

이제 Jekyll로 만든 블로그를 어디에 올려서 운영하느냐의 문제가 남았습니다. 호스팅 업체에서 유료로 할 수도 있지만 돈을 쓰고 싶지가 않습니다. 가입, 신청, 관리 등의 번거로움도 달갑지 않습니다. 

그래서 [Github Pages](https://pages.github.com/)로 블로그를 만들기로 한 것입니다. Github Pages는 무료로 웹페이지를 호스팅해 줍니다. `{사용자이름}.github.io`와 같이 도메인까지 무료로 제공해 줍니다. 게다가 Github Pages는 Jekyll을 내장하고 있어서 파일만 올리면 알아서 사이트를 빌드해 줍니다.

먼저 [Github](https://github.com/)에서 리파지토리를 하나 만듭니다. 리파지토리 이름을 `{사용자이름}.github.io`로 정해 주세요.

이제 블로그 파일을 준비합니다. Jekyll을 설치하여 빈 (Empty) 블로그를 만들고 하나하나 만들어갈 수도 있지만 Jekyll도 설치하기가 싫어서 저는 템플릿을 다운받아서 수정하여 사용했습니다. Jekyll의 기본 템플릿은 [minima](https://github.com/jekyll/minima) 입니다.

주로 수정해야 하는 파일들은 `_config.yml`과 `_posts` 내의 파일들 입니다. `_config.yml`파일에서는 `title`, `author`, `email`, `description`, `url` 등을 수정해 주어야 합니다.

이렇게 준비한 파일을 전에 만든 리파지토리에 올려줍니다. 준비한 블로그 폴더로 이동하고 다음과 같이 파일들을 올려줍니다.

```
$ git init
$ git remote add origin https://github.com/{사용자이름}/{사용자이름}.github.io
$ git add *
$ git commit -m "first commit"
$ git push -u origin master
```

이제 Github Pages가 사이트를 빌드하기를 조금 기다리고 브라우저에서 `https://{사용자이름}.github.io`로 접속하면 블로그가 나타납니다.
