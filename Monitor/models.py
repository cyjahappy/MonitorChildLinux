from django.db import models


# 存储系统各项指标的数据
class ServerInfo(models.Model):
    date = models.DateTimeField(primary_key=True, auto_now=True)
    cpu = models.FloatField(null=True)
    memory = models.FloatField(null=True)
    disk = models.FloatField(null=True)
    network = models.FloatField(null=True)
    network_recv = models.FloatField(null=True)
    network_sent = models.FloatField(null=True)


# 存储除本机以外所有CRM服务器的IP地址
class ServerList(models.Model):
    server_ip = models.GenericIPAddressField(primary_key=True)
    server_name = models.CharField(default='Child Server', max_length=20)


# 存储Ping的结果
class PingResults(models.Model):
    id = models.AutoField(primary_key=True)
    server_ip = models.ForeignKey(ServerList, on_delete=models.CASCADE)
    result = models.FloatField(null=True)
    date = models.DateTimeField(auto_now=True, null=True)


# 存储对CRM服务器的iPerf测试的结果
class iPerfTestResults(models.Model):
    id = models.AutoField(primary_key=True)
    server_ip = models.ForeignKey(ServerList, on_delete=models.CASCADE)
    sent_Mbps = models.FloatField(null=True)
    received_Mbps = models.FloatField(null=True)
    retransmits = models.FloatField(null=True)
    tcp_mss_default = models.FloatField(null=True)
    error = models.CharField(null=True, max_length=30)
    date = models.DateTimeField(auto_now=True, null=True)


# 存储需要检测H5访问时长的网址列表
class HTMLTestList(models.Model):
    url = models.URLField(primary_key=True)
    url_name = models.CharField(null=True, max_length=20)


# 存储检测H5访问时长的结果
class HTMLTestResults(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.ForeignKey(HTMLTestList, on_delete=models.CASCADE)
    dns_query = models.FloatField(null=True)
    tcp_connection = models.FloatField(null=True)
    request = models.FloatField(null=True)
    dom_parse = models.FloatField(null=True)
    blank_screen = models.FloatField(null=True)
    onload = models.FloatField(null=True)
    dom_ready = models.FloatField(null=True)
    date = models.DateTimeField(auto_now=True)


# 存储系统各项阈值的数据
class ServerInfoThreshold(models.Model):
    id = models.AutoField(primary_key=True)
    cpu_threshold = models.FloatField()
    memory_threshold = models.FloatField()
    disk_threshold = models.FloatField()
    bandwidth_threshold = models.FloatField()
    ping_threshold = models.FloatField(default=1)
    HTML_open_time_threshold = models.FloatField()
    backend_management_system_open_time_threshold = models.FloatField()
    microservices_exec_time_threshold = models.FloatField()
    tcp_sent_Mbps_threshold = models.FloatField()
    tcp_received_Mbps_threshold = models.FloatField()


# 存储主服务器的IP地址
class MainServerIP(models.Model):
    id = models.AutoField(primary_key=True)
    server_ip = models.GenericIPAddressField()
