FROM python:3

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y nodejs npm
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install -g bower


RUN mkdir /code
WORKDIR /code

ADD ./requirements.txt /code
RUN pip install -r requirements.txt

ADD ./bower.json /code
RUN echo '{ "allow_root": true }' > /root/.bowerrc
RUN bower install

ADD ./ /code

RUN mv /code/bower_components /code/app/bower_components

CMD ["python", "app.py"]

