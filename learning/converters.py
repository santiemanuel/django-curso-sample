import datetime


class DateRangeConverter:
    # El patrón de regex para coincidir con dos fechas en formato 'YYYYMMDD-YYYYMMDD'.
    regex = "[0-9]{8}-[0-9]{8}"

    def to_python(self, value):
        # Separar las fechas por el guion bajo y convertirlas a objetos de fecha.
        start_date_str, end_date_str = value.split("-")
        start_date = datetime.datetime.strptime(start_date_str, "%Y%m%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y%m%d").date()
        return start_date, end_date

    def to_url(self, value):
        # Recibe una tupla con dos objetos de fecha y los convierte de nuevo a cadena.
        start_date, end_date = value
        return f'{start_date.strftime("%Y%m%d")}-{end_date.strftime("%Y%m%d")}'
