import apisMeraki
import mongo
#import pandas as pd
#import numpy as np
import json
import os
from datetime import datetime, timedelta
import pytz
import logging
from dotenv import load_dotenv



load_dotenv()
organization_id = os.getenv('ORGANIZATION_ID_BBVA')
zona_horaria = pytz.timezone('America/Guatemala')

fecha_hora_actual = datetime.now(zona_horaria)
print('fecha', fecha_hora_actual)
array_Definitivo = [];
fecha_hora_ajustada = fecha_hora_actual - timedelta(hours=1)
timestamp_t0 = fecha_hora_ajustada.timestamp()      
t0 = round(timestamp_t0)

timestamp_t1 = fecha_hora_actual.timestamp()
t1 = round(timestamp_t1)

#VAR CATALOGOS
equiposSM = [];
sitiosSM = [];

def saveFailedConnectionByNetwork(organization_id=organization_id, t0 = t0, t1 = t1): 
    contador = 0;
    myMongo = mongo.getDbMongo();
    db = myMongo['telmexApp']
    collection = db['rpaFailedsConnectionsMeraki']
    #print('collection', collection)
    #return 0;
    # CARGAR CATALOGOS 
    inv_equipos_sm = catalogoEquiposSM();
    inv_sitios = catalogoSitiosSM();

    networks = apisMeraki.getOrganizationNetworks(organization_id)
    
    totalRedes = len(networks)
    print(totalRedes)
    totalFaileds = 0;
    con = 0

    for network in networks:  
        
        totalFaileds = 0;
        print(network['id'])

        failedsConnection =  apisMeraki.getNetworkWirelessFailedConnections(network['id'], t0=t0, t1=t1)
        totalFaileds = len(failedsConnection);  
        print(totalFaileds)
         
        for failed in failedsConnection:
            contador = contador + 1
            print('contador=> ',contador)  

            parity_odd = lambda x: x['serial_no_'] == failed['serial']
            ap = next(filter(parity_odd, inv_equipos_sm), None)
            
            if ap != None:
                print('ap==========>', ap['name'])
                failed['location_code'] = ap['location_code']
                failed['company'] = ap["company"]
                failed['name'] = ap['name']
                failed['logical_name'] = ap['logical_name']
                failed['mac_ap'] = ap['mac']

                # VALIDAR QUE EXISTA FAILED CONNECTION
                if failed['location_code'] != None:
                    parity_odd = lambda x: x['LOCATION'] == failed['location_code']
                    sitio = next(filter(parity_odd, inv_sitios), None)
                    if sitio != None:
                        print('sitio==========>', sitio['STATE'])
                        failed['state'] = sitio['STATE']

            fecha_hora_obj = datetime.strptime(failed['ts'], "%Y-%m-%dT%H:%M:%S.%fZ")
            formato_deseado = "%Y-%m-%dT%H:%M:%S.%fZ"          
            fecha_hora_guatemala = fecha_hora_obj.replace(tzinfo=pytz.utc).astimezone(zona_horaria)
            fecha_hora_formateada = fecha_hora_guatemala.strftime(formato_deseado) 
            fecha_local = datetime.strptime(fecha_hora_formateada, formato_deseado)
            failed['fecha_local'] = fecha_local
            failed['fecha'] = fecha_hora_obj
            failed['network_id'] = network['id']
            failed['network_name'] = network['name']
        
        print('network->', network['id'], ' -------- totalFaileds', totalFaileds)    

        if totalFaileds != 0:
            array_Definitivo.extend(failedsConnection)
        con = con + 1;
    
    if con == totalRedes:   
        totaDefinitivo = len(array_Definitivo)
        print('totalDeDatos=>', totaDefinitivo)
        collection.insert_many(array_Definitivo)
        print('exito')
        return 'exito'
    else:
        print ('error')
        return 'error'
    
def saveApsByOrganization ():  
    myMongo = mongo.getDbMongo();
    db = myMongo['telmexApp']
    collection = db['aps_python_request']
    collection.delete_many({})
    getAps = apisMeraki.getOrganizationDevicesAvailabilities(organization_id=organization_id)
    collection.insert_many(getAps)
    
    return 'exito';


def catalogoEquiposSM():
    myMongo = mongo.getDbMongo();
    db = myMongo['telmexApp']
    collection = db['inv_equipos_sm']
    invEquiposSM = collection.find({'netcode': 'N000011', 'subtype':'ACCESS POINT', 'type':'NETWORKCOMP'})
        
    for equipo in invEquiposSM:
        equiposSM.append(equipo)
    
    if len(equiposSM) != 0:
        print("se logro inv_equipos_sm")
        return equiposSM;
    else:
        return "error"
    
def catalogoSitiosSM():
    myMongo = mongo.getDbMongo();
    db = myMongo['telmexApp']
    collection = db['inv_sitios']

    invSitios = collection.find({"NETWORK_CODE": 'N000011'})
    
    for sitio in invSitios:
        sitiosSM.append(sitio)
    
    if len(sitiosSM) != 0:
        print('se logro inv_sitios')
        return sitiosSM
    else:
        return "error"
    

#catalogoSitiosSM();