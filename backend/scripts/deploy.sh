#!/bin/bash

# AWS CLI 설치
# sudo apt update
# sudo apt install -y awscli

cd /var/www/flask

# S3에서 파일 복사
aws s3 cp s3://ai-htp-test-backend /

# 가상 환경 설정
python3 -m venv ai-htp-test-env
source ai-htp-test-env/bin/activate

# 필요한 패키지 설치
pip install -r requirements.txt

# Flask 애플리케이션 실행
export FLASK_APP=app.py
flask run --host=0.0.0.0
