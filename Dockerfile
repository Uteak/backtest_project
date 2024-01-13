FROM python:3.11.1

# ensures that the python output 
# i.e. the stdout and stderr streams are sent straight to terminal 
ENV PYTHONUNBUFFERED 1

ARG DEV=false

# 필수 패키지 설치
RUN apt-get update && \
    apt-get install -y curl build-essential

COPY . /home/
WORKDIR /home

# install this only if it is dev mode
RUN if [ $DEV = true ]; then pip install -r requirements.dev.txt; fi

# TA-Lib 설치
RUN curl -L http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz | tar xvz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install

# 필수 의존성 설치
RUN pip install --upgrade pip && \
    pip install ta-lib && \
    pip install django==4.1.5 && \
    pip install django-allauth==0.54.0 && \
    pip install djangorestframework==3.14.0 && \
    pip install drf-spectacular==0.25.1 && \ 
    pip install django-bootstrap4==23.2 && \
    pip install django-storages==1.14.2 && \
    pip install beautifulsoup4==4.12.2 && \
    pip install pandas==1.4.3 && \
    pip install finance-datareader==0.9.66 && \
    pip install dart-fss==0.4.7 && \
    pip install requests==2.31.0 && \
    pip install Backtesting==0.3.3 && \
    pip install matplotlib==3.5.2 && \
    pip install plotly==5.18.0

EXPOSE 8000
