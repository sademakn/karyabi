FROM python

LABEL maintainer="Sajjad Dehghani"

COPY ./requirements.txt /app/

RUN pip install -r /app/requirements.txt

WORKDIR /app
COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]