FROM python:3.7.2

# 필요한 파일을 이미지로 복사
COPY main/ /app/main/
COPY app.py /app/
COPY requirements.txt /app/
COPY ml_models/ /app/ml_models/

# 작업 디렉토리 설정
WORKDIR /app

RUN pip install --upgrade pip==23.1.2
RUN pip install -r requirements.txt
RUN pip3 install tensorflow

EXPOSE 5000
CMD ["python", "app.py"]

