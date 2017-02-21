FROM python:2

ADD worker.py /
ADD LoadTest.py /

RUN pip install pause

CMD [ "python", "/LoadTest.py", "--help" ]