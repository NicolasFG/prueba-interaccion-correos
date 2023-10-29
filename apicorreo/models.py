from django.db import models

# Create your models here.


class bl(models.Model):

    id = models.BigIntegerField(primary_key=True)
    nro_bl = models.CharField(max_length=255)
    puerto_de_carga = models.CharField(max_length=255)
    puerto_de_descarga = models.CharField(max_length=255)
    vessel = models.CharField(max_length=255)
    peso = models.CharField(max_length=255)
    no_voyage = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'bl'
