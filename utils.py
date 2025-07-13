#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import argparse

def run_command(command):
    """명령어 실행 및 결과 반환"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def setup_environment():
    """개발 환경 설정"""
    print('🔧 개발 환경을 설정합니다...')
    
    # 가상환경 생성
    success, output = run_command('python3 -m venv venv')
    if success:
        print('✅ 가상환경 생성 완료')
    else:
        print('❌ 가상환경 생성 실패:', output)
        return False
    
    # 의존성 설치
    success, output = run_command('venv/bin/pip install -r requirements.txt')
    if success:
        print('✅ 의존성 설치 완료')
    else:
        print('❌ 의존성 설치 실패:', output)
        return False
    
    return True

def run_app():
    """앱 실행"""
    print('🚀 YouTube Live Streamer를 실행합니다...')
    os.system('venv/bin/streamlit run youtube_live_streamer.py')

def clean_cache():
    """캐시 파일 정리"""
    print('�� 캐시 파일을 정리합니다...')
    
    cache_dirs = ['__pycache__', '.streamlit', 'venv/__pycache__']
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            run_command(f'rm -rf {cache_dir}')
            print(f'✅ {cache_dir} 정리 완료')

def main():
    parser = argparse.ArgumentParser(description='YouTube Live Streamer 유틸리티')
    parser.add_argument('command', choices=['setup', 'run', 'clean'], 
                       help='실행할 명령어')
    
    args = parser.parse_args()
    
    if args.command == 'setup':
        setup_environment()
    elif args.command == 'run':
        run_app()
    elif args.command == 'clean':
        clean_cache()

if __name__ == '__main__':
    main()
