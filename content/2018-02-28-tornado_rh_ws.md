title: Python Tornado로 HTTP 및 웹소켓(Web Socket) 요청 처리하기
date: 2018-02-28
category: python
tags: python, tornado, websocket
slug: tornado_rh_ws

Tornado는 비동기(Asynchronous) 통신을 지원하는 Python 웹프레임워크 입니다. 아는 바로는 (확실하진 않지만) Facebook에서 만들었고 페북의 채팅 기능에서 활용하고 있다고 합니다.
Tornado는 특히 웹소켓(Web Socket) 개발에 유용하게 사용할 수 있습니다. 다른 Python 웹프레임워크인 Django, Flask 등에서 보다 간단하게 웹소켓을 사용할 수 있는 장점이 있습니다.

기본적인 요청 처리는 다음과 같이 RequestHandler를 상속하여 구현하면 됩니다.
```python
import tornado

__author__ = 'mkk'

class MyRequestHandler(tornado.web.RequestHandler):
    def get(self):
        # GET Params
        self.get_argument("name")
        # Response
        self.write("OK")

application = tornado.web.Application([
    (r"/", MyRequestHandler),
])
application.listen(8888)
tornado.ioloop.IOLoop.current().start()
```

웹소켓 요청을 처리하기 위해서는 다음과 같이 작성하면 됩니다.
```python
import tornado

__author__ = 'mkk'

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")

application = tornado.web.Application([
    (r"/ws", EchoWebSocket),
])
application.listen(8888)
tornado.ioloop.IOLoop.current().start()
```
