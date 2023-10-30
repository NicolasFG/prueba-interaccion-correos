import msal
import os
import requests
import shutil  # Para eliminar la carpeta y su contenido
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import io
import uuid


APP_ID = '98b67ff8-13ef-4b3c-8abd-c2a581f383ba'
SCOPES = ['Mail.ReadWrite']
GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

client_secret = 'dVR8Q~dbzRuaefNyVFgLQhIMRl4w6fPjaQ~2WcS0'
app_id = '98b67ff8-13ef-4b3c-8abd-c2a581f383ba'

def generate_access_token(tenant_id='658360c2-4aca-4b22-a0fa-7a5701fc3c26', 
                           app_id='98b67ff8-13ef-4b3c-8abd-c2a581f383ba', 
                           client_secret='dVR8Q~dbzRuaefNyVFgLQhIMRl4w6fPjaQ~2WcS0', 
                           scopes=["https://graph.microsoft.com/.default"]):
   
   
    authority = f"https://login.microsoftonline.com/{tenant_id}"


    client = msal.ConfidentialClientApplication(client_id=app_id,
                                               client_credential=client_secret,
                                               authority=authority)

    token_response = client.acquire_token_for_client(scopes=scopes)


    if "access_token" in token_response:
        return token_response['access_token']
    else:
        print(token_response.get("error"))
        print(token_response.get("error_description"))
        print(token_response.get("correlation_id"))


def download_email_attachments(user_id, message_id, headers):
    try:

        # Crear una carpeta llamada "files" si no existe
        if not os.path.exists('files'):
            os.makedirs('files')
        if not os.path.exists('new_files'):
            os.makedirs('new_files')

         # Obtener los detalles del mensaje
        message_response = requests.get(
            GRAPH_API_ENDPOINT + f'/users/{user_id}/messages/{message_id}',
            headers=headers
        )
        message_details = message_response.json()
        
        sender_email = message_details.get('sender', {}).get('emailAddress', {}).get('address', 'No disponible')
        sender_name = message_details.get('sender', {}).get('emailAddress', {}).get('name', 'No disponible')
        print(f"El correo fue enviado por: {sender_name} <{sender_email}>")

    
        response = requests.get(
            GRAPH_API_ENDPOINT + f'/users/{user_id}/messages/{message_id}/attachments',
            headers=headers
        )

        attachment_items = response.json()['value']

        for attachment in attachment_items:

            # Genera un UUID basado en el host ID y la hora actual
            unique_id = uuid.uuid1()
            print(unique_id)


            file_name = attachment['name']
            print(file_name)
            attachment_id = attachment['id']
            attachment_content = requests.get(

                GRAPH_API_ENDPOINT + f'/users/{user_id}/messages/{message_id}/attachments/{attachment_id}/$value',
                headers=headers
            )

            file_name_final = sender_email + str(unique_id) + "_" + file_name 

            file_name_final = os.path.join('files', file_name_final)
            with open(file_name_final, 'wb') as file:
                file.write(attachment_content.content)
                print(f'Saving file {file_name_final}...')
            
            print(attachment_content.status_code)

            file_name_final = sender_email + str(unique_id) + "_" + file_name 

            print('Saving file {0}...'.format(file_name_final))

           
        for file_name in os.listdir('files'):    
            if file_name.endswith('.pdf'):
                print("soy pdf")
                with open(os.path.join('files',file_name),mode='rb') as file_data:

                    file_bytes = file_data.read()
                    file_io = io.BytesIO(file_bytes)
                    
                    file_post = {'file': ('filename', file_io, 'application/pdf')}
                    responseOcr = requests.post(
                        url='http://127.0.0.1:5000/recognize-pdf',
                        files=file_post
                    )

                    # If the response contains JSON data
                    if responseOcr.headers['Content-Type'] == 'application/json':
                        json_response = responseOcr.json()
                        print(json_response)
                        
                    # If the response contains plain text
                    else:
                        text_response = responseOcr.text
                        print(text_response)

                    
                    print("Toca")
                    print(file_name)
                    # Dividir la cadena usando "_" como delimitador
                    partes = file_name.split("_")

                    print(partes)
                    #print()

                    # Reemplazar la parte después del "_" con "hola" y unir las partes
                    file_name_final_parseado = f"{partes[0]}_{json_response['type']}.pdf"

                    # Imprimir la cadena modificada
                    print(file_name_final_parseado)

                    file_name_final_parseado = os.path.join('new_files', file_name_final_parseado)
                    
                    with open(file_name_final_parseado, 'wb') as file:
                        file.write(attachment_content.content)
                        print(f'Saving file {file_name_final_parseado}...')

                    strong_conecction_string = 'DefaultEndpointsProtocol=https;AccountName=maerskstorage;AccountKey=t579Ae+Cbcja9ZzVteaXek2nDTWAYBmSihUDSTLaftjvfzkbnyPqIWEQxX6dtHFFdGBmRdgBMuh++AStBlNFzw==;EndpointSuffix=core.windows.net'

                    blob_service_client = BlobServiceClient.from_connection_string(strong_conecction_string)
                    blob_service_client

                    print("subiendo el archivo")
                    container_name = 'maersk-files-aduanas'
                   
                    blob_obj = blob_service_client.get_blob_client(container=container_name, blob=file_name_final_parseado)
                    print("subiendo blob")
                    with open(os.path.join(file_name_final_parseado),mode='rb') as file_data:
                        blob_obj.upload_blob(file_data)


        # Eliminar la carpeta "files" y su contenido
        shutil.rmtree('files')
        shutil.rmtree('new_files')

        print('Folder "files" and its contents have been deleted.')
           
        return True
    except Exception as e:
        print(e)
        return False

def funcion_final():

    access_token = generate_access_token(tenant_id='658360c2-4aca-4b22-a0fa-7a5701fc3c26',
                             app_id='98b67ff8-13ef-4b3c-8abd-c2a581f383ba',
                             client_secret='dVR8Q~dbzRuaefNyVFgLQhIMRl4w6fPjaQ~2WcS0',
                             scopes=["https://graph.microsoft.com/.default"])

    print(access_token)

    
    headers = {
    'Authorization': 'Bearer ' + access_token
    }

    """
    params = {
    'top': 3, # max is 1000 messages per request
    #'select': 'subject,hasAttachments',
    #'filter': 'hasAttachments eq true',
    'count': 'true'
    }
    """
    params = {
    '$top': 3, #Traer los ultimos top 3
    #'$orderby': 'receivedDateTime desc', #Ordenarlos por antiguedad de menor a mayor
    #'$filter': "startswith(subject, 'test2')", #Que tengan de titulo hola
    '$count': 'true'
    }
        
    response = requests.get(GRAPH_API_ENDPOINT + '/users/{c010175c-80a0-4ece-8770-28130260a619}/mailFolders/inbox/messages', headers=headers, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.json())

    response_json = response.json()
    response_json.keys()

    response_json['@odata.count']

    emails = response_json['value']

    for email in emails:
        if email['hasAttachments']:
            email_id = email['id']
            
            print("Pasando a la funcion de descarga")
            download_email_attachments(user_id='c010175c-80a0-4ece-8770-28130260a619',
                                    message_id=email_id,
                                    headers=headers)
            return "Descargo y envio a procesos los archivos corrrectamente"
        else:
            #print("No tiene ningun archivo adjunto")
            return "No tiene ningun archivo adjunto"

def listar_blobs_y_obtener_urls():
    try:

        container_name = 'maersk-files-aduanas'
        
        strong_conecction_string = 'DefaultEndpointsProtocol=https;AccountName=maerskstorage;AccountKey=t579Ae+Cbcja9ZzVteaXek2nDTWAYBmSihUDSTLaftjvfzkbnyPqIWEQxX6dtHFFdGBmRdgBMuh++AStBlNFzw==;EndpointSuffix=core.windows.net'

        blob_service_client = BlobServiceClient.from_connection_string(strong_conecction_string)
        blob_service_client

        # Obtener el cliente del contenedor
        container_client = blob_service_client.get_container_client(container_name)

        # Listar todos los blobs en el contenedor
        blob_list = container_client.list_blobs()
        
        # Recorrer la lista de blobs y obtener las URLs
        for blob in blob_list:
            blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob.name}"
            print(f"Blob URL: {blob_url}")
            return blob_url

    except Exception as e:
        print(f"Error: {e}")








