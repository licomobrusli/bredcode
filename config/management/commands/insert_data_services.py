from django.core.management.base import BaseCommand
from config.models import Services, ServiceCategory

class Command(BaseCommand):
    help = 'Load a list of services into the database'

    def handle(self, *args, **kwargs):
        services_data = [
            ('CP1', 'CRT', 'CORTE DE PELO', 'CORTE MODERNO O CLASICO', 30, 10, 'fake\\image\\path\\1'),
            ('BB1', 'OTR', 'BARBA', 'PERFILADO A NAVAJA/MAQUINA/TIJERA', 15, 6, 'fake\\image\\path\\2'),
            ('CJ1', 'OTR', 'CEJAS', 'ESTILISMO DE CEJAS A NAVAJA', 6, 4, 'fake\\image\\path\\3'),
            ('TP1', 'TNT', 'TINTE COMPLETO', 'DECOLORACIÓN + COLOR A ELEGIR', 120, 40, 'fake\\image\\path\\4'),
            ('TM1', 'TNT', 'TINTE MECHAS', 'DECOLORACIÓN + COLOR A ELEGIR', 110, 30, 'fake\\image\\path\\5'),
            ('TB1', 'TNT', 'TINTE BARBA', 'DECOLORACIÓN + COLOR A ELEGIR', 110, 12, 'fake\\image\\path\\6'),
            ('TC1', 'TNT', 'TINTE CEJAS', 'DECOLORACIÓN + COLOR A ELEGIR', 20, 4, 'fake\\image\\path\\7'),
            ('CA1', 'TNT', 'COLOR ADICIONAL', 'APLICACIÓN DE 1 COLOR ADICIONAL', 20, 10, 'fake\\image\\path\\8'),
            ('CON', 'OTR', 'CERA NARIZ/OÍDO', 'DEPILACIÓN DE PELO DE CEJAS Y OIDO CON CERA', 4, 6, 'fake\\image\\path\\9'),
            ('DB1', 'DSN', 'DISEÑO BASICO', 'LINEA RECTA A NAVAJA + MAQUINA', 5, 1, 'fake\\image\\path\\10'),
            ('DE1', 'DSN', 'DISEÑO ESTÁNDAR', 'VARIAS LINEAS RECTAS A NAVAJA + MAQUINA', 10, 6, 'fake\\image\\path\\11'),
            ('DP1', 'DSN', 'DISEÑO PREMIUM', 'PERSONALIZADO A NAVAJA + MAQUINA', 20, 10, 'fake\\image\\path\\12'),
            ('ME1', 'OTR', 'MOGAN´S EXPRESS', 'LAVADO+CHAMPÚ+SECADO + PEINADO', 20, 7, 'fake\\image\\path\\13')
        ]

        for code, service_category_code, name, description, total_duration, price, image_path in services_data:
            service_category = ServiceCategory.objects.get(code=service_category_code)
            Services.objects.create(
                code=code,
                service_category=service_category,
                name=name,
                description=description,
                total_duration=total_duration,
                price=price,
                image_path=image_path,
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
