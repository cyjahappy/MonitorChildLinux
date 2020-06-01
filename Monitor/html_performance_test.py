import pytz
from datetime import datetime, timedelta
from selenium import webdriver
from .models import HTMLTestList, HTMLTestResults
from .threshold_check import html_performance_check, html_performance_alert
from selenium.webdriver.chrome.options import Options


def get_html_performance_test_result(url):
    """
    接收一个URL地址, 进行前端性能测试, 将结果以字典形式返回
    :param url:
    :return:
    """
    chrome_options = Options()
    # 设置Chrome以root权限运行
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    # 设置Chrome以无界面模式运行
    chrome_options.add_argument('--headless')
    # 服务器ubuntu上大多没有gpu，–disable-gpu以免报错
    chrome_options.add_argument('--disable-gpu')
    # 添加User-Agent避免网站检测到你使用的是无界模式进行反抓取
    chrome_options.add_argument(
        "user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'")
    # 使用Chrome浏览器来模拟测试环境
    # 部署不同服务器的时候需要根据实际情况修改路径!!!!!!!
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/home/cyj/.virtualenvs/MonitorChildLinux/bin/chromedriver')
    # 使用浏览器打开对应的URL
    driver.get(url)
    # pull window.performance.timing after loading the page and add information about url and number of run
    perf_timings = driver.execute_script("return window.performance.timing")
    # DNS查询耗时
    dns_query = (perf_timings['domainLookupEnd'] - perf_timings['domainLookupStart']) / 1000
    # TCP连接耗时
    tcp_connection = (perf_timings['connectEnd'] - perf_timings['connectStart']) / 1000
    # request请求耗时
    request = (perf_timings['responseEnd'] - perf_timings['responseStart']) / 1000
    # 解析dom树耗时
    dom_parse = (perf_timings['domComplete'] - perf_timings['domInteractive']) / 1000
    # 白屏时间
    blank_screen = (perf_timings['responseStart'] - perf_timings['navigationStart']) / 1000
    # dom ready时间
    dom_ready = (perf_timings['domContentLoadedEventEnd'] - perf_timings['navigationStart']) / 1000
    # 整体页面完全加载完毕的时间
    onload = (perf_timings['loadEventEnd'] - perf_timings['navigationStart']) / 1000
    # 关闭浏览器
    driver.quit()
    html_performance_test_result = {
        'url_id': url,
        'dns_query': dns_query,
        'tcp_connection': tcp_connection,
        'request': request,
        'dom_parse': dom_parse,
        'blank_screen': blank_screen,
        'dom_ready': dom_ready,
        'onload': onload
    }
    return html_performance_test_result


def html_performance_test_to_database():
    """
    从HTMLTestList中提取所有需要测试性能的URL地址, 都测试一遍一遍之后将结果存储到数据库
    :return:
    """

    # 声明一个列表用于存储检测中不达标的URL地址
    html_performance_problematic_url = []
    html_performance_problematic_result = []
    html_performance_problematic_results = []
    url = HTMLTestList.objects.all()
    total_url = url.count()
    i = 0
    while i < total_url:
        html_performance_test_result = get_html_performance_test_result(url[i].url)

        # 进行阈值检查, 并将存储阈值检测不达标的URL的信息
        if html_performance_check(html_performance_test_result) is True:
            html_performance_problematic_url.append(html_performance_test_result['url_id'])
            html_performance_problematic_result.append(html_performance_test_result['dns_query'])
            html_performance_problematic_result.append(html_performance_test_result['tcp_connection'])
            html_performance_problematic_result.append(html_performance_test_result['request'])
            html_performance_problematic_result.append(html_performance_test_result['dom_parse'])
            html_performance_problematic_result.append(html_performance_test_result['blank_screen'])
            html_performance_problematic_result.append(html_performance_test_result['dom_ready'])
            html_performance_problematic_result.append(html_performance_test_result['onload'])
            html_performance_problematic_results.append(html_performance_problematic_result)
            html_performance_problematic_result = []

        # 将结果存入数据库
        HTMLTestResults_instance = HTMLTestResults()
        HTMLTestResults_instance.url_id = html_performance_test_result['url_id']
        HTMLTestResults_instance.dns_query = html_performance_test_result['dns_query']
        HTMLTestResults_instance.tcp_connection = html_performance_test_result['tcp_connection']
        HTMLTestResults_instance.request = html_performance_test_result['request']
        HTMLTestResults_instance.dom_parse = html_performance_test_result['dom_parse']
        HTMLTestResults_instance.blank_screen = html_performance_test_result['blank_screen']
        HTMLTestResults_instance.dom_ready = html_performance_test_result['dom_ready']
        HTMLTestResults_instance.onload = html_performance_test_result['onload']
        HTMLTestResults_instance.save()
        i = i + 1

    # 如果html_performance_problematic_url不为空, 则调用警报函数
    if len(html_performance_problematic_url) > 0:
        html_performance_alert_message_dict = dict(
            zip(html_performance_problematic_url, html_performance_problematic_results))
        html_performance_alert(html_performance_alert_message_dict)
    return


# 定义在前端图表中一次性展示的数据量
number_of_data = 10
time_zone = pytz.timezone('Asia/Shanghai')


def get_database_html_performance_test_result_minutes(url):
    global number_of_data
    database_html_performance_test_result_minutes = {
        'dns_query': [],
        'tcp_connection': [],
        'request': [],
        'dom_parse': [],
        'blank_screen': [],
        'dom_ready': [],
        'onload': [],
        'date': []
    }
    HTMLTestResultsQuerySet = HTMLTestResults.objects.filter(url_id=url)
    QuerySetLength = HTMLTestResultsQuerySet.count()
    HTMLTestResultsData = HTMLTestResultsQuerySet[QuerySetLength - number_of_data:QuerySetLength]

    # 只有QuerySet不为空,才会进行取值
    if HTMLTestResultsData.exists():
        i = 0
        while i < number_of_data:
            database_html_performance_test_result_minutes['dns_query'].append(HTMLTestResultsData[i].dns_query)
            database_html_performance_test_result_minutes['tcp_connection'].append(
                HTMLTestResultsData[i].tcp_connection)
            database_html_performance_test_result_minutes['request'].append(HTMLTestResultsData[i].request)
            database_html_performance_test_result_minutes['dom_parse'].append(HTMLTestResultsData[i].dom_parse)
            database_html_performance_test_result_minutes['blank_screen'].append(HTMLTestResultsData[i].blank_screen)
            database_html_performance_test_result_minutes['dom_ready'].append(HTMLTestResultsData[i].dom_ready)
            database_html_performance_test_result_minutes['onload'].append(HTMLTestResultsData[i].onload)
            # 转换时区
            database_html_performance_test_result_minutes['date'].append(
                HTMLTestResultsData[i].date.astimezone(time_zone).strftime('%H:%M'))
            i = i + 1
    return database_html_performance_test_result_minutes


"""
# 以分钟为单位从数据库中取值
def get_database_html_performance_test_result_minutes(url):

    # 获取今天的日期
    now = datetime.now()
    database_html_performance_test_result_minutes = {
        'dns_query': [],
        'tcp_connection': [],
        'request': [],
        'dom_parse': [],
        'blank_screen': [],
        'dom_ready': [],
        'onload': [],
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
        HTMLTestResultsData = HTMLTestResults.objects.filter(date__year=date_to_get_data_year,
                                                             date__month=date_to_get_data_month,
                                                             date__day=date_to_get_data_day,
                                                             date__hour=date_to_get_data_hour,
                                                             date__minute=date_to_get_data_minute,
                                                             url_id=url)

        # 只有QuerySet不为空,才会进行取值
        if HTMLTestResultsData.exists():
            database_html_performance_test_result_minutes['dns_query'].append(HTMLTestResultsData[0].dns_query)
            database_html_performance_test_result_minutes['tcp_connection'].append(
                HTMLTestResultsData[0].tcp_connection)
            database_html_performance_test_result_minutes['request'].append(HTMLTestResultsData[0].request)
            database_html_performance_test_result_minutes['dom_parse'].append(HTMLTestResultsData[0].dom_parse)
            database_html_performance_test_result_minutes['blank_screen'].append(HTMLTestResultsData[0].blank_screen)
            database_html_performance_test_result_minutes['dom_ready'].append(HTMLTestResultsData[0].dom_ready)
            database_html_performance_test_result_minutes['onload'].append(HTMLTestResultsData[0].onload)
            # 转换时区
            database_html_performance_test_result_minutes['date'].append(
                HTMLTestResultsData[0].date.astimezone(time_zone).strftime('%H:%M'))

        i = i - 1
    return database_html_performance_test_result_minutes
"""
