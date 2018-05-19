title: 대신증권 크레온(Creon) API를 사용하여 파이썬에서 주식 차트 데이터 받아오기
date: 2018-01-16
tags: creon, api, python
slug: creon_chart

최근 개인 투자자들의 프로그램 매매에 대한 관심이 높아지고 있습니다. 이에 따라 여러 증권사들이 API를 선보이고 있습니다. 대표적인 증권사 API로 키움증권 OpenAPI+, 이베스트투자증권 Xing API, 그리고 이번 포스트에서 다룰 대신증권 크레온 Plus API를 들 수 있습니다.

세 가지 API를 모두 사용해 봤지만, 크레온 Plus API를 가장 직관적으로 쉽게 사용할 수 있었습니다. 여기서는 크레온 Plus API로 분봉 차트 데이터를 받아오는 파이썬 소스코드를 다룹니다.
 
```python
import time
import logging
from logging.handlers import TimedRotatingFileHandler

import win32com.client
import pandas as pd


# 로그 파일 핸들러
fh_log = TimedRotatingFileHandler("logs/log", when="midnight", encoding="utf-8", backupCount=120)
fh_log.setLevel(logging.DEBUG)

# 콘솔 핸들러
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)

# 로깅 포멧 설정
formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")
fh_log.setFormatter(formatter)
sh.setFormatter(formatter)

# 로거 생성
logger = logging.getLogger("creon")
logger.setLevel(logging.DEBUG)
logger.addHandler(fh_log)
logger.addHandler(sh)


class Creon:
    def __init__(self):
        self.obj_CpCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        self.obj_CpCybos = win32com.client.Dispatch('CpUtil.CpCybos')
        self.obj_StockChart = win32com.client.Dispatch("CpSysDib.StockChart")

    def creon_7400_주식차트조회(self, code, date_from, date_to):
        """
        http://money2.creontrade.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=284&seq=102&page=1&searchString=StockChart&p=8841&v=8643&m=9505
        :return:
        """
        b_connected = self.obj_CpCybos.IsConnect
        if b_connected == 0:
            logger.debug("연결 실패")
            return None

        list_field_key = [0, 1, 2, 3, 4, 5, 8]
        list_field_name = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
        dict_chart = {name: [] for name in list_field_name}

        while True:
            self.obj_StockChart.SetInputValue(0, 'A'+code)
            self.obj_StockChart.SetInputValue(1, ord('1'))  # 0: 개수, 1: 기간
            self.obj_StockChart.SetInputValue(2, date_to)  # 종료일
            self.obj_StockChart.SetInputValue(3, date_from)  # 시작일
            self.obj_StockChart.SetInputValue(4, 100)  # 요청 개수
            self.obj_StockChart.SetInputValue(5, list_field_key)  # 필드
            self.obj_StockChart.SetInputValue(6, ord('m'))  # 'D', 'W', 'M', 'm', 'T'
            self.obj_StockChart.BlockRequest()

            status = self.obj_StockChart.GetDibStatus()
            msg = self.obj_StockChart.GetDibMsg1()
            logger.debug("통신상태: {} {}".format(status, msg))
            if status != 0:
                return None

            cnt = self.obj_StockChart.GetHeaderValue(3)  # 수신개수
            for i in range(cnt):
                dict_item = {name: self.obj_StockChart.GetDataValue(pos, i) for pos, name in zip(range(len(list_field_name)), list_field_name)}
                for k, v in dict_item.items():
                    dict_chart[k].append(v)

            if not self.obj_StockChart.Continue:
                break
            self._wait()

        logger.debug("차트: {} {}".format(cnt, dict_chart))
        return pd.DataFrame(dict_chart, columns=list_field_name)

    def _wait(self):
        time_remained = self.obj_CpCybos.LimitRequestRemainTime
        cnt_remained = self.obj_CpCybos.GetLimitRemainCount(1)  # 0: 주문 관련, 1: 시세 요청 관련, 2: 실시간 요청 관련
        if cnt_remained <= 0:
            timeStart = time.time()
            while cnt_remained <= 0:
                time.sleep(time_remained / 1000)
                time_remained = self.obj_CpCybos.LimitRequestRemainTime
                cnt_remained = self.obj_CpCybos.GetLimitRemainCount(1)


if __name__ == '__main__':
    creon = Creon()
    print(creon.creon_7400_주식차트조회('035420', 20180101, 20180109))
```

이 파이썬 스크립트를 실행하면 다음과 같이 NAVER 종목의 20180101부터 20180109까지의 분봉 차트 데이터를 받아올 수 있습니다.

![분봉차트데이터](/img/2018-01-16-creon_minchart.png)

크레온 Plus API를 설치하고 파이썬 스크립트를 관리자 권한으로 실행할 것을 권장합니다.
