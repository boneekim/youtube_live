# YouTube Live Streamer

## 프로젝트 설명
boneekim의 YouTube 라이브 스트리밍 도구입니다.

## 설치 방법

1. 가상환경 생성
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scriptsctivate
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 편집하여 YouTube API 키 등을 설정
```

## 사용 방법

### 1. Streamlit 앱 실행
```bash
streamlit run youtube_live_streamer.py
```

### 2. 설정
- YouTube Studio에서 스트림 키 획득
- 앱의 사이드바에 스트림 키 입력
- 카메라 설정 후 스트리밍 시작

## 기능

- 실시간 카메라 피드
- YouTube Live 스트리밍
- 스트리밍 상태 모니터링
- 실시간 통계 (시청자 수, 좋아요, 댓글)

## 필요한 API 키

1. YouTube Data API v3 키
2. YouTube Live Streaming API 권한

## 개발자

- **boneekim**
- GitHub: https://github.com/boneekim/youtube_live

## 라이센스

MIT License
