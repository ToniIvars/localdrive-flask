FROM python:slim

WORKDIR /localdrive
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

CMD [ "gunicorn", "drive:create_app()", "-b", ":5000" ]