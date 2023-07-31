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
    - Nombre de l colector
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
        colector_visibility_percent.append((colector_peers_table_peers[i]-colector_peers_not_seeing[i])/(colector_peers_table_peers[i])) 
    # Obteniendo la visibilidad total de la red
    colector_number= len(colector_name)
    # Obteniendo la visibilidad total de la red
    ip_address_visibility_percent = round((sum(colector_visibility_percent)/colector_number)*100, 2)
    return [ip_address_visibility_percent, colector_name, colector_country, colector_visibility_percent]



def get_all_ip_visibility_for_AS():
    AS_number = "27773"  # replace with your AS number
    url = f"https://stat.ripe.net/data/bgp-state/data.json?resource=AS{AS_number}"
    response = requests.get(url)
    data = json.loads(response.text)


    # with open('response.json', 'r') as json_file:
    #     data = json.load(json_file)


    prefixes = set()  # a set to store unique prefixes

    for bgp_info in data['data']['bgp_state']:
        prefixes.add(bgp_info['target_prefix'])  # the 'path' field contains the announced networks

    as_info = {
        'AS_number': AS_number,
        'prefixes': {}
    }


    for prefix in prefixes:
        #ROA
        
        roa_url = f"https://stat.ripe.net/data/rpki-validation/data.json?resource={AS_number}&prefix={prefix}"
        roa_response = requests.get(roa_url)
        roa_data = json.loads(roa_response.text)

        #IRR
        irr_url = f"https://stat.ripe.net/data/prefix-routing-consistency/data.json?resource={prefix}"
        irr_response = requests.get(irr_url)
        irr_data = json.loads(irr_response.text)


        as_info['prefixes'][prefix] = {
            'ROA': roa_data,
            'IRR': irr_data
        }



    # Save to a JSON file
    # with open('as_info.json', 'r') as file:
    #     data = json.load(file)



    for key, values in as_info['prefixes'].items():
        print(key)
        #get_percent_visibility(get_ip_visibility(key))

        ip_address1 = key
        red1 = get_percent_visibility(get_ip_visibility('190.53.10.0/23'))
        headers_tabla= ['Nombre', 'País', 'Visibilidad'] # Encabezados generales
        # Generando tabla 1
        data_tabla1= [[name, red1[2][i], "{}%".format(round(red1[3][i]*100,2))] for i, name in enumerate(red1[1])]
        tabla_header_data = [headers_tabla]+data_tabla1
        tabla1= tabulate(tabla_header_data, headers="firstrow")
        # Se generan los prints
        print("\nRed {ip}, visbilidad: {vi}%".format(ip= ip_address1, vi=red1[0]))
        print("\nPara la red 1:\n")
        print(tabla1)

    