# MonitorChildLinux
CRM服务器监控系统(子服务器端)

## 部署(Ubuntu 18.04)

#### 创建一个用于运行CRM服务器监控系统子服务器端Django Web App的用户

1. 创建用户

```
# 以cyj为例
adduser cyj
```

```
# 切换到用户cyj
su cyj
```

2. 赋予用户sudo权限:

    /etc/sudoers 追加一行(需要用强制保存)

```
cyj ALL=NOPASSWD: ALL
```

#### 创建独立的Python虚拟环境

1. 安装virtualenv和virtualenvwrapper

```
pip3 install virtualenv
pip3 install virtualenvwrapper
```

2. 创建目录用来存放虚拟环境

```
mkdir $HOME/.virtualenvs
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
source ~/.bashrc
```

5. 创建用于运行CRM服务器监控系统子服务器端Django Web App的Python虚拟环境

```
mkvirtualenv MonitorChildLinux
```

    相关命令:

```
# 切换到MonitorChildLinux环境
workon MonitorChildLinux

# 退出虚拟环境
deactivate
```

#### 服务端iPerf3
1. 安装iPerf3

```
sudo apt install iperf3
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

    运行以下指令

```
# 重载systemd daemon配置
sudo systemctl daemon-reload
# 配置iPerf3开机启动
sudo systemctl enable iperf.service
# 启动服务端iPerf3
sudo systemctl start iperf.service
```
