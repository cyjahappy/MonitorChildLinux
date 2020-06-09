# MonitorChildLinux
CRM服务器监控系统(子服务器端), 部署在CRM的Linux服务器上, 提供的功能包括: 监控CRM的Linux服务器健康程度，使用Selenium对指定网页进行前端性能测试，对指定服务器进行iPerf测试，对指定服务器进行Ping测试， 提供REST API用于命令服务器主机进行各种测试和获取测试的结果。测试完成之后会将测试结果与预先设置的阈 值进行比较，如果不达标，则会发邮件报警。

CRM服务器监控系统(子服务器端)在平时是完全静态的, 只有在有API被调用的时候才会运作起来, 不会占用过多的Linux服务器的计算资源. 由于本监控系统运行时不需要使用许多Django的内置功能, 故精简Django Admin后台系统, 静态资源, 模板, 消息框架等等内置功能, 这个Django Web框架中留下的功能基本是用于支持Django放出REST API的.

其中, 各个子服务器端中有一个SQLite数据库(使用Django内置的库驱动, 并不需要服务器安装额外的组件), 其中存储了各个CRM的Linux服务器的IP地址, 在进行iPerf测试和Ping测试的时候会对数据库中的每个IP都测试一遍. 数据库中还存储了各个测试的结果(有清理数据库的API, 母服务器端调用时则会清理过期的数据, 不会占用过多的存储空间). 

## 主要功能实现方式

### 网元层监控(检测服务器各项指标)

通过读取Linux服务器中的/proc, 来获取服务器中各项指标的值, 其中不同Linux发行版存放相应文件位置稍有不同, 因此使用Psutil库来进行取值, 可以很好的适配各个Linux的发行版. 

### 服务层监控(前端性能测试)

通过Selenium与Chrome结合进行前端性能的自动化测试. Selenium测试直接运行在Chrome浏览器中，模拟真正的用户浏览网页的操作, 并且 其中Chrome浏览器运行时使用Headless模式, 测试的同时会禁用GPU避免出错(大多数Linux服务器没有GPU). 本操作需要在Linux服务器中预先安装Chrome浏览器, 并安装对应该浏览器版本的Chrome驱动.

### 网络层监控(Ping测试)

使用Ping3库, 通过Python构造ICMP报文进行Ping测试. 其中Python构造ICMP报文中需要构造Raw Socket, Python构造Raw Socket必须具备root权限. 其中Django Web App是作为一个Web App在容器uWSGI中运行的, 因此想要成功进行Ping测试的话,uWSGI进程所属的用户只能是root. 这样并不会影响到服务器的安全性, Nginx通过调用uWSGI生成的Unix Socket与Django Web App, 其中Nginx并不需要以root权限运行.

### 网络层监控(iPerf测试)

子服务器之间能够相互进行iPerf测试, 以此测试服务器之间文件传输速度. 其中iPerf测试可选使用TCP模式测试, 或使用UDP测试. 使用TCP测试的话会引入TCP协议中的拥塞控制功能, 测试服务器在健康状态时相互之间的正常带宽. 使用UDP测试的话就没有拥塞控制功能, 会占用到其他所有正常TCP连接中的带宽, 并测试出两个服务器之间的极限带宽. 本测试的实现需要在每个服务器上以Systemd运行iPerf的服务端.

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
# 以cyj为例
$ adduser cyj
```

2. 赋予用户sudo权限:

    /etc/sudoers 追加一行(需要用强制保存)

```
cyj ALL=NOPASSWD: ALL
```

3. 切换到用户

```
# 切换到用户cyj
$ su cyj
```

#### 创建独立的Python虚拟环境

1. 安装virtualenv和virtualenvwrapper

```
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
export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv
source ~/.local/bin/virtualenvwrapper.sh
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

    在/lib/systemd/system中创建文件iperf.service, 并在文件中加入以下内容

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
$ wget https://github.com/cyjahappy/MonitorChildLinux/archive/v0.1-alpha.zip
```

2. 将下载的压缩文件解压在该用户的主目录(这里是/home/cyj)

```
# 以v0.1-alpha为例
$ unzip v0.1-alpha.zip

# 将解压出来的文件夹重命名为MonitorChildLinux(必须与之前创建的虚拟环境的名字一样)
$ mv MonitorChildLinux-0.1-alpha MonitorChildLinux

# 最终项目文件的位置应该是/home/cyj/MonitorChildLinux
```

3. 安装依赖文件

```
# 进入项目文件的文件夹
$ cd /home/cyj/MonitorChildLinux

# 进入刚才创建的名为MonitorChildLinux的虚拟环境
$ workon MonitorChildLinux

# 根据requrirements.txt安装依赖文件
$ pip3 install -r requirements.txt
```

4. 将/home/cyj/MonitorChildLinux/MonitorChildLinux/settings.py文件中ALLOWED_HOSTS= ['...']这栏中添加该服务器本机的公网IP地址

```
# 本例中服务器IP地址为157.245.176.143
ALLOWED_HOSTS = ['157.245.176.143']
```

5. 将/home/cyj/MonitorChildLinux/db.sqlite3中Monitor_serverlist表中加入所有子服务器的IP地址

6. 退出虚拟环境

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

4. 将下载的压缩包解压到项目Python虚拟环境的文件夹内中的bin中(这里是/home/cyj/.virtualenvs/MonitorChildLinux/bin/chromedriver)

#### 安装uWSGI, 并配置开机启动

1. 系统级的安装uWSGI(不可在虚拟环境中安装)

```
$ sudo -H pip3 install uwsgi

# 检查版本
$ uwsgi --verison 
```

2. 创建uWSGI的配置文件
    在/home/cyj/MonitorChildLinux文件夹中创建文件MonitorChildLinux_uwsgi.ini, 并写入以下内容:

```
# MonitorChildLinux_uwsgi.ini file
[uwsgi]

# Django-related settings
# Django Web App项目文件的目录路径 (绝对路径)
chdir           = /home/cyj/MonitorChildLinux
# Django的 wsgi 文件(不用更改)
module          = MonitorChildLinux.wsgi
# Python虚拟环境的路径 (绝对路径)
home            = /home/cyj/.virtualenvs/MonitorChildLinux

# process-related settings
# master
master          = true
# 规定运行Django Web App的容器的最大进程数
processes       = 10
# 指向生成的Unix Socket路径(之后给Nginx调用)(绝对路径)
socket          = /home/cyj/MonitorChildLinux/MonitorChildLinux.sock
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
$ sudo ln -s /home/cyj/MonitorChildLinux/MonitorChildLinux_uwsgi.ini /etc/uwsgi/vassals/
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
    server unix:///home/cyj/MonitorChildLinux/MonitorChildLinux.sock; # 指向项目目录中的Unix socket(运行uWSGI后会自动生成)
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
        include     /home/cyj/MonitorChildLinux/uwsgi_params; # 指向uwsgi_params
    }
}
```

2. 从[nginx/uwsgi_params](https://github.com/nginx/nginx/blob/master/conf/uwsgi_params)下载Nginx的uwsgi_params文件到Django Web App项目目录中(/home/cyj/MonitorChildLinux/uwsgi_params)

```
$ wget https://raw.githubusercontent.com/nginx/nginx/master/conf/uwsgi_params
```

4. 重启Nginx

```
$ systemctl restart nginx
```

