FROM python:3.8
COPY . /tmp/nlp/
RUN pip install -r /tmp/nlp/requirements.txt
RUN mkdir /tmp/corpus/
RUN mkdir /tmp/nlp_tmp_files
EXPOSE 8088
CMD python /tmp/nlp/run.py