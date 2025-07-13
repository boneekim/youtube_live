# YouTube Video Extractor

## 프로젝트 설명
boneekim의 YouTube 영상 추출 도구입니다. 키워드와 국가를 선택하여 YouTube 영상을 검색하고 섬네일 목록으로 결과를 확인할 수 있습니다.

## 주요 기능

### 🔍 **영상 검색**
- 키워드 기반 검색
- 국가별 필터링 (한국, 미국, 일본 등 20개국)
- 검색 결과 개수 조절 (5~50개)
- 다양한 정렬 옵션 (관련성, 최신순, 조회수, 평점)

### 🖼️ **결과 표시**
- 3열 그리드 레이아웃
- 섬네일 이미지 표시
- 영상 제목 (클릭 시 YouTube 이동)
- 채널명 및 업로드 일시
- 영상 설명 보기
- 실시간 통계 정보 (조회수, 좋아요, 댓글)

### 🌍 **지원 국가**
한국, 미국, 일본, 중국, 영국, 독일, 프랑스, 이탈리아, 스페인, 캐나다, 호주, 인도, 브라질, 러시아, 멕시코, 태국, 베트남, 인도네시아, 필리핀, 말레이시아

## 설치 방법

1. **저장소 클론**
```bash
git clone https://github.com/boneekim/youtube_live.git
cd youtube_live
```

2. **의존성 설치**
```bash
pip install -r requirements.txt
```

3. **환경 변수 설정**
```bash
cp .env.example .env
# .env 파일을 편집하여 YouTube API 키를 설정
```

4. **YouTube API 키 설정**
   - [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트 생성
   - YouTube Data API v3 활성화
   - API 키 생성
   - `.env` 파일에 API 키 추가:
     ```
     YOUTUBE_API_KEY=your_api_key_here
     ```

## 사용 방법

### 1. 앱 실행
```bash
streamlit run youtube_video_extractor.py
```

### 2. 검색하기
1. 사이드바에서 검색 키워드 입력
2. 검색할 국가 선택
3. 검색 결과 개수 및 정렬 방식 선택
4. 검색 버튼 클릭

### 3. 결과 확인
- 섬네일 이미지 확인
- 영상 제목 클릭하여 YouTube 이동
- 통계 보기 버튼으로 상세 정보 확인
- 설명 보기로 영상 설명 확인

## 파일 구조
```
youtube_live/
├── youtube_video_extractor.py  # 메인 애플리케이션
├── config.py                   # 설정 파일
├── requirements.txt            # 의존성 패키지
├── .env.example               # 환경 변수 예시
├── setup.sh                   # 설치 스크립트
├── utils.py                   # 유틸리티 스크립트
└── README.md                  # 문서
```

## 사용 예시

### 검색 예시
- **키워드**: "파이썬 강의"
- **국가**: 한국
- **결과**: 한국에서 인기 있는 파이썬 강의 영상들

### 결과 화면
- 3x7 그리드로 20개 영상 표시
- 각 영상마다 섬네일, 제목, 채널명, 업로드 일시
- 클릭하면 YouTube로 이동

## API 사용량 관리

YouTube Data API는 일일 할당량이 있습니다:
- 기본 할당량: 10,000 units/day
- 검색 1회: 약 100 units
- 통계 조회 1회: 약 1 unit

## 문제 해결

### API 키 오류
```
⚠️ YouTube API 키가 설정되지 않았습니다.
```
→ `.env` 파일에 올바른 API 키를 설정하세요.

### 할당량 초과
```
API 요청 오류: 403 Forbidden
```
→ 일일 API 할당량을 초과했습니다. 내일 다시 시도하세요.

### 검색 결과 없음
- 키워드를 다르게 입력해보세요
- 다른 국가를 선택해보세요
- 정렬 방식을 변경해보세요

## 개발자 정보

- **개발자**: boneekim
- **GitHub**: https://github.com/boneekim/youtube_live
- **이메일**: boneekim@example.com

## 라이센스

MIT License

## 업데이트 내역

### v1.0.0 (2024.07.13)
- 초기 버전 릴리스
- 키워드 및 국가별 검색 기능
- 섬네일 그리드 표시
- 영상 통계 정보 표시
- 20개국 지원
