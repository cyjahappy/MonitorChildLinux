from .models import ServerInfo, PingResults, HTMLTestResults, iPerfTestResults


def clean_database():
    ServerInfo.objects.all().delete()
    PingResults.objects.all().delete()
    HTMLTestResults.objects.all().delete()
    iPerfTestResults.objects.all().delete()
    return
