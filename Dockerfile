FROM python:3.10.10-slim-bullseye

WORKDIR /code
# Install pg_config
RUN apt-get update && apt-get install -y libpq-dev gcc

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]