import requests, json
from .models import ServerInfoThreshold

# 部署的时候要改端口!!!!!!!
# 从数据库中获取各项指标阈值存在变量中, 避免每次检测阈值的时候都需要从数据库中取值
Threshold = ServerInfoThreshold.objects.get(id=1)
cpu_threshold = Threshold.cpu_threshold
memory_threshold = Threshold.memory_threshold
disk_threshold = Threshold.disk_threshold
bandwidth_threshold = Threshold.bandwidth_threshold
HTML_open_time_threshold = Threshold.HTML_open_time_threshold
backend_management_system_open_time_threshold = Threshold.backend_management_system_open_time_threshold
microservices_exec_time_threshold = Threshold.microservices_exec_time_threshold
tcp_sent_Mbps_threshold = Threshold.tcp_sent_Mbps_threshold
tcp_received_Mbps_threshold = Threshold.tcp_received_Mbps_threshold
ping_threshold = Threshold.ping_threshold


def server_info_check(server_info):
    """
    接收server_info的数据, 逐一检查是否超过阈值, 如果超过就报警
    :param server_info:
    """

    if (server_info['cpu'] > cpu_threshold) or (server_info['memory'] > memory_threshold) or (server_info[
            'disk'] > disk_threshold) or (server_info['network'] > bandwidth_threshold):
        requests.post('http://localhost:8000/server-info-alert', data=server_info)
    return


def iperf_check(iperf3_result):
    """
    接收iperf3_result的数据, 逐一检查是否小于阈值, 如果超过就返回True, 否则返回False
    :param iperf3_result:
    """

    if (iperf3_result['sent_Mbps'] < tcp_sent_Mbps_threshold) or (
            iperf3_result['received_Mbps'] < tcp_received_Mbps_threshold):
        return True
    return False


def iperf_alert(iperf3_alert_message_dict):
    """
    接收检测不达标的服务器信息, 并将列表内容传递给母服务器
    :param iperf3_alert_message_dict:
    """
    requests.post('http://localhost:8000/iperf-test-alert', data=iperf3_alert_message_dict)


def ping_check(ping_result):
    """
    接收ping_result数据, 检测延迟是否超过阈值, 如果超过就返回True, 否则返回False
    :param ping_result:
    """

    if ping_result['result'] > ping_threshold:
        print(ping_result['server_ip'])
        return True
    return False


def html_performance_check(html_performance_test_result):
    """
    接受html_performance_test_result数据, 检测整体页面打开时间是否超过阈值, 如果超过就返回True, 否则返回False
    :param html_performance_test_result:
    """

    if html_performance_test_result['onload'] > HTML_open_time_threshold:
        return True
    return False


def html_performance_alert(html_performance_problematic_url):
    """
    接收HTML性能检验中不达标的URL字典, 并将URL字典传递到母服务器
    :param html_performance_problematic_url:
    """
    requests.post('http://localhost:8000/html-performance-test-alert', data=html_performance_problematic_url)


def refresh_threshold():
    """
    数据库中的阈值更新后就调用这个函数, 将新的阈值存入变量中
    """
    global cpu_threshold
    global memory_threshold
    global disk_threshold
    global bandwidth_threshold
    global HTML_open_time_threshold
    global backend_management_system_open_time_threshold
    global microservices_exec_time_threshold
    global tcp_sent_Mbps_threshold
    global tcp_received_Mbps_threshold
    global ping_threshold

    Threshold = ServerInfoThreshold.objects.get(id=1)
    cpu_threshold = Threshold.cpu_threshold
    memory_threshold = Threshold.memory_threshold
    disk_threshold = Threshold.disk_threshold
    bandwidth_threshold = Threshold.bandwidth_threshold
    HTML_open_time_threshold = Threshold.HTML_open_time_threshold
    backend_management_system_open_time_threshold = Threshold.backend_management_system_open_time_threshold
    microservices_exec_time_threshold = Threshold.microservices_exec_time_threshold
    tcp_sent_Mbps_threshold = Threshold.tcp_sent_Mbps_threshold
    tcp_received_Mbps_threshold = Threshold.tcp_received_Mbps_threshold
    ping_threshold = Threshold.ping_threshold
