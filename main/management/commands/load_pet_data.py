from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from main.models import Mascota, Vacuna
from pytz import UTC


DATETIME_FORMAT = '%m/%d/%Y %H:%M'

NOMBRE_VACUNAS = [
    'Canine Parvo',
    'Canine Distemper',
    'Canine Rabies',
    'Canine Leptospira',
    'Feline Herpes Virus 1',
    'Feline Rabies',
    'Feline Leukemia'
]

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the mascota data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from mascota_data.csv into our mascota mode"

    def handle(self, *args, **options):
        if Vacuna.objects.exists() or Mascota.objects.exists():
            print('Datos de la mascota ya existen...')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Creando datos para las vacunas")

        for nombre_vacuna in NOMBRE_VACUNAS:
            vac = Vacuna(nombre=nombre_vacuna)
            vac.save()

        print("Cargando los datos de las mascotas disponibles para adopcion")
        for row in DictReader(open('./pet_data.csv')):
            mascota = Mascota()
            mascota.nombre = row['Pet']
            mascota.remitente = row['Submitter']
            mascota.especie = row['Species']
            mascota.raza = row['Breed']
            mascota.descripcion = row['Pet Description']
            mascota.sexo = row['Sex']
            mascota.edad = row['Age']
            raw_fecha_llegada = row['submission date']

            fecha_llegada = UTC.localize(
                datetime.strptime(raw_fecha_llegada, DATETIME_FORMAT))

            mascota.fecha_llegada = fecha_llegada
            mascota.save()

            raw_nombres_vacunas = row['vaccinations']

            nombres_vacunas = [nombre for nombre in raw_nombres_vacunas.split('| ') if nombre]

            for nombre_vacuna in nombres_vacunas:
                vac = Vacuna.objects.get(nombre=nombre_vacuna)
                mascota.vacunas.add(vac)
            mascota.save()
