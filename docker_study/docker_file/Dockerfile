FROM python:3.6-alpine

RUN apk add --no-cache gcc musl-dev

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python"]

CMD ["app.py"]
