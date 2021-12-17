FROM python:3.8
# set work directory
WORKDIR /src

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src .

CMD ["python", "docker_script.py"]
