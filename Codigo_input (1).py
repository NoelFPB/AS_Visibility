import requests
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




# Example usage
ip_address1 = input("Ingrese la red 1: ")   #"45.195.207.0/24"  # Replace with the IP address you want to check
ip_address2 = input("Ingrese la red 2: ")   #"45.195.206.0/24"  # Replace with the IP address you want to check
red1 = get_percent_visibility(get_ip_visibility(ip_address1)) # Informacion de la red 1
if(ip_address2):red2 = get_percent_visibility(get_ip_visibility(ip_address2)) # Informacion de la red 2
headers_tabla= ['Nombre', 'Pais', 'Visibilidad'] # Encabezados generales
# Generando tabla 1
data_tabla1= [[name, red1[2][i], "{}%".format(round(red1[3][i]*100,2))] for i, name in enumerate(red1[1])]
tabla_header_data = [headers_tabla]+data_tabla1
tabla1= tabulate(tabla_header_data, headers="firstrow")
# Generando tabla 2
if(ip_address2):
    data_tabla2= [[name, red2[2][i], "{}%".format(round(red2[3][i]*100,2))] for i, name in enumerate(red2[1])]
    tabla_header_data = [headers_tabla]+data_tabla2
    tabla2= tabulate(tabla_header_data, headers="firstrow")
# Se generan los prints
print("\nRed {ip}, visbilidad: {vi}%".format(ip= ip_address1, vi=red1[0]))
if(ip_address2):print("Red {ip}, visbilidad: {vi}%".format(ip= ip_address2, vi=red2[0]))
print("\nPara la red 1:\n")
print(tabla1)
if(ip_address2):
    print("\nPara la red 2:\n")
    print(tabla2)
# Bloquea la finalizacion del programa
print("\nRed {ip}, visbilidad: {vi}%".format(ip= ip_address1, vi=red1[0]))
if(ip_address2):print("Red {ip}, visbilidad: {vi}%".format(ip= ip_address2, vi=red2[0]))
input("\nPresione enter para salir...")

    