FROM python:3.11-slim-buster

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

# Ensure the `data/database` directory exists
RUN mkdir -p /app/main/database

# Grant necessary permissions
RUN chmod -R 777 /app/main/database

ENV PYTHONPATH /app

EXPOSE 8080
ENTRYPOINT ["python", "main/controller/book_management_controller.py"]