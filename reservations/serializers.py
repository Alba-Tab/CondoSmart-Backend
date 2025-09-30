from rest_framework import serializers
from .models import AreaComun, Reserva, Suministro
from django.utils.timezone import now
class AreaComunSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaComun
        fields = "__all__"

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = "__all__"

    def validate(self, data):
        area = data.get("area")
        start = data.get("start")
        end = data.get("end")

        if start >= end or start < now():
            raise serializers.ValidationError("La fecha de inicio debe ser anterior a la de fin y mayor a ahora().")
        if not end:
            end = start
        if not start:
            start = end
            
        reserva_id = self.instance.id if self.instance else None

        qs = Reserva.objects.filter(area=area)
        if reserva_id:
            qs = qs.exclude(id=reserva_id)
        qs = qs.filter(
            start__lt=end,
            end__gt=start,
            status__in=["pendiente", "confirmada"]
        )
        if qs.exists():
            raise serializers.ValidationError("Ya existe una reserva que se superpone en el mismo periodo.")

        return data

class SuministroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suministro
        fields = "__all__"
