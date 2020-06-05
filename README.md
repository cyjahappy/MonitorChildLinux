# MonitorChildLinux
CRM服务器监控系统(子服务器端)

## API示例

### 获取子服务器当前系统各项指标信息
#### Request
- Method: **GET**
- URL: ```monitor/server-info-api```
- Headers： Content-Type:application/json

#### Response
- Body

```
{
    "cpu": 1.0,
    "memory": 40.52,
    "disk": 9.4,
    "network": 0.0,
    "network_recv": 383482123.0,
    "network_sent": 37618359.0
}
```

### 使子服务器自行检测系统各项指标,检查是否超过阈值, 并将检测结果存入子服务器数据库
#### Request
- Method: **GET**
- URL: ```/monitor/server-info-to-db```

### 使子服务器针对指定IP地址进行Ping操作, 并获取Ping结果
#### Request
- Method: **POST**
- URL: ```monitor/ping-results-api```
- Headers： Content-Type:application/json
- Body:

```
{
    "server_ip": "129.204.183.108"
}
```

### 获取该子服务器前十分钟系统各项指标检测的结果
#### Request
- Method: **GET**
- URL: ```/monitor/server-info-minutes```
- Headers： Content-Type:application/json

#### Response
- Body:

```
{
    "cpu":[1.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0],
    "memory":[49.89,49.89,49.89,49.89,49.89,49.89,49.89,49.89,49.89,49.89],
    "disk":[13.8,13.8,13.8,13.8,13.8,13.8,13.8,13.8,13.8,13.8],
    "network":[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
    "network_recv":[22378210424.0,22382711228.0,22387134029.0,22387377802.0,22391875957.0,22392142825.0,22396386350.0,
                    22401030296.0,22405639549.0,22410102115.0],
    "network_sent":[922139713268.0,922312819330.0,922485208963.0,922658390089.0,922832485908.0,923006174129.0,923180170098.0,
                    923354326663.0,923527690366.0,923701863219.0],
    "date":["09:34","09:35","09:36","09:37","09:38","09:39","09:40","09:41","09:42","09:43"]
}
```

#### Response
- Body:

```
{
    "server_ip":"129.204.183.108","result":0.2417
}
```

### 使该子服务器对其余所有子服务器进行Ping操作, 检查结果是否超过阈值, 并将检测结果存入子服务器数据库
#### Request
- Method: **GET**
- URL: ```/monitor/ping-results-to-db```

### 获取该子服务器对指定IP地址前10分钟Ping的结果和时间
#### Request
- Method: **POST**
- URL: ```/monitor/ping-results-minutes```
- Headers： Content-Type:application/json
- Body:

```
{
    "server_ip": "129.204.183.108"
}
```

#### Response
- Body:

```
{
    "result":[0.1584,0.1584,0.1584,0.1584,0.1584,0.1584,0.1584,0.1584,0.1584,0.1584],
    "date":["09:03","09:03","09:03","09:03","09:03","09:03","09:03","09:03","09:03","09:03"]
}
```

### 获取该子服务器对指定URL进行前端性能测试的结果
#### Request
- Method: **POST**
- URL: ```/monitor/html-performance-test-result-api```
- Headers： Content-Type:application/json
- Body:

```
{
    "url": "https://apple.com.cn"
}
```

#### Response 
- Body:

```
{
    "dns_query":0.008,
    "tcp_connection":0.015,
    "request":0.002,
    "dom_parse":0.479,
    "blank_screen":2.376,
    "onload":3.398,
    "dom_ready":2.899
}
```

### 获取该子服务器对指定URL前十分钟进行前端性能测试的结果
#### Request
- Method: **POST**
- URL: ```/monitor/html-performance-test-results-minutes```
- Headers： Content-Type:application/json
- Body:

```
{
    "url": "https://apple.com.cn"
}
```

#### Response
- Body:

```
{
    "dns_query":[0.01,0.008,0.002,0.013,0.001,0.002,0.001,0.003,0.018,0.001],
    "tcp_connection":[0.012,0.014,0.012,0.014,0.013,0.013,0.014,0.014,0.013,0.012],
    "request":[0.002,0.002,0.002,0.002,0.002,0.003,0.003,0.002,0.003,0.002],
    "dom_parse":[0.335,0.54,0.315,0.325,0.221,0.279,0.56,0.433,0.287,0.346],
    "blank_screen":[0.114,0.103,0.103,0.177,0.107,0.117,0.999,2.749,0.118,0.096],
    "dom_ready":[0.63,0.587,0.609,0.667,0.762,0.631,1.503,3.238,0.647,0.586],
    "onload":[0.999,1.143,0.956,1.023,0.998,0.941,2.085,3.695,0.967,0.969],
    "date":["09:05","09:07","09:08","09:12","09:13","09:14","09:15","09:18","09:19","09:21"]
}
```

### 使该子服务器对数据库中存储的所有需要进行测试的URL地址进行前端性能测试, 检测结果是否超过阈值, 并将结果存入数据库
#### Request
- Method: **GET**
- URL: ```/monitor/html-performance-test-results-to-db```

### 获取该子服务器对指定IP地址进行iPerf测试的结果
#### Request
- Method: **POST**
- URL: ```/monitor/iperf3-test-result-api```
- Headers： Content-Type:application/json
- Body:

```
{
    "server_ip": "129.204.183.108"
}
```

#### Response
- Body:

```
{
    "server_ip":"129.204.183.108",
    "sent_Mbps":4.65,
    "received_Mbps":4.19,
    "retransmits":0.0,
    "tcp_mss_default":1412.0
}
```

### 使该子服务器对其余所有子服务器进行iPerf测试, 检查结果是否超过阈值, 并将检测结果存入子服务器数据库
#### Request
- Method: **GET**
- URL: ```/monitor/iperf3-test-results-to-db```

### 获取该子服务器对指定IP地址前十分钟进行iPerf测试的结果
#### Request
- Method: **POST**
- URL: ```/monitor/iperf-test-results-minutes```
- Headers： Content-Type:application/json
- Body:

```
{
    "server_ip": "129.204.183.108",
}
```

#### Response
- Body:

```
{
    "sent_Mbps":[4.45,5.84,7.46,5.95,6.73,5.25,4.86,7.28,7.52,4.36],
    "received_Mbps":[3.99,5.23,6.68,5.34,6.04,4.75,4.4,6.53,6.79,3.97],
    "tcp_mss_default":[1412.0,1412.0,1412.0,1412.0,1412.0,1412.0,1412.0,1412.0,1412.0,1412.0],
    "retransmits":[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
    "date":["09:18","09:19","09:21","09:22","09:23","09:25","09:26","09:27","09:29","09:30"]
}
```

### 获取该子服务器数据库中的阈值
#### Request
- Method: **GET**
- URL: ```/monitor/server-info-threshold-api```
- Headers： Content-Type:application/json

#### Response
- Body:

```
{
    "cpu_threshold":87.0,
    "memory_threshold":99.0,
    "disk_threshold":98.0,
    "bandwidth_threshold":280.0,
    "HTML_open_time_threshold":88.0,
    "tcp_sent_Mbps_threshold":88.0,
    "tcp_received_Mbps_threshold":88.0,
    "microservices_exec_time_threshold":88.0,
    "backend_management_system_open_time_threshold":88.0,
    "ping_threshold":88.0
}
```

### 更新该子服务器数据库中的阈值
#### Request
- Method: **POST**
- URL: ```/monitor/server-info-threshold-update```
- Headers： Content-Type:application/json
- Body:

```
{
    "cpu_threshold":87.0,
    "memory_threshold":99.0,
    "disk_threshold":98.0,
    "bandwidth_threshold":280.0,
    "HTML_open_time_threshold":88.0,
    "tcp_sent_Mbps_threshold":88.0,
    "tcp_received_Mbps_threshold":88.0,
    "microservices_exec_time_threshold":88.0,
    "backend_management_system_open_time_threshold":88.0,
    "ping_threshold":88.0
}
```

### 清理该子服务器数据库中2天前当天的数据
#### Request
- Method: **GET**
- URL: ```/monitor/clean-database-api```

### 获取该子服务器数据库中存储的其他子服务器的IP地址列表
#### Request
- Method: **GET**
- URL: ```/monitor/target-server-list```
- Headers： Content-Type:application/json

#### Response
- Body:

```
[
    {
        "server_ip":"129.204.183.108",
        "server_name":"TencentCloud"
    },
    {
        "server_ip":"68.183.238.127",
        "server_name":"Singapore"
    }
]
```
## 部署(Ubuntu 18.04)

#### 创建一个用于运行CRM服务器监控系统子服务器端Django Web App的用户

1. 创建用户

```
# 以monitor为例
$ adduser monitor
```

2. 赋予用户sudo权限:
   
打开/etc/sudoers

```
$ sudo vim /etc/sudoers
```

追加一行:

```
monitor ALL=NOPASSWD: ALL
```

需要用wq!强制保存

3. 切换到用户

```
# 切换到用户monitor
$ su monitor
```

#### 创建独立的Python虚拟环境

1. 安装python3-pip, virtualenv和virtualenvwrapper

```
$ sudo apt install python3-pip
$ sudo -H pip3 install virtualenv virtualenvwrapper
```

2. 创建目录用来存放虚拟环境

```
$ mkdir $HOME/.virtualenvs
```

3. 打开~/.bashrc文件，并添加内容：

```
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source /usr/local/bin/virtualenvwrapper.sh
```
 
4. 重新加载配置

```
$ source ~/.bashrc
```

5. 创建用于运行CRM服务器监控系统子服务器端Django Web App的Python虚拟环境

```
$ mkvirtualenv MonitorChildLinux
```


```
# 相关命令:

# 切换到MonitorChildLinux环境
$ workon MonitorChildLinux

# 退出虚拟环境
$ deactivate
```

#### 安装服务端的iPerf3, 并配置开机启动

1. 安装iPerf3

```
$ sudo apt install iperf3
```

2. 配置Systemd

在/lib/systemd/system中创建文件iperf.service

```
sudo vim /lib/systemd/system/iperf.service
```

并在文件中加入以下内容

```
[Unit]
Description=iperf server
After=syslog.target network.target auditd.service

[Service]
ExecStart=/usr/bin/iperf3 -s

[Install]
WantedBy=multi-user.target
```

3. 运行以下指令

```
# 重载systemd daemon配置
$ sudo systemctl daemon-reload

# 配置iPerf3开机启动
$ sudo systemctl enable iperf.service

# 启动服务端iPerf3
$ sudo systemctl start iperf.service
```

#### 部署Django Web App项目文件

1. 从[Realse - CRM监控系统(子服务器端)](https://github.com/cyjahappy/MonitorChildLinux/releases)下载最新Django Web App项目文件

```
# 这里以v0.1-alpha为例
$ wget https://github.com/cyjahappy/MonitorChildLinux/archive/v0.1.2-alpha.tar.gz
```

2. 将下载的压缩文件解压在该用户的主目录(这里是/home/monitor)

```
# 以v0.1.2-alpha为例
$ tar -zxvf v0.1.2-alpha.tar.gz

# 将解压出来的文件夹重命名为MonitorChildLinux(必须与之前创建的虚拟环境的名字一样)
$ mv MonitorChildLinux-0.1.2-alpha MonitorChildLinux

# 最终项目文件的位置应该是/home/monitor/MonitorChildLinux
```

3. 安装依赖文件

```
# 进入项目文件的文件夹
$ cd /home/monitor/MonitorChildLinux

# 进入刚才创建的名为MonitorChildLinux的虚拟环境
$ workon MonitorChildLinux

# 根据requrirements.txt安装依赖文件
$ pip3 install -r requirements.txt
```

4. 将/home/monitor/MonitorChildLinux/MonitorChildLinux/settings.py文件中ALLOWED_HOSTS= ['...']这栏中添加该服务器本机的公网IP地址

```
# 本例中服务器IP地址为128.199.234.70
ALLOWED_HOSTS = ['128.199.234.70']
```

5. 退出虚拟环境

```
$ deactivate
```

#### 安装Chrome浏览器, 及Chrome的浏览器驱动

1. 从官网下载Google Chrome

```
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```

2. 安装Google Chrome

```
$ sudo apt install ./google-chrome-stable_current_amd64.deb

# 确认浏览器的版本
$ google-chrome --version
```

3. 从[ChromeDriver - WebDriver for Chrome](https://chromedriver.chromium.org/downloads)中找到对应Chrome版本的驱动, 并下载

```
# 下载(这里以版本号83.0.4103.39为例)
$ wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
```

4. 将下载的压缩包解压到项目Python虚拟环境的文件夹内中的bin中(这里是/home/monitor/.virtualenvs/MonitorChildLinux/bin/chromedriver)

#### 安装uWSGI, 并配置开机启动

1. 系统级的安装uWSGI(不可在虚拟环境中安装)

```
$ sudo -H pip3 install uwsgi

# 检查版本
$ uwsgi --verison 
```

2. 创建uWSGI的配置文件
    在/home/monitor/MonitorChildLinux文件夹中创建文件MonitorChildLinux_uwsgi.ini, 并写入以下内容:

```
# MonitorChildLinux_uwsgi.ini file
[uwsgi]

# Django-related settings
# Django Web App项目文件的目录路径 (绝对路径)
chdir           = /home/monitor/MonitorChildLinux
# Django的 wsgi 文件(不用更改)
module          = MonitorChildLinux.wsgi
# Python虚拟环境的路径 (绝对路径)
home            = /home/monitor/.virtualenvs/MonitorChildLinux

# process-related settings
# master
master          = true
# 规定运行Django Web App的容器的最大进程数
processes       = 10
# 指向生成的Unix Socket路径(之后给Nginx调用)(绝对路径)
socket          = /home/monitor/MonitorChildLinux/MonitorChildLinux.sock
# 设置Unix Socket的读写权限
chmod-socket    = 777
# clear environment on exit
vacuum          = true
```

其中chmod-socket    = 777, 是为了使 Nginx 可以调用 uWSGI (以root权限运行的)构建的 Unix socket (所有者和用户组都是root)的同时, Nginx可以不以root的身份运行. 

3. 配置Emperor模式的uWSGI

```
# 为 vassals 创建一个文件夹
$ sudo mkdir /etc/uwsgi
$ sudo mkdir /etc/uwsgi/vassals

# 将刚才创建的uWSGI配置文件链接到/etc/uwsgi/vassals/
$ sudo ln -s /home/monitor/MonitorChildLinux/MonitorChildLinux_uwsgi.ini /etc/uwsgi/vassals/
```

4. 配置emperor.uwsgi.service
    在/lib/systemd/system中创建emperor.uwsgi.service, 并写入以下内容:

```
[Unit]
Description=uWSGI Emperor
After=syslog.target

[Service]
ExecStart=/usr/local/bin/uwsgi --ini /etc/uwsgi/emperor.ini
# Requires systemd version 211 or newer
RuntimeDirectory=uwsgi
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

5. 在/etc/uwsgi中创建文件emperor.ini, 并写入以下内容:

```
[uwsgi]
emperor = /etc/uwsgi/vassals
uid = root
gid = root
```

其中将uWSGI的进程用户和用户组设置为root. 因为Python中构建raw socket需要root权限(实现PING检测需要构建ICMP报文, 构建ICMP报文需要构建raw socket).

6. 运行以下指令

```
# 重载systemd daemon配置
$ sudo systemctl daemon-reload

# 配置uWSGI开机启动
$ sudo systemctl enable emperor.uwsgi.service

# 启动uWSGI
$ sudo systemctl start emperor.uwsgi.service
```

#### 配置Nginx

1. 在/etc/nginx/sites-enabled中创建文件MonitorChildLinux_nginx.conf, 并写入以下内容:

```
# MonitorChildLinux_nginx.conf

upstream django {
    server unix:///home/monitor/MonitorChildLinux/MonitorChildLinux.sock; # 指向项目目录中的Unix socket(运行uWSGI后会自动生成)
}

# configuration of the server
server {
    # the port your site will be served on
    listen      80;
    # the domain name it will serve for
    server_name 157.245.176.143; # 将server_name后面的IP地址换为该服务器本机的IP地址
    charset     utf-8;

    client_max_body_size 75M;   # adjust to taste

    location / {
        uwsgi_pass  django;
        include     /home/monitor/MonitorChildLinux/uwsgi_params; # 指向uwsgi_params
    }
}
```

2. 从[nginx/uwsgi_params](https://github.com/nginx/nginx/blob/master/conf/uwsgi_params)下载Nginx的uwsgi_params文件到Django Web App项目目录中(/home/monitor/MonitorChildLinux/uwsgi_params)

```
$ wget https://raw.githubusercontent.com/nginx/nginx/master/conf/uwsgi_params
```

4. 重启Nginx

```
$ systemctl restart nginx
```

