FROM python:3.8 

WORKDIR /usr/local/src/app

RUN apt-get update && apt-get install -y python3-pip

RUN pip3 install tensorflow
RUN pip3 install keras

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m pip install Pillow
COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]