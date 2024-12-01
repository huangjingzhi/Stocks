from django.apps import AppConfig
import sqlite3

class StockConfig(AppConfig):
    name = 'stock'
    verbose_name = 'stock'
    def ready(self):
        pass