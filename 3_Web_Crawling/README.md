### 1. Overview
> 💡 여러 뉴스 채널 웹 사이트에서 1년치 데이터를 수집하기 위한 Python 기반 크롤링 수행

<br/> 

### 2. Configuration

◼︎ **Architecture**
```text
./
│
├── scripts/
│   ├── hospitalitynet/
│   │   ├── hospitalitynet.sh
│   │   └── hospitalitynet.py
│   │
│   ├── ihrsa/
│   │   ├── ihrsa.sh
│   │   ├── ihrsa.py
│   │   └── ihrsa_industry.py
│   │
│   └── vendingtimes/
│       ├── vendingtimes.sh
│       └── vendingtimes.py
│
├── utils/
│   └── utils.py
│
└── csv_results/ (실행 시 폴더 자동 생성)
```

◼︎ **사이트별 크롤링 기능 분리**
* 크롤링 대상 웹사이트마다 독립적인 디렉터리와 Python 스크립트를 구성
* 사이트의 HTML 구조와 데이터 형식에 맞춰 수집 로직을 관리할 수 있도록 설계

◼︎ **공통 기능 관리**
* `utils/utils.py`에서 여러 크롤러가 공통으로 사용하는 기능을 관리
* 주요 사용 함수
  * Load_soup(url): Requests로 웹페이지를 요청, BeautifulSoup 사용해 HTML 파싱
  * Clean_Text(text): 수집한 텍스트의 불필요한 공백을 제거
  * Get_Date_from_a_Year_ago(): 현재 날짜를 기준으로 1년 전 날짜를 반환, 시간은 자정으로 설정
  * errorLog(error_message, url): 크롤링 중 발생한 오류 메시지, URL, 발생 시각을 `error_log.txt`에 기록

◼︎ **결과 CSV 저장**
* 크롤링한 데이터는 `csv_results/` 디렉터리에 사이트별로 구분하여 저장
* 코드 실행 시 디렉토리 및 CSV 파일 자동 생성

| Vertical | Site | Format | Title | Content | Title-Kor | Content-Kor | Upload_Date | URL | Keyword | Sentiment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 산업 분야 | 사이트 | 콘텐츠 유형 | 원문 제목 | 원문 본문 | 한국어 제목 | 한국어 본문 | 업로드 날짜 | 원문 URL | 키워드 | 감성 분석 |

<br/> 

### 3. Execution

* 사이트 내 특정 카테고리 크롤링 시
```bash
cd scripts/hospitalitynet  # 사이트 디렉토리로 이동
python hospitalitynet.py -u opinion -s csv # u: 크롤링할 카테고리 지정, s: 저장 형식
```
* 사이트 내 전체 카테고리 실행 시
```bash
cd scripts/hospitalitynet  # 사이트 디렉토리로 이동
bash hospitablity.sh
```
* 이후 각 카테고리의 크롤링 결과는 `csv_results/hospitalitynet/`에 개별 CSV 파일로 저장됨
