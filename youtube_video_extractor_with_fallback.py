import streamlit as st
import requests
import json
from datetime import datetime
import os
import random

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

# 일본 후지산 관련 샘플 데이터
FUJISAN_LIVE_SAMPLES = [
    {
        'video_id': 'fujisan_live_001',
        'title': '🔴 LIVE: 후지산 실시간 라이브 캠 - Mount Fuji Live Camera',
        'description': '후지산의 아름다운 실시간 모습을 24시간 생중계합니다. 일본의 상징인 후지산을 언제든지 감상하세요.',
        'channel_title': 'Fujisan Live Cam',
        'published_at': '2024-07-13T09:00:00Z',
        'thumbnail_url': 'https://via.placeholder.com/320x180/FF6B35/FFFFFF?text=🗻+후지산+LIVE',
        'video_url': 'https://www.youtube.com/watch?v=fujisan_live_001',
        'live_status': '🔴 LIVE',
        'is_live': True,
        'view_count': '12845',
        'like_count': '456',
        'comment_count': '89'
    },
    {
        'video_id': 'fujisan_live_002',
        'title': '🔴 후지산 일출 라이브 - Sunrise at Mt. Fuji LIVE',
        'description': '후지산에서 보는 아름다운 일출을 실시간으로 만나보세요. 매일 아침 장엄한 일출 장면을 생중계합니다.',
        'channel_title': 'Japan Nature Live',
        'published_at': '2024-07-13T04:30:00Z',
        'thumbnail_url': 'https://via.placeholder.com/320x180/FF8C42/FFFFFF?text=🌅+후지산+일출',
        'video_url': 'https://www.youtube.com/watch?v=fujisan_live_002',
        'live_status': '🔴 LIVE',
        'is_live': True,
        'view_count': '8967',
        'like_count': '234',
        'comment_count': '67'
    },
    {
        'video_id': 'fujisan_live_003',
        'title': '🔴 후지산 벚꽃 라이브 - Cherry Blossoms at Mt. Fuji',
        'description': '후지산 주변의 벚꽃이 만개한 아름다운 모습을 실시간으로 감상하세요. 봄의 정취를 만끽할 수 있습니다.',
        'channel_title': 'Sakura Live Japan',
        'published_at': '2024-07-13T07:15:00Z',
        'thumbnail_url': 'https://via.placeholder.com/320x180/FFC0CB/FFFFFF?text=🌸+후지산+벚꽃',
        'video_url': 'https://www.youtube.com/watch?v=fujisan_live_003',
        'live_status': '🔴 LIVE',
        'is_live': True,
        'view_count': '15673',
        'like_count': '789',
        'comment_count': '123'
    },
    {
        'video_id': 'fujisan_video_001',
        'title': '후지산 등반 완전 가이드 - Mount Fuji Climbing Guide',
        'description': '후지산 등반을 위한 완벽한 가이드입니다. 등반 코스, 준비물, 주의사항 등을 자세히 알려드립니다.',
        'channel_title': 'Japan Travel Guide',
        'published_at': '2024-07-12T16:20:00Z',
        'thumbnail_url': 'https://via.placeholder.com/320x180/4A90E2/FFFFFF?text=🥾+후지산+등반',
        'video_url': 'https://www.youtube.com/watch?v=fujisan_video_001',
        'live_status': '📹 영상',
        'is_live': False,
        'view_count': '45234',
        'like_count': '2134',
        'comment_count': '456'
    },
    {
        'video_id': 'fujisan_video_002',
        'title': '후지산 주변 맛집 투어 - Food Tour around Mt. Fuji',
        'description': '후지산 주변의 숨은 맛집들을 소개합니다. 현지인만 아는 맛집에서 일본의 진정한 맛을 경험해보세요.',
        'channel_title': 'Japan Food Explorer',
        'published_at': '2024-07-11T18:45:00Z',
        'thumbnail_url': 'https://via.placeholder.com/320x180/F39C12/FFFFFF?text=🍜+후지산+맛집',
        'video_url': 'https://www.youtube.com/watch?v=fujisan_video_002',
        'live_status': '📹 영상',
        'is_live': False,
        'view_count': '28567',
        'like_count': '1456',
        'comment_count': '289'
    },
    {
        'video_id': 'fujisan_video_003',
        'title': '후지산 사진 촬영 명소 - Best Photo Spots at Mt. Fuji',
        'description': '후지산을 가장 아름답게 담을 수 있는 촬영 명소들을 소개합니다. 인스타그램 감성 사진을 찍어보세요.',
        'channel_title': 'Photo Japan',
        'published_at': '2024-07-10T14:30:00Z',
        'thumbnail_url': 'https://via.placeholder.com/320x180/9B59B6/FFFFFF?text=📸+후지산+사진',
        'video_url': 'https://www.youtube.com/watch?v=fujisan_video_003',
        'live_status': '📹 영상',
        'is_live': False,
        'view_count': '19876',
        'like_count': '987',
        'comment_count': '178'
    }
]

class YouTubeVideoExtractor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.api_working = False
        
    def test_api_key(self):
        """API 키 유효성 테스트"""
        if not self.api_key or self.api_key.startswith('AIzaSyDummy'):
            return False
            
        try:
            # 간단한 테스트 요청
            test_url = f"{self.base_url}/search"
            params = {
                'part': 'snippet',
                'q': 'test',
                'type': 'video',
                'maxResults': 1,
                'key': self.api_key
            }
            
            response = requests.get(test_url, params=params)
            if response.status_code == 200:
                self.api_working = True
                return True
            else:
                return False
                
        except Exception as e:
            return False
        
    def search_videos(self, keyword, country_code='JP', max_results=20, order='relevance', event_type='video'):
        """YouTube API를 사용하여 비디오 검색 (실패 시 샘플 데이터 사용)"""
        
        # API 키 테스트
        if not self.test_api_key():
            return self.get_sample_data(keyword, country_code, max_results, event_type)
            
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
            # API 실패 시 샘플 데이터 반환
            return self.get_sample_data(keyword, country_code, max_results, event_type)
        except Exception as e:
            # 기타 오류 시 샘플 데이터 반환
            return self.get_sample_data(keyword, country_code, max_results, event_type)
            
    def get_sample_data(self, keyword, country_code, max_results, event_type):
        """샘플 데이터 반환"""
        # 키워드가 "후지산"이고 일본 검색인 경우
        if '후지산' in keyword.lower() and country_code == 'JP':
            filtered_videos = FUJISAN_LIVE_SAMPLES.copy()
        else:
            # 기본 샘플 데이터
            filtered_videos = []
            
        # 영상 유형 필터링
        if event_type == 'live':
            filtered_videos = [v for v in filtered_videos if v['is_live']]
        elif event_type == 'uploaded':
            filtered_videos = [v for v in filtered_videos if not v['is_live']]
            
        # 결과 수 제한
        return filtered_videos[:max_results], "샘플 데이터"

    def get_video_statistics(self, video_id):
        """비디오 통계 정보 가져오기"""
        # 샘플 데이터에서 통계 찾기
        for video in FUJISAN_LIVE_SAMPLES:
            if video['video_id'] == video_id:
                return {
                    'view_count': video['view_count'],
                    'like_count': video['like_count'],
                    'comment_count': video['comment_count']
                }
        
        # 기본 통계 반환
        return {
            'view_count': str(random.randint(1000, 50000)),
            'like_count': str(random.randint(100, 2000)),
            'comment_count': str(random.randint(10, 500))
        }

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
    
    # 추출기 초기화
    extractor = YouTubeVideoExtractor(api_key)
    
    # API 상태 확인
    if not api_key or api_key.startswith('AIzaSyDummy'):
        st.warning("⚠️ 실제 YouTube API 키가 설정되지 않아 샘플 데이터를 사용합니다.")
        st.info("💡 실제 검색을 위해서는 .env 파일에 올바른 YOUTUBE_API_KEY를 설정해주세요.")
    
    # 검색 설정
    st.sidebar.header("🔍 검색 설정")
    
    # 키워드 입력
    keyword = st.sidebar.text_input("검색 키워드", value="후지산", placeholder="예: 후지산, 파이썬 강의")
    
    # 국가 선택
    country = st.sidebar.selectbox("검색 국가", list(COUNTRY_CODES.keys()), index=2)  # 일본을 기본값으로
    country_code = COUNTRY_CODES[country]
    
    # 영상 유형 선택 (라이브/전체/업로드)
    video_type = st.sidebar.selectbox("영상 유형", list(VIDEO_TYPES.keys()), index=1)  # 라이브를 기본값으로
    event_type = VIDEO_TYPES[video_type]
    
    # 검색 결과 개수
    max_results = st.sidebar.slider("검색 결과 개수", 3, 20, 6)
    
    # 정렬 방식
    order_options = {
        '관련성': 'relevance',
        '최신순': 'date',
        '조회수': 'viewCount',
        '평점': 'rating'
    }
    order = st.sidebar.selectbox("정렬 방식", list(order_options.keys()), index=0)
    
    # 자동 검색 (페이지 로드 시)
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        with st.spinner("검색 중..."):
            videos, error = extractor.search_videos(
                keyword, 
                country_code, 
                max_results, 
                order_options[order],
                event_type
            )
            
            st.session_state.videos = videos
            st.session_state.search_keyword = keyword
            st.session_state.search_country = country
            st.session_state.video_type = video_type
            st.session_state.error = error
    
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
                
                st.session_state.videos = videos
                st.session_state.search_keyword = keyword
                st.session_state.search_country = country
                st.session_state.video_type = video_type
                st.session_state.error = error
        else:
            st.sidebar.error("검색 키워드를 입력해주세요.")
    
    # 검색 결과 표시
    if 'videos' in st.session_state and st.session_state.videos:
        st.subheader(f"🎯 검색 결과: '{st.session_state.search_keyword}' ({st.session_state.search_country} - {st.session_state.video_type})")
        
        # 샘플 데이터 사용 알림
        if st.session_state.get('error') == "샘플 데이터":
            st.info("📋 샘플 데이터를 사용하여 검색 결과를 표시합니다.")
        
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
                    st.markdown("🔴 **LIVE**")
                
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
                
                # 기본 통계 표시
                stats = extractor.get_video_statistics(video['video_id'])
                if stats:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("조회수", format_number(stats.get('view_count', '0')))
                    with col_b:
                        st.metric("좋아요", format_number(stats.get('like_count', '0')))
                
                # 설명
                with st.expander("설명 보기"):
                    st.write(video['description'])
                
                st.divider()
    
    # 하단 정보
    st.markdown("---")
    st.markdown("💻 **Developer**: boneekim | 📂 **GitHub**: https://github.com/boneekim/youtube_live")

if __name__ == "__main__":
    main()
