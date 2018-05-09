title: Django 서버 시작할 때 실행할 코드 설정하기
date: 2017-11-28
category: python
tags: python, django
slug: django_onstartup

Django는 파이썬 계열에서 대표적인 웹 프레임워크 입니다. 많지는 않지만 서버를 실행함과 동시에 특정 코드를 실행할 일이 생깁니다. 예를 들어서, 서버를 시작하면서 파일을 읽거나, 객체를 생성해 놓거나, 다른 서버에 메시지를 전송하는 등이 될 수 있습니다.

이 때, `AppConfig`를 사용하면 됩니다. 먼저 `AppConfig`를 상속하는 클래스를 정의합니다.

```python
# app/broker.py
from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'my_app'
    verbose_name = "My App"

    def ready(self):
        # TODO: Write your codes to run on startup
        pass
```

이렇게 정의한 클래스를 `__init__.py`에 명시해 주면 끝입니다.

```python
# app/__init__.py
default_app_config = 'app.broker.MyAppConfig'
```

그런데 한가지 주의할 점이 있습니다. 이 부분을 간과하면 곤란한 상황이 생길 수 있습니다.
Django가 기본적으로 코드 검증 과정에서 한번, 코드 실행 과정에서 한번, 총 2번 `MyAppConfig`를 실행합니다.

두번 실행되는 일을 피하기 위해서 Django 서버를 실행할 때 다음과 같이 `--noreload` 옵션을 넣어줍니다.

```bash
python manage.py runserver 0.0.0.0:8000 --noreload
```
