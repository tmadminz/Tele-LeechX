FROM ubuntu:20.04


RUN mkdir ./app
RUN chmod 777 ./app
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

RUN apt -qq update --fix-missing && \
    apt -qq install -y git \
    aria2 \
    wget \
    curl \
    busybox \
    unzip \
    unrar \
    tar \
    python3 \
    ffmpeg \
    python3-pip \
    p7zip-full \
    p7zip-rar

#Link Parsers By yusuf
RUN wget -O /usr/bin/gdtot "https://tgstreamerbot.akuotoko.repl.co/1673806755639796/gdtot" && \
chmod +x /usr/bin/gdtot && \
wget -O /usr/bin/gp "https://tgstreamerbot.akuotoko.repl.co/1660131579769332/gp" && \
chmod +x /usr/bin/gp && \
echo '{"url":"https://new.gdtot.top/","cookie":"PHPSESSID=oqfihh3ic4emg9agvobemdg18a; _ga=GA1.2.1497265010.1637937185; _gid=GA1.2.433271470.1637937185; _gat_gtag_UA_130203604_4=1; crypt=S3htTzl3aDdHUWdJWDhLZVV2MlpSVGlkZ0RVYU0xc29oQlNKSENGakRaOD0%3D"}' > cookies.txt 
#use your own gdtot cookies don't use with my...

RUN wget https://rclone.org/install.sh
RUN bash install.sh

RUN mkdir /app/gautam
RUN wget -O /app/gautam/gclone.gz https://git.io/JJMSG
RUN gzip -d /app/gautam/gclone.gz
RUN chmod 0775 /app/gautam/gclone

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x extract
CMD ["bash","start.sh"]
