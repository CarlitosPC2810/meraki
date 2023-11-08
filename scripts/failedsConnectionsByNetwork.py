import sys
import logging
import requests
import time
import os

sys.path.insert(0,'/opt/cpcarriz/merakipruebas')
import querysMongoDB

arrayDefinitvo = [];
con = 1;
respuesta = "";
cont = 0;

#print(querysMongoDB)

def repetirFuncion():
    try:
        time.sleep(30)
        params1= {
        'message': '# API MERAKI BY PYTHON INICIO #'
        }
        envioDeNotificaciones(params1)
        querysMongoDB.saveFailedConnectionByNetwork()
        
        params2 = {
        'message': '# API MERAKI BY PYTHON TERMINO #'
        }

        envioDeNotificaciones(params2)

        return {
            'error': 'false',
            'message': 'Exito'
        }
    
    except Exception as e:
        print('# FALLO API MERAKI#',e)
        return {
            'error': 'true',
            'message': 'Error al generar apis'
        } 

def envioDeNotificaciones(params): 
    response = requests.post(url=url, params=params, headers=headers)
    json = response.json()
    print(json)

if __name__ == '__main__':
    url = 'http://10.237.5.158/api/failedProcessWarning'
    headers={   
            "apiid":"appempresarial",
            "apikey": "29ecb3db28a0f7d53497bb3b86bcd93ebb6710839083e28623b47a804d77d9b670ee7a2cd6a7bcaddc17dc15b02c0ef4e50e974b984eba40ff75a4e858f53583"
        }
    try:
        respuesta = repetirFuncion()
        print('respuesta' + str(respuesta['error']))
        while respuesta['error'] == 'true' and con < 6:
            params = {
            'message': '# API MERAKI INTENTO ' + str(con) +' #'
            }
            envioDeNotificaciones(params)
            respuesta = repetirFuncion()
            con = con +1
            
        print('respuesta', respuesta)

    except Exception as e:
        
        if cont < 1:
            time.sleep(30)
            params = {
            'message': '# APi MERAKI ULTIMO INTENTO CATCH #'
            }
            envioDeNotificaciones(params)
            respuesta2 = repetirFuncion()
            con = con +1

        params = {
        'message': '# ERROR API MERAKI BY PYTHON # \n' + str(e)
        }
        envioDeNotificaciones(params)
        print("Error", e)    
    

