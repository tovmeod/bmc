import csv

from django.core.management.base import BaseCommand

from bmcapp.models import Passenger


class Command(BaseCommand):
    help = 'Import data from a CSV file using the API'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The name of the CSV file to import')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        self.import_data(csv_file)

    def import_data(self, csv_file):
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row['Age']:
                    del row['Age']
                Passenger.objects.create(**row)
