# -*- coding: utf-8 -*-
import psutil
import time
import pytz
from .models import ServerInfo
from .threshold_check import server_info_check
from datetime import datetime, timedelta


def get_server_info():
    """
    使用psutil库来获取系统的各项指标
    :return: 字典格式存储的server_info
    """
    # CPU使用率(%)
    cpu = psutil.cpu_percent(interval=1)
    # 内存总量(转换为GB)
    memory_total = psutil.virtual_memory().total / 1073741824
    # 已使用的内存(转换为GB)
    memory_used = round((psutil.virtual_memory().used / 1073741824), 2)
    # 内存使用率(%)
    memory = round((memory_used / memory_total) * 100, 2)
    # 磁盘使用率(%)(需要使用"df -h"命令 to list all mounted disk partitions, 然后选择对的那个来获取磁盘使用率)
    disk = psutil.disk_usage("/").percent

    # 获取现在的时间
    t0 = time.time()
    # 直到当前服务器网络已经上传的Bytes总和
    last_network_sent = psutil.net_io_counters().bytes_sent
    # 停一秒以便接下来获取这一秒的网络带宽信息
    time.sleep(1)
    # 一秒后, 直到当前服务器网络已经上传的Bytes
    network_sent = psutil.net_io_counters().bytes_sent
    # 获取一秒后的时间
    t1 = time.time()
    # 得到这一秒服务器上传的Mb总和(上行带宽!!)
    upstream_bandwidth = (network_sent - last_network_sent) / (t1 - t0)
    # 转成Mbps
    network = round(upstream_bandwidth / (1024*1024), 2)

    # 一秒后, 直到当前服务器网络已经下载的Bytes
    network_recv = psutil.net_io_counters().bytes_recv
    server_info = {'cpu': cpu,
                   'memory': memory,
                   'memory_used': memory_used,
                   'disk': disk,
                   'network': network,
                   'network_recv': network_recv,
                   'network_sent': network_sent,
                   }
    return server_info


def server_info_to_database():
    """
    将服务器各项指标的值传入ServerInfo表
    :return:
    """
    server_info = get_server_info()
    # 阈值检测
    server_info_check(server_info)
    # 将结果存入数据库中
    ServerInfoInstance = ServerInfo()
    ServerInfoInstance.cpu = server_info['cpu']
    ServerInfoInstance.memory = server_info['memory']
    ServerInfoInstance.disk = server_info['disk']
    ServerInfoInstance.network = server_info['network']
    ServerInfoInstance.network_recv = server_info['network_recv']
    ServerInfoInstance.network_sent = server_info['network_sent']
    ServerInfoInstance.save()
    return


# 定义在前端图表中一次性展示的数据量
number_of_data = 10
time_zone = pytz.timezone('Asia/Shanghai')


# 以分钟为单位从数据库中取值
def get_database_server_info_minutes():
    """
    以分钟为单位从数据库中取值
    :return: 存储前十分钟系统各项指标的字典
    """

    # 获取今天的日期
    now = datetime.now()
    database_server_info_minutes = {
        'cpu': [],
        'memory': [],
        'disk': [],
        'network': [],
        'network_recv': [],
        'network_sent': [],
        'date': []
    }
    i = number_of_data
    while i > 0:
        date_to_get_data = now - timedelta(minutes=i)
        # 逐个提取年月日
        date_to_get_data_year = (date_to_get_data.strftime('%Y'))
        date_to_get_data_month = (date_to_get_data.strftime('%m'))
        date_to_get_data_day = (date_to_get_data.strftime('%d'))
        date_to_get_data_hour = (date_to_get_data.strftime('%H'))
        date_to_get_data_minute = (date_to_get_data.strftime('%M'))
        # 获取这个时间点的QuerySet
        ServerInfoData = ServerInfo.objects.filter(date__year=date_to_get_data_year,
                                                   date__month=date_to_get_data_month,
                                                   date__day=date_to_get_data_day,
                                                   date__hour=date_to_get_data_hour,
                                                   date__minute=date_to_get_data_minute)

        # 只有QuerySet不为空,才会进行取值
        if ServerInfoData.exists():
            # ServerInfoData[0]从这个QuerySet中获取第一个值(避免像旧方法那样会取到重复值)
            database_server_info_minutes['cpu'].append(ServerInfoData[0].cpu)
            database_server_info_minutes['memory'].append(ServerInfoData[0].memory)
            database_server_info_minutes['disk'].append(ServerInfoData[0].disk)
            database_server_info_minutes['network'].append(ServerInfoData[0].network)
            database_server_info_minutes['network_recv'].append(ServerInfoData[0].network_recv)
            database_server_info_minutes['network_sent'].append(ServerInfoData[0].network_sent)
            # 转换时区
            database_server_info_minutes['date'].append(ServerInfoData[0].date.astimezone(time_zone).strftime('%H:%M'))

        i = i - 1
    return database_server_info_minutes
