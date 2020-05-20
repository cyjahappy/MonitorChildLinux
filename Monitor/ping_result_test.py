from ping3 import ping
from .models import ServerList, PingResults


def get_ping_result(server_ip):
    """
    接收一个IP地址,返回ping的结果
    :param server_ip:
    :return ping_result:
    """

    # 以秒为单位返回ping的结果
    result = ping(server_ip)

    if not result:
        # 找不到服务器
        # 这一行放找不到服务器的报警函数
        print('host unknown (cannot resolve)')
        return
    elif result is None:
        # 超时
        # 这一行放ping超时的报警函数
        print('timed out (no reply)')
        return
    else:
        ping_result = {
            'server_ip': server_ip,
            'result': result
        }
        return ping_result


def ping_result_to_database():
    """
    从PingList中提取所有需要ping的IP, ping一遍之后将结果存储到数据库(给后端使用的)
    :return:
    """
    ip = ServerList.objects.all()
    total_ip = ip.count()
    i = 0
    while i < total_ip:
        ping_result = get_ping_result(ip[i].server_ip)
        if ping_result:
            PingResultsInstance = PingResults()
            PingResultsInstance.server_ip_id = ping_result['server_ip']
            PingResultsInstance.ping_result = round((ping_result['result']), 2)
            PingResultsInstance.save()
        i = i + 1
    return


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
