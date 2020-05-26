from django.urls import path
from Monitor import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

urlpatterns = [
    path('monitor/server-info-api', views.ServerInfoList.as_view()),
    path('monitor/server-info-to-db', views.ServerInfo_to_Database.as_view()),
    path('monitor/ping-results-api', views.PingResult.as_view()),
    path('monitor/ping-results-to-db', views.PingResults_to_Database.as_view()),
    path('monitor/ping-results-minutes', views.DisplayPingTestResults.as_view()),
    path('monitor/html-performance-test-result-api', views.HTMLPerformanceTestResult.as_view()),
    path('monitor/html-performance-test-results-to-db', views.HTMLTestResults_to_Database.as_view()),
    path('monitor/iperf3-test-results-to-db', views.iPerfResults_to_Database.as_view()),
    path('monitor/iperf3-test-result-api', views.iPerfResults.as_view()),
    path('monitor/server-info-threshold-api', views.ServerInfoThresholdList.as_view()),
    path('monitor/server-info-threshold-update', views.ServerInfoThresholdUpdate.as_view()),
    path('monitor/clean-database-api', views.CleanDatabase.as_view()),
    path('monitor/server-info-minutes', views.DisplayServerInfo.as_view()),
    path('monitor/html-performance-test-results-minutes', views.DisplayHTMLPerformanceTestResults.as_view()),
    path('monitor/iperf-test-results-minutes', views.DisplayIPerfTestResults.as_view()),
    path('monitor/target-server-list', views.TargetServerList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
