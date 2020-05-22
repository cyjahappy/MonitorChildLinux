from rest_framework import serializers
from .models import ServerInfo, PingResults, HTMLTestResults, iPerfTestResults, ServerInfoThreshold, ServerList


class ServerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerInfo
        fields = ('date', 'cpu', 'memory', 'disk', 'network', 'network_recv', 'network_sent')


class PingResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PingResults
        fields = ('server_ip', 'result')


class HTMLTestResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HTMLTestResults
        fields = (
            'url_id', 'dns_query', 'tcp_connection', 'request', 'dom_parse', 'blank_screen', 'onload', 'dom_ready',
            'date')


class iPerfTestResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = iPerfTestResults
        fields = ('server_ip', 'sent_Mbps', 'received_Mbps', 'retransmits', 'tcp_mss_default')


class ServerInfoThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerInfoThreshold
        fields = (
            'cpu_threshold', 'memory_threshold', 'disk_threshold', 'bandwidth_threshold', 'HTML_open_time_threshold',
            'tcp_sent_Mbps_threshold', 'tcp_received_Mbps_threshold', 'microservices_exec_time_threshold',
            'backend_management_system_open_time_threshold', 'ping_threshold')


class ServerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerList
        fields = ('server_ip', 'server_name')
