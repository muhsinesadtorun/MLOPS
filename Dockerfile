FROM python:3.8

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install tensorflow
RUN pip install keras
RUN pip install joblib
RUN pip install numpy
RUN pip install keras-utils

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]