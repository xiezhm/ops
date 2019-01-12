# ops
运维常用ops

### docker run
```
docker run --name  debian_java \
       -p 8070:8070 -p 8031:22 \
       -v /home/ubuntu/java:/home/ubuntu/java \
       --restart=always \
       --network mynetwork --ip 172.18.0.21 \
       -d debian_java:0.4 
```

```
docker run --name debian_php \
	   -p 8021:22 \
	   -v  /home/ubuntu/php:/home/ubuntu/php \
	   -v /home/ubuntu/php/nginx/php-fpm.conf:/etc/php/7.1/fpm/pool.d/www.conf \
       -v /home/ubuntu/php/nginx/php_default:/etc/nginx/sites-enabled/default \
       -v /home/ubuntu/php/crontab/php_crontab.sh:/var/spool/cron/crontabs/ubuntu \
	   --network mynetwork --ip 172.18.0.21 \
       -idt debian_php:0.4 \
       /bin/bash -c "/etc/rc.local;/bin/bash
```

```
docker run --name debian_runner \
       -p 10022:22 \
       --network mynetwork --ip 172.18.0.100 \
       -idt debian_runner:0.4 \
       /bin/bash -c "/etc/rc.local;/bin/bash
```

```
mv  java_status.py /etc/zabbix/
chmod +x java_status.py
cat << EOF >/etc/zabbix/zabbix_agentd.d/userparameter_java.conf 
UserParameter=java.status[*],/etc/zabbix/java_status.py $1 $2 $3
EOF
```