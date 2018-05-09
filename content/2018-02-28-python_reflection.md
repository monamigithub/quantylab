title: 파이썬 리플렉션 (동적 클래스 인스턴스 생성 및 함수 호출)
date: 2018-02-28
category: python
tags: python, reflection
slug: python_reflection

리플렉션(Reflection)이란 런타임에서 프로그램의 구조를 파악하고 동적 객체 생성 및 함수 호출 등의 행위를 수행할 수 있게 해주는 장치 입니다.

이 포스트에서는 파이썬에서의 간단한 리플렉션 예제를 소개합니다.

```python
class MyClass:
    my_var = 1

    def __init__(self):
        pass

    def my_fnc(self, arg):
        print('my_fnc({}) called.'.format(arg))


# 클래스 및 클래스변수 접근
my_class = globals()['MyClass']
print(my_class)
print(my_class.my_var)


# 객체 생성
my_inst = my_class()
print(my_inst)


# 함수 접근 및 호출
func = getattr(my_inst, 'my_fnc')
print(func)
func(2)
```
