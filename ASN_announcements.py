import requests
import json
from tabulate import tabulate

def get_ip_visibility(ip_address):
    ''''
    Con esta funcion se obtiene el apartado de visibilities del query
    '''
    api_url = 'https://stat.ripe.net/data/visibility/data.json?resource={}'.format(ip_address)
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()  
        if "data" in data and "visibilities" in data["data"]:
            visibility = data["data"]["visibilities"]
            return visibility
        else: return None      
    else: return None

def get_percent_visibility(ip_address):
    '''
    Con esta función se recupera la informacion de:
    - Nombre del colector
    - Pais de donde se encuentra
    - La cantidad de peerings que no ven la red
    - La cantidad de peers que debieron verlo
    
    Como retorno se obtiene el porcentaje total de visibiliadad, nombre del
    colector, pais del colector y visibilidad por colector.
    '''
    colector_name =  []
    colector_country= []
    colector_peers_not_seeing = []
    colector_peers_table_peers = []
    colector_visibility_percent = []
    
    # Recuperando la informacion
    for i, peer in enumerate(ip_address):
        # Nombre del colector
        colector_name.append(peer["probe"]["name"])
        # Pais del colector
        colector_country.append(peer["probe"]["country"])
        # Peerings que no lo ven
        colector_peers_not_seeing.append(len(peer["ipv4_full_table_peers_not_seeing"]))
        # Cantidad de peerings que deben verlo
        colector_peers_table_peers.append(peer["ipv4_full_table_peer_count"])
        # Encontrando el porcentaje total de peerings que lo ven, por colector
        if colector_peers_table_peers[i] != 0:
            colector_visibility_percent.append((colector_peers_table_peers[i]-colector_peers_not_seeing[i])/(colector_peers_table_peers[i])) 
        else:
            print('Cero colector_peers_table_peers')
    # Obteniendo la visibilidad total de la red
    colector_number= len(colector_name)
    # Obteniendo la visibilidad total de la red
    ip_address_visibility_percent = round((sum(colector_visibility_percent)/colector_number)*100, 2)
    return [ip_address_visibility_percent, colector_name, colector_country, colector_visibility_percent]



def get_all_ip_visibility_for_AS(AS_number):
    prefixes = get_all_prefix_per_AS(AS_number)

    for prefix in prefixes:
    
        ip_address = prefix
        red1 = get_percent_visibility(get_ip_visibility(ip_address))
        headers_tabla= ['Nombre', 'País', 'Visibilidad'] # Encabezados generales
        # Generando tabla 1
        data_tabla1= [[name, red1[2][i], "{}%".format(round(red1[3][i]*100,2))] for i, name in enumerate(red1[1])]
        tabla_header_data = [headers_tabla]+data_tabla1
        tabla1= tabulate(tabla_header_data, headers="firstrow")
        # Se generan los prints
        print("\nRed {ip}, visbilidad: {vi}%".format(ip= ip_address, vi=red1[0]))
        print(tabla1)


def get_all_prefix_per_AS(AS_number):

    url = f"https://stat.ripe.net/data/bgp-state/data.json?resource=AS{AS_number}"
    response = requests.get(url)
    data = json.loads(response.text)
    # Archivos para probar sin hacer requests
    # with open('response.json', 'w') as json_file:
    #     json.dump(data, json_file, indent=4)
        
    # with open('response.json', 'r') as json_file:
    #     data = json.load(json_file)

    prefixes = set()  # a set to store unique prefixes
    # Prefixes son todos los prefijos que mira el AS
    for bgp_info in data['data']['bgp_state']:
        prefixes.add(bgp_info['target_prefix'])  # the 'path' field contains the announced networks
    
    return prefixes

def get_roa(prefix, AS_number):
    roa_url = f"https://stat.ripe.net/data/rpki-validation/data.json?resource={AS_number}&prefix={prefix}"
    roa_response = requests.get(roa_url)
    roa_data = json.loads(roa_response.text)
    #print(roa_data)
    return roa_data

def get_irr(prefix):
    #IRR
    irr_url = f"https://stat.ripe.net/data/prefix-routing-consistency/data.json?resource={prefix}"
    irr_response = requests.get(irr_url)
    irr_data = json.loads(irr_response.text)
    #print(irr_data)    
    return irr_data

def get_roa_irr_per_prefix(AS_number):

    prefixes = get_all_prefix_per_AS(AS_number)

    as_info = {
        'AS_number': AS_number,
        'prefixes': {}
    }

    for prefix in prefixes:
        roa_data = get_roa(prefix, AS_number)
        irr_data = get_irr(prefix)

        as_info['prefixes'][prefix] = {
            'ROA': roa_data,
            'IRR': irr_data
        }
    
    print(json.dumps(as_info, indent = 4))

    return as_info
 
get_all_ip_visibility_for_AS(AS_number = 27773)
#get_roa_irr_per_prefix(AS_number=27773)


