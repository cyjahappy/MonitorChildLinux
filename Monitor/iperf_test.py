import iperf3
import pytz
from datetime import datetime, timedelta
from .models import ServerList, iPerfTestResults
from .threshold_check import iperf_check, iperf_alert


def iperf3_test(server_ip):
    """
    接受一个IP地址, 进行iPerf3测试,将测试结果以字典形式返回
    服务器上防火墙一定要开启iPerf3服务端的服务, 防火墙一定要开!!!
    :param server_ip:
    :return: iperf3_result
    """

    client = iperf3.Client()
    client.server_hostname = server_ip

    result = client.run()

    # 当无法与服务器通信时, 返回错误信息
    if result.error:
        iperf3_error_result = {
            "server_ip": server_ip,
            "error": result.error,
        }
        return iperf3_error_result

    # 正常进行测试, 返回测试结果
    else:
        # TCP重传的次数是0的话, 把None改成0, 便于传值
        if result.retransmits is None:
            result.retransmits = 0
        iperf3_result = {
            'server_ip': server_ip,
            'sent_Mbps': round(result.sent_Mbps, 2),
            'received_Mbps': round(result.received_Mbps, 2),
            'tcp_mss_default': round(result.tcp_mss_default, 2),
            'retransmits': result.retransmits,
        }
    return iperf3_result


def iperf3_result_to_database():
    """
    对ServerList中的IP地址逐个进行iPerf3测试, 将结果存入数据库, 并进行阈值检测报警.
    """

    # 声明一个列表用于存储检测中不达标的ip地址
    iperf3_problematic_server_ip = []
    iperf3_problematic_result = []
    iperf3_problematic_results = []

    ip = ServerList.objects.all()
    total_ip = ip.count()
    i = 0
    while i < total_ip:
        iperf3_result = iperf3_test(ip[i].server_ip)
        iPerfTestResultsInstance = iPerfTestResults()
        if 'error' in iperf3_result:
            iPerfTestResultsInstance.error = iperf3_result['error']
        else:
            # 进行阈值检测, 并将检测不达标的IP地址添加进列表尾部
            if iperf_check(iperf3_result) is True:
                iperf3_problematic_server_ip.append(iperf3_result['server_ip'])
                iperf3_problematic_result.append(iperf3_result['sent_Mbps'])
                iperf3_problematic_result.append(iperf3_result['received_Mbps'])
                iperf3_problematic_result.append(iperf3_result['tcp_mss_default'])
                iperf3_problematic_result.append(iperf3_result['retransmits'])
                iperf3_problematic_results.append(iperf3_problematic_result)
                iperf3_problematic_result = []

            iPerfTestResultsInstance.server_ip_id = iperf3_result['server_ip']
            iPerfTestResultsInstance.sent_Mbps = iperf3_result['sent_Mbps']
            iPerfTestResultsInstance.received_Mbps = iperf3_result['received_Mbps']
            iPerfTestResultsInstance.tcp_mss_default = iperf3_result['tcp_mss_default']
            iPerfTestResultsInstance.retransmits = iperf3_result['retransmits']
        iPerfTestResultsInstance.save()
        i = i + 1

    # 如果problematic_server_ip不为空, 则调用警报函数
    if len(iperf3_problematic_server_ip) > 0:
        iperf3_alert_message_dict = dict(zip(iperf3_problematic_server_ip, iperf3_problematic_results))
        iperf_alert(iperf3_alert_message_dict)
    return


# 定义在前端图表中一次性展示的数据量
number_of_data = 10
time_zone = pytz.timezone('Asia/Shanghai')


def get_database_iperf3_test_result_minutes(server_ip):
    database_iperf3_test_result_minutes = {
        'sent_Mbps': [],
        'received_Mbps': [],
        'tcp_mss_default': [],
        'retransmits': [],
        'date': [],
    }
    iPerfTestResultsQuerySet = iPerfTestResults.objects.filter(server_ip_id=server_ip)
    QuerySetLength = iPerfTestResultsQuerySet.count()
    iPerfTestResultsData = iPerfTestResultsQuerySet[QuerySetLength - number_of_data:QuerySetLength]

    # 只有QuerySet不为空,才会进行取值
    if iPerfTestResultsData.exists():
        i = 0
        while i < number_of_data:
            database_iperf3_test_result_minutes['sent_Mbps'].append(iPerfTestResultsData[i].sent_Mbps)
            database_iperf3_test_result_minutes['received_Mbps'].append(iPerfTestResultsData[i].received_Mbps)
            database_iperf3_test_result_minutes['tcp_mss_default'].append(iPerfTestResultsData[i].tcp_mss_default)
            database_iperf3_test_result_minutes['retransmits'].append(iPerfTestResultsData[i].retransmits)
            # 转换时区
            database_iperf3_test_result_minutes['date'].append(
                iPerfTestResultsData[i].date.astimezone(time_zone).strftime('%H:%M'))
            i = i + 1
    return database_iperf3_test_result_minutes


"""
# 以分钟为单位从数据库中取值
def get_database_iperf3_test_result_minutes(server_ip):

    # 获取今天的日期
    now = datetime.now()
    database_iperf3_test_result_minutes = {
        'sent_Mbps': [],
        'received_Mbps': [],
        'tcp_mss_default': [],
        'retransmits': [],
        'date': [],
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
        iPerfTestResultsData = iPerfTestResults.objects.filter(date__year=date_to_get_data_year,
                                                               date__month=date_to_get_data_month,
                                                               date__day=date_to_get_data_day,
                                                               date__hour=date_to_get_data_hour,
                                                               date__minute=date_to_get_data_minute,
                                                               server_ip_id=server_ip)

        # 只有QuerySet不为空,才会进行取值
        if iPerfTestResultsData.exists():
            database_iperf3_test_result_minutes['sent_Mbps'].append(iPerfTestResultsData[0].sent_Mbps)
            database_iperf3_test_result_minutes['received_Mbps'].append(iPerfTestResultsData[0].received_Mbps)
            database_iperf3_test_result_minutes['tcp_mss_default'].append(iPerfTestResultsData[0].tcp_mss_default)
            database_iperf3_test_result_minutes['retransmits'].append(iPerfTestResultsData[0].retransmits)
            # 转换时区
            database_iperf3_test_result_minutes['date'].append(
                iPerfTestResultsData[0].date.astimezone(time_zone).strftime('%H:%M'))

        i = i - 1

    return database_iperf3_test_result_minutes
"""
