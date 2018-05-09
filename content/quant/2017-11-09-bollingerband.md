title: 파이썬으로 볼린저 밴드 (Bollinger Bands) 구하기
date: 2017-11-09
tags: python, bollinger
slug: bollingerband

볼린저 밴드 (Bollinger Bands)는 어떠한 시리즈 (연속된 값 리스트)의 이동평균값에 표준편차를 빼고 더한 범위를 의미합니다. 이 범위에서 상위 값을 Upper Bollinger Band (HBB), 중간 값을 Middle Bollinger Band (MBB), 하위 값을 Lower Bollinger Band (LBB)라고 합니다.

구하는 공식은 간단합니다.

- `UBB = MA_w(series) + k * sd(series)`
- `MBB = MA_w(series)`
- `LBB = MA_w(series) - k * sd(series)`

여기서 `MA_w()`는 이동평균값을 구하는 함수입니다. 이동평균을 구할 윈도우 크기를 `w`라고 정했습니다. 그리고 `sd()`는 표준편차 값입니다. `k`는 볼린저 밴드에서 고려하는 상수로 볼린저 밴드의 넓이에 영향을 줍니다. `k`는 주로 2로 정합니다.

이제 파이썬 코드를 보겠습니다.

```python
import pandas as pd
import matplotlib.pyplot as plt

def plot_bb(series, w=20, k=2):
    """
    Calculate Bollinger Bands
    ubb = MA_w(series) + k * sd(series)
    mbb = MA_w(sereis)
    lbb = MA_w(series) - k * sd(series)
    :param series:
    :return: (hbb, mbb, lbb)
    """
    mbb = pd.rolling_mean(series, window=w)
    ubb = mbb + k * pd.rolling_std(series, w, min_periods=w)
    lbb = mbb - k * pd.rolling_std(series, w, min_periods=w)
    ubb.plot(x='Date', y='UBB')
    mbb.plot(x='Date', y='MBB')
    lbb.plot(x='Date', y='LBB')
    plt.show()
```

계산한 볼린저 밴드를 `matplotlib`으로 가시화합니다.
