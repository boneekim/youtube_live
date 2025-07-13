import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class Config:
    # YouTube API 설정
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
    YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID', '')
    YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET', '')
    
    # 스트리밍 설정
    STREAM_QUALITY = os.getenv('STREAM_QUALITY', '720p')
    STREAM_BITRATE = os.getenv('STREAM_BITRATE', '2500')
    STREAM_FPS = int(os.getenv('STREAM_FPS', '30'))
    
    # 카메라 설정
    CAMERA_INDEX = int(os.getenv('CAMERA_INDEX', '0'))
    CAMERA_WIDTH = int(os.getenv('CAMERA_WIDTH', '1280'))
    CAMERA_HEIGHT = int(os.getenv('CAMERA_HEIGHT', '720'))
    
    # 기타 설정
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # RTMP 설정
    RTMP_URL = 'rtmp://a.rtmp.youtube.com/live2/'
    
    @classmethod
    def get_rtmp_url(cls, stream_key):
        """RTMP URL 생성"""
        return f"{cls.RTMP_URL}{stream_key}"
    
    @classmethod
    def validate_config(cls):
        """설정 유효성 검사"""
        required_fields = ['YOUTUBE_API_KEY']
        missing_fields = []
        
        for field in required_fields:
            if not getattr(cls, field):
                missing_fields.append(field)
        
        if missing_fields:
            return False, f"필수 설정이 누락되었습니다: {', '.join(missing_fields)}"
        
        return True, "설정이 완료되었습니다."
