title: 자바스크립트 (JavaScript)에서 객체지향 프로그래밍 (OOP) 하기
date: 2017-11-19
category: web
tags: javascript, oop
slug: javascript_oop

자바스크립트에서는 명시적으로 지원되는 객체지향 프로그래밍 방법이 부족합니다. 객체지향 프로그래밍의 철학을 철저하게 따르는 자바 (Java)와는 이름은 비슷하지만 차이가 많습니다.

이번 포스트에서는 자바스크립트에서 OOP를 흉내낼 수 있는 팁을 소개합니다.

OOP 꽃은 클래스 입니다. 클래스는 상태 (State)과 행동 (Behavior)을 캡슐화 (Encapsulation)하는 단위입니다. 상태는 속성 (Attribute)로, 행동은 메소드 (Method)로 구현됩니다. 물론 자바스크립트에서는 메소드를 함수 (Function)라고 명명하는 것이 더 자연스러울 것입니다.

그럼 자바스크립트에서 클래스를 만들어 보겠습니다.

```javascript
function MyClass() {

}
```

사실 자바스크립트는 `class` 키워드를 완전히 지원하고 있지 않습니다. 클래스 역할을 `function` 키워드가 대신합니다. `function` 키워드로 클래스도, 함수도 선언하는 것입니다.

여기서 `MyClass`의 객체를 생성하려면 `var myClassInstance = new MyClass();`와 같이 하면 됩니다.

그럼 `MyClass`에 상태와 행동을 넣어 보겠습니다.

```javascript
function MyClass() {
    var myPrivateAttr1 = 1;
    var myPrivateAttr2 = 2;
    function myPrivateFnc1 () {
        return myPrivateAttr1;
    }
    function myPrivateFnc2 () {
        return myPrivateAttr2;
    }
}
```

변수 2개와 함수 2개를 넣었는데, 모두 `MyClass` 외부에서는 사용할 수 없습니다. 즉 이들은 Private 속성과 함수 입니다. 그럼 Public 속성과 함수를 추가하는 방법을 보겠습니다.

```javascript
function MyClass() {
    var myPrivateAttr1 = 1;
    var myPrivateAttr2 = 2;
    function myPrivateFnc1 () {
        return myPrivateAttr1;
    }
    function myPrivateFnc2 () {
        return myPrivateAttr2;
    }

    var self = {
        myPublicAttr1: 1,
        myPublicAttr2: 2,
        myPublicFnc1: function () {
            return myPrivateFnc1();
        },
        myPublicFnc2: function () {
            return myPrivateFnc2();
        }
    };
    return self;
}
```

이렇게 하면 외부에서 `self` 변수 안에 들어 있는 속성과 함수들을 접근할 수 있게 됩니다. 즉 이들은 Public 속성과 함수들 입니다.

```javascript
var myClassInstance = new MyClass();
console.log(myClassInstance.myPublicFnc1());
```

이렇게 하면 브라우저 콘솔에 1이 출력될 것입니다.
