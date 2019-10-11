import csv, os
from django.core.management import BaseCommand
from movies.models import Movie


class Command(BaseCommand):
    help = 'Imports IMDB csv data and creates all Movie model instances'

    def handle(self, *args, **options):
        project_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        with open(os.path.join(project_folder, 'imdb-data.csv')) \
                as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # skip header row

            for row in reader:
                try:
                    _, created = Movie.objects.get_or_create(
                        rank=reader.line_num-1,
                        id=row[1],
                        rating=row[2],
                        num_votes=row[3],
                        weighted_rating=row[4],
                        title=row[5],
                        year=row[6],
                        runtime=row[7],
                    )
                except Movie.DoesNotExist:
                    continue
