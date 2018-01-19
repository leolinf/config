# docker redis 镜像的启动

                    目录挂载（起到数据备份作用）                                           指定配置文件
sudo docker run -v /mnt/redis/data:/data -d -p 6379:6379 --restart always --name myredis redis redis-server /mnt/redis/data/redis6379.conf

<https://github.com/faalin/Article/blob/master/redis6379.conf>

# rabbitmq docker 镜像配置问题

## 安装的rabbitmq default 版本

sudo docker pull rabbitmq 

              镜像名                     容器名          映射端口   images    

sudo docker run -d --restart always --hostname=rabbitmq --name my-rabbitmq -p 15672:15672 rabbitmq

## 启动web rabbitmq_management 

sudo docker exec -it my-rebbitmq bash

rabbitmq-plugins enable rabbitmq_management

## 默认的文件位置

=INFO REPORT==== 6-Jul-2015::20:47:02 ===

node           : rabbit@my-rabbit

home dir       : /var/lib/rabbitmq

config file(s) : /etc/rabbitmq/rabbitmq.config

cookie hash    : UoNOcDhfxW9uoZ92wh6BjA==

log            : tty

sasl log       : tty

database dir   : /var/lib/rabbitmq/mnesia/rabbit@my-rabbit

## 添加用户和vhost 的基本命令

sudo rabbitmqctl add_user myuser mypassword

sudo rabbitmqctl add_vhost myvhost

sudo rabbitmqctl set_user_tags myuser mytag

sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
