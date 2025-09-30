from django.core.management.base import BaseCommand
from housing.models import Contrato
from datetime import date
from django.db import models

class Command(BaseCommand):
    help = "Genera cargos mensuales de todos los contratos activos"

    def handle(self, *args, **options):
        hoy = date.today()
        periodo = date(hoy.year, hoy.month, 1)

        contratos = Contrato.objects.filter(
            is_active=True,
            start__lte=periodo
        ).filter(
            models.Q(end__isnull=True) | models.Q(end__gte=periodo)
        )

        total_generados = 0
        for contrato in contratos:
            cargo = contrato.generar_cargo_mensual(periodo)
            if cargo:
                total_generados += 1
                self.stdout.write(self.style.SUCCESS(
                    f"Cargo generado para contrato {contrato.pk} - Unidad {contrato.unidad.code}"
                ))

        self.stdout.write(self.style.SUCCESS(
            f"Total de cargos generados: {total_generados}"
        ))
