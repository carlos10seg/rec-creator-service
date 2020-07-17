FROM python:3.8-buster

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5010

CMD ["python", "app.py"]