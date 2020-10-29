FROM python:3
RUN apt update; \
    apt -y install \
#Simulate screen
        xvfb \
#Just convenience
        nano \
#PIL (matplotlib) requirements
        libtiff5-dev libjpeg-dev libopenjp2-7-dev zlib1g-dev \
        libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
        libharfbuzz-dev libfribidi-dev libxcb1-dev \
#pytables requirements
        libhdf5-serial-dev
RUN pip install cython; pip install tables
WORKDIR boulder-stats
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
ENTRYPOINT [ "python", "click_cli.py"]
