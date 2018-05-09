title: Python에서 시간 값 변환
date: 2017-09-25
category: python
tags: python
slug: time_converting

개발을 하다보면 시간 값을 자주 다루게 되는데, Python에서 datetime, timestamp (숫자), 문자열 시간 간의 변환하는 간단한 코드를 정리했습니다.

우선 시간 관련 값들을 처리하기 위해 다음 두 모듈을 임포트 합니다.

```python
import datetime
import time
```

## datetime에서 timestamp로 변환

```python
dt = datetime.datetime(2010, 2, 25, 23, 23)
ts = time.mktime(dt.timetuple())
dt, ts
(datetime.datetime(2010, 2, 25, 23, 23), 1267107780.0)
```

## timestamp에서 datetime으로 변환

```python
ts = 1284101485
dt = datetime.datetime.fromtimestamp(ts)
ts, dt
(1284101485, datetime.datetime(2010, 9, 10, 15, 51, 25))
```

## datetime에서 string으로 변환

```python
dt = datetime.datetime(2010, 2, 25, 23, 23)
str_time = dt.strftime('%Y-%m-%d %H:%M:%S')
dt, str_time
(datetime.datetime(2010, 2, 25, 23, 23), '2010-02-25 23:23:00')
```

## string에서 datetime으로 변환

```python
str_time = '2010-02-25 23:23:00'
dt = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
str_time, dt
('2010-02-25 23:23:00', datetime.datetime(2010, 2, 25, 23, 23))
```
