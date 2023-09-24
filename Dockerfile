FROM runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel
#always build with --platform linux/amd64

RUN apt update
RUN apt-get install -y python3 python3-pip
RUN apt install -y git
RUN apt install -y ffmpeg

#clone repo files
RUN git clone https://github.com/flyingjebi/instructblip.git
#install packages
RUN pip install -r instructblip/requirements.txt
RUN pip install requests==2.31.0
RUN pip install runpod

#when running
CMD [ "python3", "-u", "/instructblip/runpod_handler.py" ]