# Version 0.3
# 显示该镜像是基于 debian:stretch 镜像
FROM debian:stretch
# 维护人信息
MAINTAINER tanliang tanjnr@gmail.com

# 设置debian的镜像，加快速度
#RUN echo 'deb http://mirrors.163.com/debian/ stretch main non-free contrib' > /etc/apt/sources.list \
#    && echo 'deb http://mirrors.163.com/debian/ stretch-updates main non-free contrib' >> /etc/apt/sources.list \
#    && echo 'deb http://mirrors.163.com/debian/ stretch-backports main non-free contrib' >> /etc/apt/sources.list \
#    && echo 'deb http://mirrors.163.com/debian-security/ stretch/updates main non-free contrib' >> /etc/apt/sources.list

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 添加php源
RUN apt-get update -yqq
RUN apt-get install -yqq wget
RUN wget -O /etc/apt/trusted.gpg.d/php.gpg https://mirror.xtom.com.hk/sury/php/apt.gpg
RUN apt-get install -yqq apt-transport-https
RUN sh -c 'echo "deb https://packages.sury.org/php/ stretch main" > /etc/apt/sources.list.d/php.list'
RUN apt-get update -yqq
RUN apt-get install -yqq php7.1 php7.1-fpm php7.1-redis php7.1-mysql php7.1-curl php7.1-xml php7.1-json php7.1-zip php7.1-bcmath php7.1-mbstring php7.1-mcrypt php7.1-gd php7.1-common
RUN sed -i 's/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/' /etc/php/7.1/fpm/php.ini

RUN apt-get install tzdata
RUN dpkg-reconfigure --frontend noninteractive tzdata

# 安装 ssh 软件
RUN apt-get install -yqq openssh-server
RUN mkdir -p /var/run/sshd
RUN mkdir -p /root/.ssh
# 取消pam限制
RUN sed -ri 's/session  required   pam_loginuid.so/#session    required  pam_loginuid.so/g' /etc/pam.d/sshd
# 复制配置文件到相应位置
COPY authorized_keys /root/.ssh/authorized_keys

# 更改语言 支持中文
RUN apt-get install -yqq locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# zh_CN.UTF-8 UTF-8/zh_CN.UTF-8 UTF-8/' /etc/locale.gen && \
    echo 'LANG="zh_CN.UTF-8"'>/etc/default/locale && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=zh_CN.UTF-8

# 安装php
RUN apt-get install -y php7.1 php7.1-fpm

# 安装更多服务
RUN apt-get install -yqq cron nginx
RUN echo "#!/bin/sh -e" > /etc/rc.local 
RUN echo "service ssh start" >> /etc/rc.local
RUN echo "service nginx start" >> /etc/rc.local
RUN echo "service cron start" >> /etc/rc.local
RUN echo "/etc/init.d/php7.1-fpm start" >> /etc/rc.local
RUN echo "su - ubuntu /tmp/start.sh" >> /etc/rc.local
RUN echo "exit 0" >> /etc/rc.local
RUN chmod 755 /etc/rc.local

# 增加用户
RUN apt-get install -yqq sudo vim
RUN useradd -d /home/ubuntu -m -s /bin/bash -G sudo ubuntu
RUN echo "ubuntu:ubuntu" |chpasswd
RUN touch /var/spool/cron/crontabs/ubuntu
RUN chmod 600 /var/spool/cron/crontabs/ubuntu
    
# 开放端口
EXPOSE 22 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99
