from django.apps import AppConfig

from data.management.commands import start_task


class DataConfig(AppConfig):
    name = 'data'


from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'data'
    verbose_name = 'data'
    def ready(self):
        # 注册start_task和stop_task命令
        from data.management.commands import start_task, stop_task

