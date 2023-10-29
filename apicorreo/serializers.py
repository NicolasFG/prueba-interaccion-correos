from rest_framework import serializers
from .models import *

class BlSerializer(serializers.ModelSerializer):
    class Meta:
        model = bl

        fields= ['id','nro_bl','puerto_de_carga','puerto_de_descarga','vessel','peso','no_voyage']