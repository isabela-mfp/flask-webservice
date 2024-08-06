FROM python:3.9-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 32187
ENV FLASK_APP=app.py
CMD ["sh", "-c", "python createDatabase.py && python app.py"]