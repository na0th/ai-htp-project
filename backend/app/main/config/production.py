import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY=b'\xc3\x13\xe9%\xbdE]X\xb7Y\xdd\xea\xfeR9\x13'

# RDS 정보
RDS_HOST='ai-drawing-test-rds.c68obtazckig.ap-northeast-2.rds.amazonaws.com'
RDS_PORT=3306
RDS_USERNAME='admin'
RDS_PASSWORD=12345678
RDS_DATABASE='ai_drawing_test'

# AWS S3 정보
AWS_BUCKET_NAME='ai-htp-test'
AWS_ACCESS_KEY_ID='AKIA2GXUT4Q2DXDF7WRE'
AWS_SECRET_ACCESS_KEY='SrlMyL8xAq2nSKT4wa4gxuwM7K8EYU6cDYG0HW'
AWS_REGION='ap-northeast-2'
