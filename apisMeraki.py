import meraki
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

APIKEY = os.getenv('MERAKI_DASHBOARD_API_KEY')
#print('APIKEY', APIKEY) 

dashboard = meraki.DashboardAPI(APIKEY, output_log=False)

def getNetworkHealthAlerts(network_id):
    response = dashboard.networks.getNetworkHealthAlerts(network_id)
    print('getNetworkHealthAlerts', response)
    return response

def getOrganizationDevicesAvailabilities(organization_id): 
    response = dashboard.organizations.getOrganizationDevicesStatuses(organization_id, total_pages='all')
    total = len(response)
    print('total_aps', total)
    return response;

def getNetworkWirelessLatencyHistory(network_id, t0, t1):
    response = dashboard.wireless.getNetworkWirelessLatencyHistory(networkId=network_id, t0=t0, t1=t1)    
    print(response)
    return response;

def getNetworkWirelessFailedConnections(network_id, t0, t1):
    response = dashboard.wireless.getNetworkWirelessFailedConnections(network_id, t0 = t0, t1= t1)
    #print(response)
    total = len(response)
    print('total', total)
    return response

def getOrganizationNetworks(organization_id):
    response = dashboard.organizations.getOrganizationNetworks(organization_id, total_pages='all')
    print('networks=>', response)
    return response

def getNetworkClients(network_id, t0, network_name):
    response = dashboard.networks.getNetworkClients(network_id, total_pages='all', perPage='1000', t0=t0)
    total = len(response)
    print('network=>', network_id, ' | ',network_name, '--> clientes=>', total);
    #return response

def getNetworkWirelessSsids(network_id):
    response = dashboard.wireless.getNetworkWirelessSsids(network_id)
    return response
#getOrganizationNetworks(605171199927910526)


