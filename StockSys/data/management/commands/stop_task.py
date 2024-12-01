import os
import signal
from django.core.management.base import BaseCommand
from django.apps import apps
class Command(BaseCommand):
    help = 'Stops the task started with start_task command'
    def handle(self, *args, **kwargs):
        for model in apps.get_models():
            self.stdout.write(" APP -> %s" % model)

