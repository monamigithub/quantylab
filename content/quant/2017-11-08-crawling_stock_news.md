title: 파이썬으로 네이버 주식 뉴스 크롤링하기
date: 2017-11-08
tags: python, stock, news, crawling
slug: crawling_stock_news

네이버 주식에서 뉴스를 크롤링하는 간단한 파이썬 코드를 소개합니다.

- Dependency
  - python 3
  - requests
  - BeautifulSoup
  - webob

뉴스 문서를 질의 (Query)나 종목코드로 크롤링 해와서 문서에 포함된 글과 종목코드들을 반환해 줍니다.

```python
import json
import os
from bs4 import BeautifulSoup
import re
import requests
from webob.compat import urlparse

__author__ = 'moonkwonkim@gmail.com'


class NaverFinanceNewsCrawler:
    URL_NAVER_FINANCE = "http://finance.naver.com"
    URL_NAVER_FINANCE_NEWS_QUERY = "http://finance.naver.com/news/news_search.nhn?q=%s&x=0&y=0" # params: query
    URL_NAVER_FINANCE_NEWS_CODE = "http://finance.naver.com/item/news_news.nhn?code=%s&page=%s" # params: (code, page)
    URL_NAVER_NEWS_FLASH = "http://finance.naver.com/news/news_list.nhn?mode=LSS2D&section_id=101&section_id2=258"
    URL_NAVER_STOCK_NOTICE = "http://finance.naver.com/item/news_notice.nhn?code=%s&page=%s" # params: (code, page)

    def __init__(self):
        pass

    def crawl(self, query=None, code=None, page=1):
        """

        :param query:
        :param code:
        :param page:
        :return:
        """
        if query:
            return self._crawl_by_query(query)
        elif code:
            return self._crawl_by_code(code, page=page)
        else:
            raise Exception("[Error] 'query' or 'code' should be entered.")

    def _crawl_by_query(self, query):
        """
        Crawl Naver Finance News
        :param query: string; search keywords
        :return: generator; [{title, summary, url, articleId, content, codes}, ...]
        """

        # Convert the query to euc-kr string
        q = ""
        for c in query.encode('euc-kr'):
            q += "%%%s" % format(c, 'x').capitalize()

        r_url = NaverFinanceNewsCrawler.URL_NAVER_FINANCE_NEWS_QUERY % (q)
        r = requests.get(r_url)

        soup = BeautifulSoup(r.text, "lxml")
        news = soup.find('div', class_='newsSchResult').find('dl', class_='newsList')
        news_title = news.find_all('dt', class_='articleSubject')
        news_summary = news.find_all('dd', class_='articleSummary')
        for title, summary in zip(news_title, news_summary):
            url = NaverFinanceNewsCrawler.URL_NAVER_FINANCE + title.a.get("href")
            res = {
                "title": title.a.text,
                "summary": summary.find(text=True).strip(' \t\n\r'),
                "url": url,
                "articleId": urlparse.parse_qs(urlparse.urlparse(url).query)["article_id"][0]
            }
            res.update(self._crawl_content(url))
            yield res

    def _crawl_by_code(self, code, page=1):
        """
        Crawl Naver Stock News
        :param code: string; a stock code
        :return: generator;
        """

        r_url = NaverFinanceNewsCrawler.URL_NAVER_FINANCE_NEWS_CODE % (code, page)
        r = requests.get(r_url)

        soup = BeautifulSoup(r.text, "lxml")
        news_rows = soup.find('table', class_='type2').find_all('td', class_='title')

        for row in news_rows:
            yield {"title": row.a.text.strip(' \t\n\r'), "url": row.a.get('href')}

    def _crawl_content(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        content = soup.find('div', id="content", class_='articleCont')
        codes = re.findall(r"\d{6}", content.text)
        return {"content": content.text.strip(' \t\n\r'), "codes": codes}
```

삼성전자에 관한 뉴스를 가져와 보겠습니다.

```python
if __name__ == "__main__":
    crawler = NaverFinanceNewsCrawler()
    docs = crawler.crawl(query='삼성전자')
    for i, d in enumerate(docs):
        print("{i}번째 문서".format(i=i+1), end=" " + "-" * 50)
        print("-" * 50)
        print("내용: {content}".format(content=d["content"]))
        print("문서에 포함된 종목 코드: {codes}".format(codes=d["codes"]))
```

이렇게 돌리면 결과는 다음과 같습니다.

```
1번째 문서 ----------------------------------------------------------------------------------------------------
내용: 【서울=뉴시스】 김지은 기자 = 코스피가 8일 사흘 만에 반등에 성공하며 2550선을 회복했다. 코스닥은 연중 최고치를 경신했다. 이날 코스피 지수는 전 거래일(2545.44)보다 6.96포인트(0.27%) 오른 2552.40에 장을 마쳤다.지수는 미국 증시 혼조세와 한미 자유무엽협정(FTA) 재협상에 대한 경계감에 전 거래일보다 10.96포인트(0.43%) 내린 2534.21로 출발했다. 하지만 이내 장중 낙폭을 줄이고 상승 전환해 2540선에서 등락을 거듭하다 개인의 매수세에 2550를 넘었다.이날 개인투자자는 618억원 어치의 주식을 사며 지수 상승을 이끌었다. 기관은 1055억, 외국인은 38억원 순매도했다. 간밤 미국 증시는 세제개편안 통과에 대한 불확실성이 부각되며 혼조세로 마감했다.뉴욕증권거래소(NYSE)에서 다우존스30 산업평균지수는 전날보다 8.81포인트(0.04%) 오른 2만3557.23으로 거래를 마쳤다. 스탠더드앤드푸어스(S&P) 500지수는 전날보다 0.49포인트(0.02%) 하락한 2590.64에 장을 닫았다. 기술주 중심의 나스닥은 18.65포인트(0.27%) 내린 6767.78을 기록했다. 키움증권 서상영 연구원은 "세제개편안 통과에 대한 불확실성의 부각으로 인한 미국 증시의 혼조세와 한미 자유무역협정(FTA) 재협상 요인 등은 한국 증시 하락 요인으로 작용할 가능성이 높다"면서도 "전날 트럼프가 북한과의 대화를 언급하는 등 지정학적 우려 완화에 대한 기대감을 높인 점은 긍정적"이라고 말했다.업종별로는 등락이 엇갈렸다.의약품(1.13%), 전기전자(1.05%), 섬유의복(0.95%), 비금속광물(0.77%), 종이목재(0.71%), 제조업(0.62%), 서비스업(0.60%), 전기가스업(0.53%) 등은 상승했다.반면 철강금속(-1.51%), 보험(-1.17%) 통신업(-0.99%), 은행(-0.76%), 의료정밀(-0.76%), 운수창고(-0.73%), 금융업(-0.69%) 등은 하락했다.시가총액 상위종목을 보면 '대장주' 삼성전자는 2만원(0.71%) 오른 282만5000원에 거래를 마쳤다. 2등주 SK하이닉스도 1200원(1.46%) 오른 8만3600원을 기록했다.이에 반해 현대차(-0.32%), 네이버(-1.63%), 포스코(-2.62%), 삼성물산(-0.34%), 삼성생명(-1.87%), 현대모비스(-0.19%), 삼성바이오로직스(-0.64%) 등은 떨어졌다.코스닥 지수는 전 거래일(701.14)보다 7.97포인트(1.14%) 오른 709.11로 마감, 연중 최고치를 기록했다.전년에 견줘서는 12.3% 상승했다.개인은 808억원 매도 우위를 보였지만 외국인과 기관은 각각 25억원, 900억원 어치 사들였다.정부의 코스닥 활성화 정책에 대한 기대감과 연기금의 코스닥 투자 확대 논의에 힘입어 상승세가 이어진 것으로 풀이된다.시가총액은 248조6000억원으로 전년 대비 23.4%늘었다. kje1321@newsis.com▶ 뉴시스 빅데이터 MSI 주가시세표 바로가기 ▶ 네이버 채널에서 뉴시스를 구독해주세요뉴시스 관련뉴스언론사 페이지로 이동합니다.[빅데이터MSI]8일 주식시장 심리 1→1→1→1단계 '매우 나쁨'시장심리 톱5…신세계·한국토지신탁·영풍·삼성중공업·한미반도체8일 빅데이터 '핫 키워드'…기능·사람·본문·복사·제품코스피, 사흘 만에 반등 2550선 회복…2552.40 마감김동연 "한미 정상회담서 FTA 깊은 논의 없어"
문서에 포함된 종목 코드: []
2번째 문서 ----------------------------------------------------------------------------------------------------
내용: - 대부분 해외 투자 집중…코스피 수익률 못따라잡아- 국내 투자도 비용 이유로 ETF 투자 중심- 종목 투자는 삼성전자 쏠림 현상으로 재미 못봐[이데일리 안혜신 기자] 로보어드바이저펀드에 투자하면 안정적으로 수익을 올릴 수 있다는 말에 적지 않은 자금을 투자했던 투자자들이 부진한 수익률때문에 한숨을 쉬고 있다.◇로보어드바이저 펀드 대부분 해외 투자 집중우후죽순 격으로 늘어나는 로보어드바이저펀드를 운용하는 ‘로봇 펀드매니저’가 고른 투자대상을 들여다보면 그 대답의 단초를 발견할 수 있다. 우선 로보어드바이저펀드의 투자 유형을 살펴봐야 하는데 펀드평가사인 KG제로인에 따르면 현재 운용순자산 10억원 이상의 로보어드바이저펀드 17개 가운데 해외채권이나 주식에 투자하는 상품이 12개로 압도적이다. 로보어드바이저펀드 내에 해외투자상품이 유독 많은 이유는 미국을 중심으로 한 전세계 로보어드바이저 상품 자체가 글로벌하게 자산을 배분하는 상품이 대부분이라는 점이 꼽힌다. 로보어드바이저펀드 후발주자인 우리 입장에서는 해외 사례를 벤치마킹한 측면이 강하다는 얘기다.아울러 국내 주식에 대한 기대 투자수익률이 낮아진 점도 해외투자상품이 많은 이유 중 하나다. 과거 7% 경제성장률을 달성할 때와 현재 2~3% 수준의 경제성장률을 이어가고 있는 상황에서의 주식시장에 대한 기대감은 다를 수 밖에 없다는 것. 업계 관계자는 “국내 자산만으로는 자산 배분에 한계를 느끼고 있다”며 “전세계적으로 놓고 보면 국내뿐만 아니라 다양한 투자 기회가 생길 수 있다”고 설명했다.하지만 해외투자 비중 증가는 아이러니하게도 로보어드바이저펀드 수익률 부진으로 이어졌다. 올해 국내 증시 상승률이 두드러지면서 상대적으로 해외투자 수익률이 이를 따라잡지 못한 것. 실제 올들어 전세계 주가지수는 지난 10월까지 평균 17% 상승했다. 반면 코스피 상승률은 22.9%로 홍콩, 브라질에 이어 상승률에서 3위를 기록하고 있다.◇국내 종목 투자는 삼성전자 쏠림에 재미 못봐그렇다면 국내 투자에 집중하는 로보어드바이저펀드의 선택 종목은 무엇일까. 대부분 펀드의 포트폴리오는 상장지수펀드(ETF)가 차지하고 있다. 분산투자로 상대적으로 안정성이 높은 ETF의 특성상 주식 직접투자보다 체감 수익률이 낮을 수밖에 없는 것이다. 최근 로보어드바이저펀드 중 가장 수익률이 높은 ‘미래에셋AI스마트베타마켓헤지자(주식-재간접)종류F’의 경우 펀드 내 비중이 21.37%로 압도적인 삼성전자(005930)를 제외하고는 일시적으로 낙폭이 큰 우량주 30종목에 투자하는 ‘TIGER 가격조정’(13.96%), 최근 성과가 좋은 종목에 투자하는 ‘TIGER 모멘텀’(13.09%), 변동석이 적은 종목에 투자하는 ‘TIGER 로우볼’(12.55%) 등 7개 ETF를 담고 있다. ‘대신로보어드바이저자산배분성과보수 1[혼합-재간접]Class C’ 역시 ‘KODEX 200’(25.45%), ‘아리랑 배당주’(7.31%), ‘KODEX 코스닥 150’(4.2%) 등 주식에 투자한 10개 종목이 모두 ETF다. ‘하이ROKI1글로벌로보어드바이저증권투자신탁 H[혼합-재간접형]’도 ‘TIGER200’(14.86%)를 비롯해 총 9개의 국내외 ETF로 포트폴리오를 채우고 있다.로보어드바이저펀드가 주로 ETF에 투자하는 이유는 간단하다. 일단 투자비용이 상대적으로 저렴하다. 업계 관계자는 “과거에는 펀드 투자성과가 잘 나오는 편이었지만 최근은 수익 내기가 쉽지 않아졌다”며 “초과 성과도 잘 나오지 않는 상황에서 비용이 더 싼 ETF를 담을 수밖에 없다”고 말했다.ETF보다 주식에 주로 투자하는 펀드도 있다. 다만 최근 코스피 정보기술(IT)주 쏠림이 심화하면서 수익률이 좋지 않다. ‘에셋플러스알파로보코리아그로스증권자투자신탁 1-1(주식)’는 LG디스플레이(034220)·NAVER(035420)·현대건설(000720)·현대산업(012630)·GS리테일(007070)·LG이노텍(011070)·롯데케미칼(011170)·현대중공업(009540)·LG전자(066570)·사람인에이치알(143240) 등 80개 종목에 투자 중이며 ‘에셋플러스알파로보글로벌인컴성과보수증권자투자신탁 1-2(주식)’는 LG디스플레이(034220)·현대건설(000720)·롯데케미칼(011170)·아모레G(002790)·엔씨소프트(036570)·한화(000880)·농심(004370)·GS(078930)·롯데칠성(005300)·한국타이어월드와이드(000240) 등 총 80개 종목에 투자중이다. 에셋플러스자산운용 관계자는 “성장에 중심을 두는 그로스펀드와 안정적인 수익 추구를 하는 인컴펀드의 투자 종목이 다르다”며 “ETF보다 액티브펀드에 종점을 두고 있는 회사인만틈 ETF 투자가 아닌 종목 투자로 로보어드바이저펀드를 연구했다”고 설명했다.‘DB밸류아이로보어드바이저증권자투자신탁(H)[채권혼합-재간접형]’ 역시 개별종목 투자비중이 높은 펀드 중 하나다. 이 펀드는 SK하이닉스(000660)·고려아연(010130)·LG(003550)·두산인프라코어(042670)·대우건설(047040)·롯데하이마트(071840)·롯데정밀화학(004000) 등에 투자하고 있다.이창헌 미래에셋자산운용 패시브솔루션팀장은 “로보어드바이저펀드는 자산배분 전략을 사용하고 있어 단순히 코스피와 수익률을 비교하는 것은 맞지 않다고 본다”며 “단기 투자 실적에 투자자들이 민감하다는 것은 알지만 로보어드바이저펀드는 꾸준히 장기적인 관점에서 수익을 봐야 한다”고 말했다.안혜신 (ahnhye@edaily.co.kr)▶이데일리 개편기념 이벤트 - 갤럭시 노트8 쏩니다▶[카카오톡] 플친 맺으면 스타벅스 쿠폰 팡팡~♥＜ⓒ종합 경제정보 미디어 이데일리 - 무단전재 & 재배포 금지＞이데일리 관련뉴스언론사 페이지로 이동합니다.미소 띤 트럼프, 한미 FTA '돌출 발언' 사라진 이유[단독]종교인 과세 50년만에 내년 시행 '가닥'…기독교계는 반발조두순 '재심'은 불가능..출소 전 타이트한 '보안 처분' 이뤄져야멜라니아, '델포조' 코트 벗고 '제이멘델' 시스루 드레스 입어'비행기 사고로 사망' 할러데이에 메이저리그 애도 물결
문서에 포함된 종목 코드: ['005930', '034220', '035420', '000720', '012630', '007070', '011070', '011170', '009540', '066570', '143240', '034220', '000720', '011170', '002790', '036570', '000880', '004370', '078930', '005300', '000240', '000660', '010130', '003550', '042670', '047040', '071840', '004000']
3번째 문서 ----------------------------------------------------------------------------------------------------
내용: - 코스피지수 2550선 회복…삼성전자·SK하이닉스등 IT관련주 상승전환- 트럼프, 北이슈 완화발언·FTA 언급자제…“긍정적으로 평가”- “IT업종 하반기 랠리 주도…반도체 업종 상승추세 여전”[이데일리 윤필호 기자] 도널드 트럼프 미국 대통령의 방한에 잔뜩 긴장했던 국내 주식시장이 안도랠리를 보였다. 우려와 달리 돌발변수가 발생하지 않자 투자심리가 안정을 되찾은 것. 특히 올해 상승장을 이끌고 있는 정보기술(IT) 관련주(株)와 제약·바이오주 등 기존 주도주들이 최근 조정세를 접고 다시 힘을 내고 있는 양상이다.◇IT·바이오주 주도로 증시 반등…트럼프 리스크 해소8일 마켓포인트에 따르면 코스피지수는 전거래일대비 6.96포인트(0.27%) 오른 2552.40에 장을 마감했다. 코스피지수는 이번 주 들어 트럼프 방한을 앞두고 부진한 모습을 보였다. 지난 6일부터 8.56포인트, 7일 3.97포인트 각각 빠지며 조정국면에 들어가는 것이 아니냐는 전망도 나왔지만 별다른 충격없이 트럼프 방한 일정이 마무리되자 시장은 기존 상승추세를 회복하는 모습이다. 특히 기존 주도주였던 IT관련주가 재차 상승세를 타면서 전기전자업종지수도 5거래일 만에 반등했다. 대장주인 삼성전자(005930)는 5거래일 만에 상승세를 보였고 SK하이닉스(000660)도 3거래일만에 상승 전환했다. 코스닥지수의 경우 제약·바이오의 약진이 돋보였다. 지난 3일 700선을 넘긴 이후 방한 이슈와는 별도로 꾸준한 상승세를 이어가고 있다.트럼프 대통령 방한으로 비롯된 불확실성이 해소된 데 따른 것으로 보인다. 트럼프 대통령은 이날 국회 연설에서 북한 핵미사일 이슈와 관련해 “북한은 미국을 유약하다고 해석했는데 이것은 치명적인 오산이 될 것“이라고 경고하며 강한 어조로 비판했다. 하지만 전날인 7일 문재인 대통령과의 공동 기자회견에서는 “북한은 협상 테이블에 나와 우리와 합의를 도출하는 것이 좋을 것”이라고 밝혀 그간 초강경 기조보다 완화됐다는 평가를 받았다.한국과 미국간 자유무역협정(FTA) 개정 문제에 대해서도 압박의 강도가 높지 않았다는 평가다. 트럼프 대통령은 국회 연설에서 이에 대해 한 차례 언급을 하는데 그쳤다. 전날 공동기자회견에서도 “현재 협정은 성공적이지 못했고 미국에는 그렇게 좋은 협상은 아니었다고 말씀드리고 싶다”고 말해 원론적인 입장을 강조하는데 그쳤다.◇“트럼프 방한 긍정적…IT관련주, 다시 상승장 이끌 것”증권가에서는 트럼프 대통령의 방한에 대체로 긍정적 평가를 내놓았다. 아울러 증시에서 IT주 등 기존 주도주들이 다시 상승랠리를 이끌 것이라고 전망했다. 박중제 메리츠종금증권 투자전략팀장은 “트럼프 대통령 방문에서 북한 문제에 완화된 모습은 긍정적”이라면서도 “FTA 재협상 문제의 경우 아직 어떤 방향으로 합의가 되고 얼마나 시간이 걸릴지 등에 대한 정보가 부족하기 때문에 당장 반영되는 이슈가 아니다”고 말했다. 그는 “IT업종은 올해 주도주였고 실적도 좋았다”며 “최근 상승세가 주춤한 것은 다른 업종과의 수익률 격차가 크게 벌어진데 따른 단기적 숨고르기 정도로 보인다”며 “하지만 전망도 여전히 좋고 이익도 증가하고 있어서 연말까지는 순환매가 나올 수 있다고 보고 있다”고 진단했다.이상재 유진투자증권 투자전략팀장은 최근 코스피지수 부진에 대해 “상승국면에서 잠시 쉬어가는 흐름으로 시장 방향성과 관련해 논란이 제기될 상황은 아니다”고 판단했다. 그러면서 트럼프 대통령의 북한 관련 발언에 대해서는 “북한 리스크와 관련해 종전의 강한 기조에서 물러나 대화를 시사하는 등 비교적 우호적 모습을 보였다”고 평가했다. 이 팀장은 IT관련주 부진에 대해 “IT주는 잠시 쉬어가는 정도지 조정이라고 말할 순 없다”면서 “단기 급등에 따른 조정은 있을 수 있지만 반도체 업황에 대한 긍정적 기대가 여전한 만큼 상승추세는 유효하다”고 점쳤다.윤필호 (nothing@edaily.co.kr)▶이데일리 개편기념 이벤트 - 갤럭시 노트8 쏩니다▶[카카오톡] 플친 맺으면 스타벅스 쿠폰 팡팡~♥＜ⓒ종합 경제정보 미디어 이데일리 - 무단전재 & 재배포 금지＞이데일리 관련뉴스언론사 페이지로 이동합니다.미소 띤 트럼프, 한미 FTA '돌출 발언' 사라진 이유[단독]종교인 과세 50년만에 내년 시행 '가닥'…기독교계는 반발조두순 '재심'은 불가능..출소 전 타이트한 '보안 처분' 이뤄져야멜라니아, '델포조' 코트 벗고 '제이멘델' 시스루 드레스 입어'비행기 사고로 사망' 할러데이에 메이저리그 애도 물결
문서에 포함된 종목 코드: ['005930', '000660']
4번째 문서 ----------------------------------------------------------------------------------------------------
내용: [서울경제] 코스피 지수가 사흘 만에 상승세로 전환했다. 8일 코스피 지수는 전 거래일 대비 6.96포인트(0.27%) 오른 2,552.40에 장을 마쳤다. 이 날 지수는 전일 대비 0.43% 하락한 2,534.48에 장을 시작했으나 외국인과 개인의 매수세에 힘입어 장중 반등에 성공했다. 장중 국내 주식을 사들이던 외국인은 오후 장에서 매도세로 전환했다. 외국인과 기관은 각각 38억원 1,059억원 어치 주식을 팔아치웠으며 개인만 홀로 매수 우위를 나타냈다. 도널드 트럼프 미국 대통령 방문으로 일부 불확실성이 해소되면서 일부 업종이 상승 전환한 게 주효했다. 업종별로는 의약품이 1.13% 상승했으며 전기전자(1.05%), 음식료품(0.59%), 섬유의복(0.95%), 종이목재(0.71%), 화학(0.40%), 비금속광물(0.77%) 등이 올랐다. 철강금속은 한미FTA 재협상 우려로 1.51% 하락했고 기계(-0.51%), 의료정밀(-0.76%), 운송장비(-0.18%), 통신업(-0.99%), 보험(-1.17%) 등이 약세를 나타냈다. 시가총액 상위 종목 중에는 삼성전자(005930)와 SK하이닉스(000660)가 각각 1.18%, 0.97% 상승하며 지수 상승을 이끌었다. 다른 상위 종목은 대개 약세로 마감했으며 한미FTA 재협상 가능성이 야기되면서 포스코가 2.31% 하락 마감했다. 코스닥은 전일 대비 7.97포인트(1.14%) 오른 709.11에 마감했다./서지혜기자 wise@sedaily.com[서울경제 바로가기]1997년 이래 대한민국 최고의 과학자 DB [바로가기]서울경제의 모든 연재물!... 서경Cube [바로가기▶]저작권자 ⓒ 서울경제, 무단 전재 및 재배포 금지서울경제 관련뉴스언론사 페이지로 이동합니다.[단독] 트럼프 맞아 청와대가 공수해 건 그림은?北에 등돌리는 중국? 갑자기 평양관광 금지한 이유멜라니아 트럼프가 샤이니 민호에게 활짝 웃어준 까닭? "훈훈한 분위기"조두순 사건 영화 '소원' 재조명...이준익 감독이 영화를 만든 이유는?장훈 감독 입장은? "조덕제 나를 만신창이 만들어" 메이킹 영상 "처절하게 강간당하는 모습
문서에 포함된 종목 코드: ['005930', '000660']
```