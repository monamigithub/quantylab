title: Django에서 Jinja2를 Template Engine으로 사용하기
date: 2017-11-01
category: python
tags: python, django, jinja2
slug: django_jinja2
---

Django는 대표적인 Python 웹 프레임워크 입니다. 페이지 렌더링, ORM, Session 자체 Template Engine도 가지고 있지요.

그런데 개인적인 의견으로 Template Engine은 Jinja2가 더 강력한 것 같습니다. 다행히 Django에서 Jinja2도 지원을 하고 있습니다. 다만 약간의 추가적인 세팅이 필요하죠.

이 포스트에서 Django에서 Jinja2를 사용하는 방법을 차근차근 설명하고자 합니다.

우선 Jinja2를 설치합니다.
```bash
$ pip install Jinja2
```

Django 프로젝트의 `settings.py` 파일을 수정합니다.
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            'app/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'extensions': [
                'jinja2.ext.do',
                'jinja2.ext.loopcontrols',
                'jdj_tags.extensions.DjangoCompat',
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

여기서 Jinja2 부분의 OPTION/extensions에 Jinja2에서 기본 제공하는 확장 기능들을 추가할 수 있습니다. `jinja2.ext.do`와 `jinja2.ext.loopcontrols`는 Jinja2의 기본 확장 기능입니다. [Jinja2 Extensions](http://jinja.pocoo.org/docs/2.9/extensions/)에서 다른 확장 기능들도 확인해 보세요.
`jdj_tags.extensions.DjangoCompat`는 Django Template Engine이 제공하는 Template Tag들을 Jinja2 버전으로 만들어 놓은 커스텀 확장 기능입니다. 이걸 사용하기 위해서 `pip install jinja2-django-tags`로 모듈을 설치합니다.

이렇게 하면 이제 Jinja2를 Template Engine으로 사용하게 됩니다. 그런데 Jinja2에서는 Custom Filter를 기존 Django 방식으로 할 수 없습니다.

필터 함수들을 가지고 있는 모듈 `filters.py`를 다음과 같이 정의합니다.
```python
""" filters.py
"""
from django.utils.http import urlquote


# collection


def filter_getitem(value, arg):
    return value.get(arg, '')


def filter_getat(value, arg):
    try:
        return value[int(arg)]
    except Exception as e:
        return None


def filter_notinappend(a, b):
    if b not in a:
        a.append(b)
    return a


def filter_union(a, b):
    return set(a) | set(b)


# math


def filter_divide(value, arg):
    return float(value) / float(arg)


def filter_mod(value, arg):
    return int(value) % int(arg)


def filter_min(a, b):
    return min(a, b)


def filter_max(a, b):
    return max(a, b)


# converting


def filter_int(value):
    return int(value)


# type


def filter_type(value):
    return str(type(value))


# str


def filter_endswith(value, arg):
    return value.endswith(arg)


def filter_quote(a):
    return urlquote(a)

```

`filters.py`의 필터들을 추가하기 위해 `settings.py`에 다음과 같은 코드를 추가합니다.

```python
jinja2.filters.FILTERS.update({
    "getitem": filters.filter_getitem,
    "getat": filters.filter_getat,
    "notinappend": filters.filter_notinappend,
    "union": filters.filter_union,
    "divide": filters.filter_divide,
    "mod": filters.filter_mod,
    "min": filters.filter_min,
    "max": filters.filter_max,
    "int": filters.filter_int,
    "type": filters.filter_type,
    "endswith": filters.filter_endswith,
    "quote": filters.filter_quote,
})
```

이렇게 하면 html에서 Jinja2 태그들 및 새롭게 추가한 Custom Filter들도 사용할 수 있습니다.

예를 들어서 다음 html 코드는
```
{% raw %}<input type="number" value="{{ -100|max(0) }}">{% endraw %}
```
추가한 max 필터를 거쳐서 `<input type="number" value="0">`이 되는 것입니다.
