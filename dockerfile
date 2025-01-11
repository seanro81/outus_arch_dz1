FROM python:3.12

WORKDIR /app
RUN python3 -m pip install --upgrade pip setuptools 
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY . .

CMD python main.py