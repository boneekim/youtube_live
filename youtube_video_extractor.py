import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
from urllib.parse import quote
import os
from config import Config

# 국가 코드 매핑
COUNTRY_CODES = {
    '한국': 'KR',
    '미국': 'US',
    '일본': 'JP',
    '중국': 'CN',
    '영국': 'GB',
    '독일': 'DE',
    '프랑스': 'FR',
    '이탈리아': 'IT',
    '스페인': 'ES',
    '캐나다': 'CA',
    '호주': 'AU',
    '인도': 'IN',
    '브라질': 'BR',
    '러시아': 'RU',
    '멕시코': 'MX',
    '태국': 'TH',
    '베트남': 'VN',
    '인도네시아': 'ID',
    '필리핀': 'PH',
    '말레이시아': 'MY'
}

# 영상 유형 옵션
VIDEO_TYPES = {
    '전체': 'video',
    '라이브': 'live',
    '업로드된 영상': 'uploaded'
}

class YouTubeVideoExtractor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
    def search_videos(self, keyword, country_code='KR', max_results=20, order='relevance', event_type='video'):
        """YouTube API를 사용하여 비디오 검색"""
        try:
            # 검색 API 엔드포인트
            search_url = f"{self.base_url}/search"
            
            # 검색 파라미터
            params = {
                'part': 'snippet',
                'q': keyword,
                'type': 'video',
                'maxResults': max_results,
                'order': order,
                'regionCode': country_code,
                'key': self.api_key
            }
            
            # 라이브 스트리밍 필터 추가
            if event_type == 'live':
                params['eventType'] = 'live'
            elif event_type == 'uploaded':
                params['eventType'] = 'completed'
            
            # API 호출
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # 비디오 정보 처리
            videos = []
            for item in data.get('items', []):
                # 라이브 스트리밍 상태 확인
                live_status = '🔴 LIVE' if item['snippet'].get('liveBroadcastContent') == 'live' else '📹 영상'
                
                video_info = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'][:200] + '...' if len(item['snippet']['description']) > 200 else item['snippet']['description'],
                    'channel_title': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt'],
                    'thumbnail_url': item['snippet']['thumbnails']['medium']['url'],
                    'video_url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'live_status': live_status,
                    'is_live': item['snippet'].get('liveBroadcastContent') == 'live'
                }
                videos.append(video_info)
                
            return videos, None
            
        except requests.exceptions.RequestException as e:
            if response.status_code == 403:
                return [], "API 키가 올바르지 않거나 할당량이 초과되었습니다."
            elif response.status_code == 400:
                return [], "검색 파라미터가 올바르지 않습니다."
            else:
                return [], f"API 요청 오류: {str(e)}"
        except Exception as e:
            return [], f"검색 중 오류 발생: {str(e)}"

    def get_video_statistics(self, video_id):
        """비디오 통계 정보 가져오기"""
        try:
            stats_url = f"{self.base_url}/videos"
            params = {
                'part': 'statistics',
                'id': video_id,
                'key': self.api_key
            }
            
            response = requests.get(stats_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get('items'):
                stats = data['items'][0]['statistics']
                return {
                    'view_count': stats.get('viewCount', '0'),
                    'like_count': stats.get('likeCount', '0'),
                    'comment_count': stats.get('commentCount', '0')
                }
            return {}
            
        except Exception as e:
            return {}

def format_number(num_str):
    """숫자를 한국어 단위로 포맷팅"""
    try:
        num = int(num_str)
        if num >= 100000000:  # 1억 이상
            return f"{num // 100000000}억 {(num % 100000000) // 10000}만"
        elif num >= 10000:  # 1만 이상
            return f"{num // 10000}만 {(num % 10000) // 1000}천"
        elif num >= 1000:  # 1천 이상
            return f"{num // 1000}천 {num % 1000}"
        else:
            return str(num)
    except:
        return num_str

def main():
    st.set_page_config(
        page_title="YouTube 영상 추출기",
        page_icon="🎬",
        layout="wide"
    )
    
    st.title("🎬 YouTube 영상 추출기")
    st.markdown("### boneekim의 YouTube 영상 검색 도구")
    
    # API 키 확인
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        st.error("⚠️ YouTube API 키가 설정되지 않았습니다.")
        st.info("💡 .env 파일에 YOUTUBE_API_KEY를 설정해주세요.")
        st.code("YOUTUBE_API_KEY=your_api_key_here", language="bash")
        
        # 데모 버전 링크 제공
        st.markdown("---")
        st.info("🔗 API 키 없이 데모 버전을 사용하려면 `demo_youtube_extractor.py`를 실행하세요.")
        st.code("streamlit run demo_youtube_extractor.py", language="bash")
        st.stop()
    
    # 추출기 초기화
    extractor = YouTubeVideoExtractor(api_key)
    
    # 검색 설정
    st.sidebar.header("🔍 검색 설정")
    
    # 키워드 입력
    keyword = st.sidebar.text_input("검색 키워드", placeholder="예: 후지산, 파이썬 강의")
    
    # 국가 선택
    country = st.sidebar.selectbox("검색 국가", list(COUNTRY_CODES.keys()), index=2)  # 일본을 기본값으로
    country_code = COUNTRY_CODES[country]
    
    # 영상 유형 선택 (라이브/전체/업로드)
    video_type = st.sidebar.selectbox("영상 유형", list(VIDEO_TYPES.keys()), index=1)  # 라이브를 기본값으로
    event_type = VIDEO_TYPES[video_type]
    
    # 검색 결과 개수
    max_results = st.sidebar.slider("검색 결과 개수", 5, 50, 20)
    
    # 정렬 방식
    order_options = {
        '관련성': 'relevance',
        '최신순': 'date',
        '조회수': 'viewCount',
        '평점': 'rating'
    }
    order = st.sidebar.selectbox("정렬 방식", list(order_options.keys()), index=0)
    
    # 검색 버튼
    if st.sidebar.button("🔍 검색", use_container_width=True):
        if keyword:
            with st.spinner("검색 중..."):
                videos, error = extractor.search_videos(
                    keyword, 
                    country_code, 
                    max_results, 
                    order_options[order],
                    event_type
                )
                
                if error:
                    st.error(f"검색 오류: {error}")
                else:
                    st.session_state.videos = videos
                    st.session_state.search_keyword = keyword
                    st.session_state.search_country = country
                    st.session_state.video_type = video_type
        else:
            st.sidebar.error("검색 키워드를 입력해주세요.")
    
    # 검색 결과 표시
    if 'videos' in st.session_state and st.session_state.videos:
        st.subheader(f"🎯 검색 결과: '{st.session_state.search_keyword}' ({st.session_state.search_country} - {st.session_state.video_type})")
        
        # 라이브 스트리밍 개수 표시
        live_count = sum(1 for video in st.session_state.videos if video['is_live'])
        if live_count > 0:
            st.success(f"🔴 라이브 스트리밍 {live_count}개 포함")
        
        st.info(f"총 {len(st.session_state.videos)}개의 영상을 찾았습니다.")
        
        # 그리드 레이아웃으로 비디오 표시
        cols = st.columns(3)  # 3열 그리드
        
        for idx, video in enumerate(st.session_state.videos):
            col = cols[idx % 3]
            
            with col:
                # 섬네일 이미지
                st.image(video['thumbnail_url'], use_container_width=True)
                
                # 라이브 상태 표시
                if video['is_live']:
                    st.markdown(f"🔴 **LIVE**")
                
                # 제목 (클릭 가능한 링크)
                st.markdown(f"**[{video['title']}]({video['video_url']})**")
                
                # 채널명
                st.caption(f"📺 {video['channel_title']}")
                
                # 업로드 일시
                try:
                    published_date = datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
                    st.caption(f"📅 {published_date.strftime('%Y-%m-%d %H:%M')}")
                except:
                    st.caption(f"📅 {video['published_at']}")
                
                # 설명
                with st.expander("설명 보기"):
                    st.write(video['description'])
                
                # 비디오 통계 (옵션)
                if st.button(f"📊 통계 보기", key=f"stats_{idx}"):
                    with st.spinner("통계 로딩 중..."):
                        stats = extractor.get_video_statistics(video['video_id'])
                        if stats:
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.metric("조회수", format_number(stats.get('view_count', '0')))
                                st.metric("좋아요", format_number(stats.get('like_count', '0')))
                            with col_b:
                                st.metric("댓글", format_number(stats.get('comment_count', '0')))
                        else:
                            st.error("통계 정보를 가져올 수 없습니다.")
                
                st.divider()
    else:
        # 초기 화면
        st.info("🔍 왼쪽 사이드바에서 키워드와 국가를 선택한 후 검색 버튼을 클릭하세요.")
        
        # 사용 예시
        st.markdown("""
        ### 📖 사용 방법
        
        1. **키워드 입력**: 검색하고 싶은 키워드를 입력하세요
           - 예시: "후지산", "도쿄", "일본 여행", "벚꽃"
        2. **국가 선택**: 검색할 국가를 선택하세요 (기본: 일본)
        3. **영상 유형**: 라이브/전체/업로드된 영상 중 선택
        4. **검색 옵션**: 결과 개수와 정렬 방식을 선택하세요
        5. **검색 실행**: 검색 버튼을 클릭하세요
        
        ### 🔴 라이브 스트리밍 검색
        - **영상 유형**에서 "라이브"를 선택하면 현재 라이브 중인 영상만 검색
        - 라이브 영상은 🔴 LIVE 표시로 구분
        - 실시간 방송 중인 영상을 바로 시청 가능
        
        ### 🌟 주요 기능
        - 🔍 키워드 및 국가별 YouTube 영상 검색
        - 🔴 라이브 스트리밍 전용 검색 필터
        - 🖼️ 섬네일 이미지와 함께 결과 표시
        - 📊 영상 통계 정보 (조회수, 좋아요, 댓글)
        - 🔗 YouTube 영상 직접 링크
        - 📅 업로드 일시 표시
        
        ### 💡 검색 팁
        - **후지산**: 일본의 후지산 관련 영상 검색
        - **도쿄 라이브**: 도쿄 실시간 라이브 캠
        - **일본 여행**: 일본 여행 관련 콘텐츠
        - **벚꽃**: 벚꽃 시즌 관련 영상
        """)
    
    # 하단 정보
    st.markdown("---")
    st.markdown("💻 **Developer**: boneekim | 📂 **GitHub**: https://github.com/boneekim/youtube_live")

if __name__ == "__main__":
    main()
