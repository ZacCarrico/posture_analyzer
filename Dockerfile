FROM mxnet/python:1.9.1_cpu_py3 

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN mkdir non_analyzed_imgs
RUN mkdir analyzed_imgs
COPY test.jpg .
COPY ./*.py .


ENTRYPOINT ["python3", "analyze_images.py"]
