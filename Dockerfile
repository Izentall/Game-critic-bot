FROM python:3.8
# set work directory
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
# copy project
COPY . /usr/src/app/
# install dependencies
RUN pip install -r requirements.txt
# run app
CMD ["python", "bot.py"]