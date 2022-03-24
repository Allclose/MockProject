#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading,time
import django
import os
sys.path.append("E:\Test\AppMock")
os.environ.setdefault("DJANGO_SETTINGS_MODULE","AppMock.settings")
django.setup()
from mitmproxy import http
from Myapp.models import *

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AppMock.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def monitor_thread():
    '轮询监控线程'
    while True:
        time.sleep(600)
        #监控抓包开关
        projects = DB_project.objects.all()
        for i in projects:
            if i.catch == True:
                time_cha = float(time.time())-float(i.catch_time)
                if time_cha > 10 :
                    i.catch = False
                    i.save()

if __name__ == '__main__':
    t = threading.Thread(target=monitor_thread)
    t.setDaemon(True)
    t.start()
    main()
