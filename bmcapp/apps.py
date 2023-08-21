import os

from django.apps import AppConfig
from django.core.management import call_command

from bmc.settings import DB_NAME


class BmcappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bmcapp'

    def ready(self):
        csv_path = os.getenv('USE_CSV')
        if csv_path is not None:
            if os.path.exists(DB_NAME):
                os.remove(DB_NAME)
            call_command('migrate')
            call_command('import', csv_path)
