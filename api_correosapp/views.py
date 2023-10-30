from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . models import *
from . functions import *

@api_view(['POST','GET'])

def registros(request):
    if request.method == 'GET':

        registro = bl.objects.all()
        reg_data = [{'id': reg.id, 'nro_bl': reg.nro_bl, 'puerto_de_carga': reg.puerto_de_carga, 'puerto_de_descarga': reg.puerto_de_descarga,'vessel': reg.vessel,'peso': reg.peso, 'no_voyage': reg.no_voyage} for reg in registro]
        
        """
        response_data = {
           'registros': reg_data,
        }
        """

        nro_orden = "2023-00-3017"
        cliente = "GRIARSA"

        #'fechaRecepcion':


        response_data = []

        for reg in registro:

            #debo sacar el id del registro y

            id_registro = reg.id

            valor = listar_blobs_y_obtener_urls()


            #Contruccion del response
            registro_dict = {
                'id': nro_orden,  
                'client': cliente,
                'creationDate': "25/10/2023",
                'documents': [
                    {
                        'data': [
                            {'name': 'Numero BL', 'value': reg.nro_bl},
                            {'name': 'puerto_de_carga', 'value': reg.puerto_de_carga},
                            {'name': 'puerto_de_descarga', 'value': reg.puerto_de_descarga},
                            {'name': 'vessel', 'value': reg.vessel},
                            {'name': 'peso', 'value': reg.peso},
                            {'name': 'no_voyage', 'value': reg.no_voyage}
                        ],                
                        'documentURL': 'C:\\Users\\USER\\Desktop\\Demo\\new_files\\rvidal@idegostd.com_BL.pdf',
                    }
                ]
            }

            response_data.append(registro_dict)

        return Response(response_data)
    
#Endpoint para manipulacion de correos
@api_view(['GET'])
def ObtenerToken(request):

    valor = funcion_final()

    print(valor)

    response_data = {
        'token': valor,
    }

    return Response(response_data)


#Endpoint para front
@api_view(['GET'])
def ObtenerUrls(request):

    valor = listar_blobs_y_obtener_urls()

    #print(valor)

    response_data = {
        'lista urls': valor,
    }

    return Response(response_data)




