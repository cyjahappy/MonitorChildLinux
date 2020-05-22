from .serializers import ServerInfoSerializer, PingResultsSerializer, iPerfTestResultsSerializer, \
    ServerInfoThresholdSerializer, HTMLTestResultsSerializer, ServerListSerializer
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .server_info_test import get_server_info, server_info_to_database, get_database_server_info_minutes
from .ping_result_test import ping_result_to_database, get_ping_result
from .html_performance_test import html_performance_test_to_database, get_html_performance_test_result, \
    get_database_html_performance_test_result_minutes
from .iperf_test import iperf3_result_to_database, iperf3_test, get_database_iperf3_test_result_minutes
from .models import ServerInfoThreshold, ServerList
from .threshold_check import refresh_threshold
from .clean_database import clean_database


class ServerInfo_to_Database(APIView):
    """
    将服务器各项指标数据存入ServerInfo表中
    """

    def get(self, request):
        try:
            server_info_to_database()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServerInfoList(APIView):
    """
    返回JSON格式的服务器各项指标数据
    """

    def get(self, request, format=None):
        serializer = ServerInfoSerializer(data=get_server_info())
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HTMLPerformanceTestResult(APIView):
    """
    接收一个URL, 进行前端性能测试, 并将测试结果以JSON形式返回

    只输入网址不行, 要加上http://或者https://,不然报错

    示例HTTP Request:
    POST http://localhost:8000/html-performance-test-result-api
    Content-Type: application/json

    {
      "url": "https://apple.com.cn"
    }
    """

    def post(self, request, format=None):
        url = request.data['url']
        result = get_html_performance_test_result(url)
        serializer = HTMLTestResultsSerializer(data=result)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HTMLTestResults_to_Database(APIView):
    """
    对HTMLTestList表中指定的URL进行前端性能测试, 并将测试结果存储在HTMLTestResults表中
    """

    def get(self, request):
        try:
            html_performance_test_to_database()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PingResults_to_Database(APIView):
    """
    对ServerList表中所有的IP依次进行ping测试, 并将测试结果存储在PingResult表中
    """

    def get(self, request, format=None):
        try:
            ping_result_to_database()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PingResult(APIView):
    """
    接收一个IP地址, ping之后将结果以JSON形式返回
    """

    def post(self, request, format=None):
        server_ip = request.data['server_ip']
        ping_result = get_ping_result(server_ip)
        serializer = PingResultsSerializer(data=ping_result)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class iPerfResults_to_Database(APIView):
    """
    对ServerList表中所有的IP依次执行iPerf测试, 并将测试结果存储在iPerfTestResults表中
    """

    def get(self, request, format=None):
        try:
            iperf3_result_to_database()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class iPerfResults(APIView):
    """
    接收一个IP地址, 进行iPerf测试, 并将测试结果以JSON形式返回

    示例HTTP Request:
    POST http://localhost:8000/iperf3-test-result-api
    Content-Type: application/json

    {"server_ip":  "129.204.183.108"}

    :return:
        {
          "server_ip": "129.204.183.108",
          "sent_Mbps": 4.37,
          "received_Mbps": 3.18,
          "retransmits": null,
          "tcp_mss_default": 8960.0
        }
    """

    def post(self, request, format=None):
        server_ip = request.data['server_ip']
        result = iperf3_test(server_ip)
        serializer = iPerfTestResultsSerializer(data=result)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServerInfoThresholdList(generics.ListAPIView):
    """
    定义GET操作,返回JSON格式的服务器各项指标阈值
    """
    queryset = ServerInfoThreshold.objects.all()
    serializer_class = ServerInfoThresholdSerializer


class TargetServerList(generics.ListAPIView):
    """
    定义GET操作,返回JSON格式的服务器各项指标阈值
    """
    queryset = ServerList.objects.all()
    serializer_class = ServerListSerializer


class ServerInfoThresholdUpdate(generics.UpdateAPIView):
    """
    定义PUT操作,更新服务期各项指标阈值

    示例HTTP Request:
    PUT http://localhost:8000/server-info-threshold-update/1/
    Content-Type: application/json

    {
      "cpu_threshold": "91",
      "memory_threshold": "91",
      "disk_threshold": "91",
      "bandwidth_threshold": "91",
      "HTML_open_time_threshold": "91",
      "tcp_sent_Mbps_threshold": "0",
      "tcp_received_Mbps_threshold": "0",
      "microservices_exec_time_threshold": "91",
      "backend_management_system_open_time_threshold": "91"
    }
    """
    queryset = ServerInfoThreshold.objects.all()
    serializer_class = ServerInfoThresholdSerializer

    # 调用函数使用数据表中的阈值信息刷新缓存的阈值
    refresh_threshold()


class CleanDatabase(APIView):
    """
    清理数据库中过期数据
    """

    def get(self, request):
        try:
            clean_database()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DisplayServerInfo(APIView):
    """
    以一定规则从ServerInfo表中提取数据, 并以JSON形式返回
    """

    def get(self, request):
        try:
            database_server_info_minutes = get_database_server_info_minutes()
            return Response(database_server_info_minutes, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DisplayHTMLPerformanceTestResults(APIView):
    """
    接收一个URL, 以一定规则从HTMLTestResults表中提取有关此URL的数据, 并以JSON形式返回

    示例HTTP Request:
    POST http://localhost:8001/html-performance-test-results-minutes
    Content-Type: application/json

    {"url": "https://apple.com.cn"}
    """

    def post(self, request):
        try:
            url = request.data['url']
            database_html_performance_test_result_minutes = get_database_html_performance_test_result_minutes(url)
            return Response(database_html_performance_test_result_minutes, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DisplayIPerfTestResults(APIView):
    """
    接收一个Server IP, 以一定规则从iPerfTestResults表中提取有关此Server IP的数据, 并以JSON形式返回
    """

    def post(self, request):
        try:
            server_ip = request.data['server_ip']
            database_iperf3_test_result_minutes = get_database_iperf3_test_result_minutes(server_ip)
            return Response(database_iperf3_test_result_minutes, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
