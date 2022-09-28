FROM python:3.10-alpine
COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8888"]