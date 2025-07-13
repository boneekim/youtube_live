import streamlit as st
import numpy as np
from datetime import datetime
import json
import os

# Try to import OpenCV with error handling
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError as e:
    OPENCV_AVAILABLE = False

class YouTubeLiveStreamer:
    def __init__(self):
        self.stream_key = None
        self.camera = None
        self.is_streaming = False
        self.opencv_available = OPENCV_AVAILABLE
        
    def setup_camera(self):
        """카메라 설정"""
        if not self.opencv_available:
            st.error("OpenCV가 설치되지 않아 카메라 기능을 사용할 수 없습니다.")
            return False
            
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                st.error("카메라를 열 수 없습니다.")
                return False
            return True
        except Exception as e:
            st.error(f"카메라 설정 중 오류 발생: {e}")
            return False
    
    def start_stream(self, stream_key):
        """라이브 스트리밍 시작"""
        self.stream_key = stream_key
        self.is_streaming = True
        st.success("라이브 스트리밍이 시작되었습니다!")
        
    def stop_stream(self):
        """라이브 스트리밍 중지"""
        self.is_streaming = False
        if self.camera and self.opencv_available:
            self.camera.release()
        st.info("라이브 스트리밍이 중지되었습니다.")
        
    def get_stream_info(self):
        """스트리밍 정보 반환"""
        return {
            "timestamp": datetime.now().isoformat(),
            "status": "streaming" if self.is_streaming else "stopped",
            "stream_key": self.stream_key,
            "opencv_available": self.opencv_available
        }

def main():
    st.set_page_config(
        page_title="YouTube Live Streamer",
        page_icon="🎥",
        layout="wide"
    )
    
    st.title("🎥 YouTube Live Streamer")
    st.markdown("### boneekim의 YouTube 라이브 스트리밍 도구")
    
    # OpenCV 상태 표시
    if OPENCV_AVAILABLE:
        st.success("✅ OpenCV 사용 가능 - 카메라 기능 활성화")
    else:
        st.warning("⚠️ OpenCV 사용 불가 - 제한된 기능으로 실행")
        st.info("Streamlit Cloud에서는 OpenCV가 제한될 수 있습니다. 로컬 환경에서 전체 기능을 사용하세요.")
    
    streamer = YouTubeLiveStreamer()
    
    # 사이드바 설정
    with st.sidebar:
        st.header("🛠️ 스트리밍 설정")
        
        # 스트림 키 입력
        stream_key = st.text_input("YouTube 스트림 키", type="password", 
                                  help="YouTube Studio에서 스트림 키를 복사하여 붙여넣으세요.")
        
        st.divider()
        
        # 카메라 설정 (OpenCV 사용 가능한 경우에만)
        if OPENCV_AVAILABLE:
            if st.button("📷 카메라 설정", use_container_width=True):
                if streamer.setup_camera():
                    st.success("카메라 설정 완료!")
        else:
            st.info("카메라 기능은 OpenCV가 필요합니다.")
        
        st.divider()
        
        # 스트리밍 제어
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ 시작", use_container_width=True):
                if stream_key:
                    streamer.start_stream(stream_key)
                else:
                    st.error("스트림 키를 입력해주세요.")
        
        with col2:
            if st.button("⏹️ 중지", use_container_width=True):
                streamer.stop_stream()
    
    # 메인 영역
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📺 라이브 프리뷰")
        
        if streamer.is_streaming:
            st.success("🔴 LIVE - 스트리밍 중...")
            if not OPENCV_AVAILABLE:
                st.info("실제 카메라 피드는 로컬 환경에서 OpenCV와 함께 사용하세요.")
        else:
            st.info("📹 스트리밍 대기 중...")
            
        # 데모 이미지 표시
        st.image("https://via.placeholder.com/640x360/1f1f1f/ffffff?text=Camera+Feed", 
                caption="카메라 피드 (데모)")
    
    with col2:
        st.subheader("📊 스트리밍 정보")
        
        # 스트리밍 정보 표시
        info = streamer.get_stream_info()
        st.json(info)
        
        st.divider()
        
        st.subheader("📈 실시간 통계")
        
        # 통계 메트릭
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.metric("시청자 수", "0", delta="0")
            st.metric("좋아요 수", "0", delta="0")
        
        with col_b:
            st.metric("댓글 수", "0", delta="0")
            st.metric("실시간 채팅", "0", delta="0")
        
        st.divider()
        
        # 시스템 정보
        st.subheader("🔧 시스템 정보")
        st.info(f"OpenCV: {'✅ 사용 가능' if OPENCV_AVAILABLE else '❌ 사용 불가'}")
        st.info(f"Python: {os.sys.version.split()[0]}")
        st.info(f"Streamlit: {st.__version__}")
    
    # 하단 정보
    st.divider()
    st.markdown("""
    ### 📝 사용 방법
    1. **스트림 키 설정**: YouTube Studio에서 스트림 키를 복사하여 사이드바에 입력
    2. **카메라 설정**: 카메라 설정 버튼 클릭 (OpenCV 필요)
    3. **스트리밍 시작**: 시작 버튼 클릭으로 라이브 스트리밍 시작
    4. **모니터링**: 실시간 통계 및 상태 확인
    
    ### 🔧 문제 해결
    - **OpenCV 오류**: Streamlit Cloud에서는 OpenCV가 제한됩니다. 로컬 환경 사용 권장
    - **카메라 접근 오류**: 브라우저 권한 설정 확인
    - **스트리밍 문제**: YouTube Studio의 스트림 설정 확인
    """)
    
    st.markdown("---")
    st.markdown("💻 **Developer**: boneekim | 📂 **GitHub**: https://github.com/boneekim/youtube_live")

if __name__ == "__main__":
    main()
