title: Pandas DataFrame을 엑셀 파일로 내보내기
date: 2017-09-25
category: python
tags: python, pandas
slug: df_export

한글을 포함하는 Pandas DataFrame을 csv 파일로 변환할 상황이 생겼습니다.

```python
import pandas as pd
df = pd.DataFrame()
# ...
df.to_csv('out.csv', encoding='utf-8')
```

이렇게 인코딩까지 지정하면 한글이 깨지지 않을 것이라 기대했는데... 깨집니다.
안깨지게 하려면 csv가 아니라 excel 파일로 변환하면 됩니다.

```python
df.to_excel('out.xlsx', sheet_name='sheet1')
```

긴 URL이 있으면 워닝 (UserWarning: Ignoring URL)이 뜨는데, 아래와 같이 해결할 수 있습니다.

```python
writer = pd.ExcelWriter('out.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
df.to_excel(writer)
```
