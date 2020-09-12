FROM python:3.8
COPY . /tmp/nlp/
RUN pip install -r /tmp/nlp/requirements.txt
EXPOSE 8088
CMD python /tmp/nlp/run.py