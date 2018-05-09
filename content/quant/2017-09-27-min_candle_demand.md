title: 분봉 수급 점수 계산하기
date: 2017-09-27
tags: 주식, 분봉, 수급
slug: min_candle_demand

여기서 구하고자 하는 피쳐는 **분봉 수급 점수**입니다.

> 분봉 수급 점수: 1분동안 체결이 많이 이루어진 분봉들 중에서 매수세가 강한 분봉들의 비율로 [-1, 1]의 범위를 가짐

아래와 같은 1분봉차트가 있습니다. 분봉들이 아주 많아서 사람이 직접 점수를 계산하기는 어려울 수 있습니다.

![분봉동시호가제외](/img/2017-09-27-mincandledemand/분봉동시호가제외.png)

[분봉차트 CSV 파일](/data/2017-09-27-mincandledemand_000660_1m.csv)

이를 파이썬으로 계산해 보겠습니다.
> python3, numpy, pandas, matplotlib, mpl_finance 등을 필요로 합니다.

`mpl_finance`는 https://github.com/matplotlib/mpl_finance 에서 받을 수 있습니다.

우선 필요한 라이브러리들 부터 임포트합니다.

```python
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
import mpl_finance
 
if __name__ == '__main__':
    pass
```

이제 아래 코드로 `main`을 채웁니다.

```python
df_chart = pd.read_csv('data/000660_m_in.csv')  # 다운받은 데이터의 경로로 변경하십시오

# 고려할 분봉 수 결정
# df_chart = df_chart.iloc[-60*6*5:]  # 약 5일치 분봉

# 동시호가 거래 없애기
df_chart['체결일'] = (df_chart['체결시간'] / 1000000).astype(int)
df_chart['체결시분'] = df_chart['체결시간'].mod(1000000).astype(int)
df_chart = df_chart[df_chart['체결시분'] < 153000]

# 거래량이 평균+표준편자*2 보다 많았던 분봉들만 남깁니다
df_chart = df_chart[df_chart['거래량'] > df_chart['거래량'].mean() + df_chart['거래량'].std() * 2]

# [수요 거래대금 + 공급 거래대금]을 구합니다
supdemand = ((df_chart['현재가'] - df_chart['시가']).abs() * df_chart['거래량']).sum()

# [수요 거래대금 - 공급 거래대금]을 구합니다
demand = ((df_chart['현재가'] - df_chart['시가']) * df_chart['거래량']).sum()

# [(수요 거래대금 - 공급 거래대금) / (수요 거래대금 + 공급 거래대금)]을 구합니다
score_demand = float(demand) / supdemand
```

여기서 `score_demand`가 **분봉 수급 점수**입니다. 이 점수가 1에 가까울수록 수요 거래대금이 컸다는 의미이고 -1에 가까울수록 공급 거래대금이 많았다는 의미입니다.

위의 1분봉 차트에 대해서 분봉 수급 점수는 0.1252 입니다. 양수이므로 수요 거래대금이 더 많았다는 뜻입니다.

물론 이 지표만으로 투자를 결정할 수는 없습니다. 앞으로 다양한 지표들을 개발하고 데이터를 기반으로 이유있는 투자를 하고자 합니다.
