import streamlit as st
import json
from datetime import datetime
import random

# 데모 데이터 (실제 API 대신 사용)
DEMO_VIDEOS = [
    {
        'video_id': 'dQw4w9WgXcQ',
        'title': 'Python 기초 강의 - 변수와 데이터 타입',
        'description': '파이썬 프로그래밍의 기초를 배워보세요. 변수 선언과 다양한 데이터 타입에 대해 알아봅니다.',
        'channel_title': 'CodeWithBonee',
        'published_at': '2024-07-10T10:00:00Z',
        'thumbnail_url': 'https://via.placeholder.com/320x180/FF0000/FFFFFF?text=Python+Tutorial',
        'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'view_count': '15234',
        'like_count': '892',
        'comment_count': '156'
    },
    {
        'video_id': 'abc123def456',
        'title': '웹 개발 완전 정복 - HTML, CSS, JavaScript',
        'description': '웹 개발의 기초부터 고급까지 모든 것을 배워보세요. 실습 위주의 강의로 실무 능력을 키워보세요.',
        'channel_title': 'WebDev Master',
        'published_at': '2024-07-09T14:30:00Z',
        'thumbnail_url': 'https://via.placeholder.com/320x180/00FF00/FFFFFF?text=Web+Development',
        'video_url': 'https://www.youtube.com/watch?v=abc123def456',
        'view_count': '28567',
        'like_count': '1234',
        'comment_count': '289'
    },
    {
        'video_id': 'xyz789ghi012',
        'title': '머신러닝 입문 - 파이썬으로 시작하는 AI',
        'description': '머신러닝의 기본 개념부터 실제 구현까지 단계별로 배워보세요. 실무에서 바로 사용할 수 있는 내용들을 담았습니다.',
        'channel_title': 'AI Learning Hub',
        'published_at': '2024-07-08T09:15:00Z',
        'thumbnail_url': 'https://via.placeholder.com/320x180/0000FF/FFFFFF?text=Machine+Learning',
        'video_url': 'https://www.youtube.com/watch?v=xyz789ghi012',
        'view_count': '45892',
        'like_count': '2156',
        'comment_count': '445'
    },
    {
        'video_id': 'demo001',
        'title': '데이터 과학을 위한 판다스 완전 가이드',
        'description': '데이터 분석의 핵심 라이브러리인 판다스를 마스터하세요. 실제 데이터를 활용한 분석 실습을 포함합니다.',
        'channel_title': 'Data Science Pro',
        'published_at': '2024-07-07T16:45:00Z',
        'thumbnail_url': 'https://via.placeholder.com/320x180/FF6600/FFFFFF?text=Pandas+Tutorial',
        'video_url': 'https://www.youtube.com/watch?v=demo001',
        'view_count': '12456',
        'like_count': '678',
        'comment_count': '123'
    },
    {
        'video_id': 'demo002',
        'title': 'React 개발 실무 강의 - 컴포넌트부터 배포까지',
        'description': 'React를 이용한 모던 웹 개발을 배워보세요. 실제 프로젝트를 만들어가며 배우는 실무 중심 강의입니다.',
        'channel_title': 'Frontend Masters',
        'published_at': '2024-07-06T11:20:00Z',
        'thumbnail_url': 'https://via.placeholder.com/320x180/61DAFB/FFFFFF?text=React+Tutorial',
        'video_url': 'https://www.youtube.com/watch?v=demo002',
        'view_count': '34567',
        'like_count': '1890',
        'comment_count': '356'
    },
    {
        'video_id': 'demo003',
        'title': 'Node.js 백엔드 개발 마스터클래스',
        'description': 'Node.js를 이용한 서버 개발을 배워보세요. REST API 설계부터 데이터베이스 연동까지 모든 것을 다룹니다.',
        'channel_title': 'Backend Guru',
        'published_at': '2024-07-05T13:10:00Z',
        'thumbnail_url': 'https://via.placeholder.com/320x180/68A063/FFFFFF?text=Node.js+Backend',
        'video_url': 'https://www.youtube.com/watch?v=demo003',
        'view_count': '23456',
        'like_count': '1123',
        'comment_count': '267'
    }
]

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

def search_demo_videos(keyword, country_code, max_results):
    """데모 비디오 검색 (실제 API 대신 사용)"""
    # 키워드에 따라 다른 결과 반환
    filtered_videos = []
    
    for video in DEMO_VIDEOS:
        if keyword.lower() in video['title'].lower() or keyword.lower() in video['description'].lower():
            filtered_videos.append(video)
    
    # 결과가 없으면 모든 비디오 반환
    if not filtered_videos:
        filtered_videos = DEMO_VIDEOS
    
    # 무작위로 섞고 최대 결과 수만큼 반환
    random.shuffle(filtered_videos)
    return filtered_videos[:max_results]

def main():
    st.set_page_config(
        page_title="YouTube 영상 추출기 (데모)",
        page_icon="🎬",
        layout="wide"
    )
    
    st.title("🎬 YouTube 영상 추출기 (데모 버전)")
    st.markdown("### boneekim의 YouTube 영상 검색 도구")
    
    # 데모 알림
    st.warning("⚠️ 이것은 데모 버전입니다. 실제 YouTube API 대신 샘플 데이터를 사용합니다.")
    
    # 검색 설정
    st.sidebar.header("🔍 검색 설정")
    
    # 키워드 입력
    keyword = st.sidebar.text_input("검색 키워드", placeholder="예: 파이썬 강의")
    
    # 국가 선택
    country = st.sidebar.selectbox("검색 국가", list(COUNTRY_CODES.keys()), index=0)
    country_code = COUNTRY_CODES[country]
    
    # 검색 결과 개수
    max_results = st.sidebar.slider("검색 결과 개수", 3, 6, 6)
    
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
                # 데모 검색 수행
                videos = search_demo_videos(keyword, country_code, max_results)
                st.session_state.videos = videos
                st.session_state.search_keyword = keyword
                st.session_state.search_country = country
        else:
            st.sidebar.error("검색 키워드를 입력해주세요.")
    
    # 검색 결과 표시
    if 'videos' in st.session_state and st.session_state.videos:
        st.subheader(f"🎯 검색 결과: '{st.session_state.search_keyword}' ({st.session_state.search_country})")
        st.info(f"총 {len(st.session_state.videos)}개의 영상을 찾았습니다. (데모 데이터)")
        
        # 그리드 레이아웃으로 비디오 표시
        cols = st.columns(3)  # 3열 그리드
        
        for idx, video in enumerate(st.session_state.videos):
            col = cols[idx % 3]
            
            with col:
                # 섬네일 이미지
                st.image(video['thumbnail_url'], use_column_width=True)
                
                # 제목 (클릭 가능한 링크)
                st.markdown(f"**[{video['title']}]({video['video_url']})**")
                
                # 채널명
                st.caption(f"📺 {video['channel_title']}")
                
                # 업로드 일시
                published_date = datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
                st.caption(f"📅 {published_date.strftime('%Y-%m-%d %H:%M')}")
                
                # 통계 정보
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("조회수", format_number(video['view_count']))
                with col_b:
                    st.metric("좋아요", format_number(video['like_count']))
                
                # 설명
                with st.expander("설명 보기"):
                    st.write(video['description'])
                
                st.divider()
    else:
        # 초기 화면
        st.info("🔍 왼쪽 사이드바에서 키워드와 국가를 선택한 후 검색 버튼을 클릭하세요.")
        
        # 사용 예시
        st.markdown("""
        ### 📖 사용 방법 (데모 버전)
        
        1. **키워드 입력**: 검색하고 싶은 키워드를 입력하세요
           - 예시: "파이썬", "웹 개발", "머신러닝", "React", "Node.js"
        2. **국가 선택**: 검색할 국가를 선택하세요
        3. **검색 옵션**: 결과 개수와 정렬 방식을 선택하세요
        4. **검색 실행**: 검색 버튼을 클릭하세요
        
        ### 🎯 데모 키워드 추천
        - **"파이썬"** - 파이썬 관련 강의
        - **"웹"** - 웹 개발 관련 영상
        - **"머신러닝"** - AI/ML 관련 콘텐츠
        - **"React"** - 프론트엔드 개발
        - **"데이터"** - 데이터 과학 관련
        
        ### 🔧 실제 버전 사용하기
        실제 YouTube API를 사용하려면:
        1. `.env` 파일에 `YOUTUBE_API_KEY` 설정
        2. `youtube_video_extractor.py` 실행
        """)
    
    # 하단 정보
    st.markdown("---")
    st.markdown("💻 **Developer**: boneekim | 📂 **GitHub**: https://github.com/boneekim/youtube_live")

if __name__ == "__main__":
    main()
