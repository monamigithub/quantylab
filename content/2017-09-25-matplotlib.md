title: Matplotlib 라인차트
date: 2017-09-25
category: python
slug: matplotlib

Python에서 초간단 라인차트를 그려보자.
누군가가 일주일 동안 BMI를 측정해보았다고 치고, 아래 코드는 x축을 날짜, y축을 BMI 값으로 가지는 차트를 그린다.

```python
import matplotlib.pyplot as plt

bmi = [24.6, 24.6, 24.9, 24.9, 24.9 ,24.9, 24.6]

plt.title("BMI Chart")
plt.ylabel("BMI")

plt.xticks(range(1, 8), ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"], fontsize=10)
plt.plot(range(1, 8), bmi, "o-", color="b", linewidth=1)
plt.ylim([23, 26])

plt.show()
```

title을 정하고, y축 레이블을 정하고, x축에 표시할 값들을 정해주고, 데이터를 뿌린다. 이 때, 값들을 점으로 표시하고 선으로 연결하도록 "o-" 옵션을 주고, 색깔을 blue로 하고, 선 굵기를 1로 했다.
y축의 범위를 [23, 26]으로 정해서 선차트 위아래 어느정도 공간을 주고. show!

![차트](/img/2017-09-25-matplotlib_chart.png)
