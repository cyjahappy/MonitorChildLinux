import pytz
from ping3 import ping
from .models import ServerList, PingResults
from .threshold_check import ping_check, ping_alert


def get_ping_result(server_ip):
    """
    接收一个IP地址,返回ping的结果
    :param server_ip:
    :return ping_result:
    """

    # 以秒为单位返回ping的结果
    result = ping(server_ip)
    ping_result = {
        'server_ip': server_ip,
        'result': ''
    }
    if result is False:
        # 找不到服务器
        ping_result['result'] = 'Host Cannot Resolve'
        return ping_result
    elif result is None:
        # 超时
        ping_result['result'] = 'Timed Out(no reply)'
        return ping_result
    else:
        ping_result['result'] = round(result, 4)
        return ping_result


def ping_result_to_database():
    """
    从PingList中提取所有需要ping的IP, ping一遍之后将结果存储到数据库(给后端使用的)
    :return:
    """
    # 声明一个列表用于存储检测中不达标的URL地址
    ping_problematic_server_ip = []
    ping_problematic_results = []
    ip = ServerList.objects.all()
    total_ip = ip.count()
    i = 0
    while i < total_ip:
        ping_result = get_ping_result(ip[i].server_ip)
        # 如果正确返回了ping的结果
        if type(ping_result['result']) is float:
            # 如果ping结果进行阈值检测后不符合标准, 就将目标服务器IP地址和结果传入列表
            if ping_check(ping_result) is True:
                ping_problematic_server_ip.append(ping_result['server_ip'])
                ping_problematic_results.append(ping_result['result'])
            # 将ping结果存储进数据库
            PingResultsObject = PingResults()
            PingResultsObject.server_ip_id = ping_result['server_ip']
            PingResultsObject.result = ping_result['result']
            PingResultsObject.save()
        # 如果目标服务器无法正确返回ping的结果, 将目标服务器和结果传入列表
        else:
            ping_problematic_server_ip.append(ping_result['server_ip'])
            ping_problematic_results.append(ping_result['result'])
            # 如无法正确返回结果, 则不将结果传入数据库
        i = i + 1

    # 如果ping_problematic_server_ip不为空, 则调用报警函数
    if len(ping_problematic_server_ip) > 0:
        ping_alert_message_dict = dict(
            zip(ping_problematic_server_ip, ping_problematic_results))
        ping_alert(ping_alert_message_dict)
    return


# 定义在前端图表中一次性展示的数据量
number_of_data = 10
time_zone = pytz.timezone('Asia/Shanghai')


def get_database_ping_test_result_minutes(server_ip):
    database_ping_test_result_minutes = {
        'result': [],
        'date': [],
    }
    PingResultsQuerySet = PingResults.objects.filter(server_ip_id=server_ip)
    QuerySetLength = PingResultsQuerySet.count()
    PingResultsData = PingResultsQuerySet[QuerySetLength - number_of_data:QuerySetLength]

    # 只有QuerySet不为空,才会进行取值
    if PingResultsData.exists():
        i = 0
        while i < number_of_data:
            database_ping_test_result_minutes['result'].append(PingResultsData[0].result)
            # 转换时区
            database_ping_test_result_minutes['date'].append(
                PingResultsData[0].date.astimezone(time_zone).strftime('%H:%M'))
            i = i + 1
    return database_ping_test_result_minutes


"""
# 以分钟为单位从数据库中取值
def get_database_ping_test_result_minutes(server_ip):

    # 获取今天的日期
    now = datetime.now()
    database_ping_test_result_minutes = {
        'result': [],
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
        PingResultsData = PingResults.objects.filter(date__year=date_to_get_data_year,
                                                               date__month=date_to_get_data_month,
                                                               date__day=date_to_get_data_day,
                                                               date__hour=date_to_get_data_hour,
                                                               date__minute=date_to_get_data_minute,
                                                               server_ip_id=server_ip)

        # 只有QuerySet不为空,才会进行取值
        if PingResultsData.exists():
            database_ping_test_result_minutes['result'].append(PingResultsData[0].result)
            # 转换时区
            database_ping_test_result_minutes['date'].append(
                PingResultsData[0].date.astimezone(time_zone).strftime('%H:%M'))

        i = i - 1

    return database_ping_test_result_minutes
"""

'''
# 从PingList中提取所有的需要ping的IP, ping一遍之后返回ping的结果的字典(给前端实时用表格展示结果使用的)
def get_ping_results():
    ip = PingList.objects.all()
    total_ip = ip.count()
    ping_results = {
        'server_name': [],
        'server_ip': [],
        'ping_result': []
    }
    i = 0
    while i < total_ip:
        ping_results['server_name'].append(ip[i].server_name)
        ping_results['server_ip'].append(ip[i].server_ip)
        ping_results['ping_result'].append(ping(ip[i].server_ip))
        i = i + 1
    return ping_results
'''
