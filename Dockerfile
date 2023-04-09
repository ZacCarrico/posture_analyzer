FROM mxnet/python:1.9.1_cpu_py3 

COPY ./*.py /root/posture_analyzer/
COPY requirements.txt /root/posture_analyzer/
COPY test.jpg /root/posture_analyzer/
WORKDIR /root/posture_analyzer/

RUN pip3 install -r requirements.txt
