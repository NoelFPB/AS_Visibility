# AS_Visibility

Este script se conecta a la API de RIPE NCC para obtener información sobre visibilidad, ROA (Route Origin Authorization) e IRR (Internet Routing Registry) para direcciones IP y números de sistemas autónomos (AS).

Funciones:
get_ip_visibility(ip_address):

Entrada: Dirección IP.
Salida: Datos de visibilidad de la dirección IP.
Descripción: Conecta con la API para obtener datos de visibilidad para un prefijo IP específico.

get_percent_visibility(ip_address):

Entrada: Salida de la función get_ip_visibility. Es decir, datos de visibildiad de la dirección IP.
Salida: Lista con visibilidad total, nombres de los colectores, países de los colectores y porcentaje de visibilidad por colector.
Descripción: Calcula el porcentaje de visibilidad para un prefijo IP basándose en la función anterior.

get_all_ip_visibility_for_AS(AS_number):

Entrada: Número de sistema autónomo (AS).
Descripción: Para un número AS dado, recupera la visibilidad de todos los prefijos y genera una tabla con detalles.

get_all_prefix_per_AS(AS_number):

Entrada: Número de sistema autónomo (AS).
Salida: Conjunto de todos los prefijos pertenecientes a un número AS.
Descripción: Recopila todos los prefijos IP asociados con un número AS específico.

get_roa(prefix, AS_number):

Entrada: Prefijo IP, Número de sistema autónomo (AS).
Salida: Datos ROA del prefijo para el número AS especificado.
Descripción: Consulta la validación ROA para un prefijo y número AS específico.

get_irr(prefix):

Entrada: Prefijo IP.
Salida: Datos IRR del prefijo.
Descripción: Obtiene la consistencia del enrutamiento del prefijo desde el IRR.

get_roa_irr_per_prefix(AS_number):

Entrada: Número de sistema autónomo (AS).
Salida: Diccionario con detalles ROA e IRR para cada prefijo bajo el número AS especificado.
Descripción: Combina las funciones anteriores para proporcionar una visión completa de ROA e IRR para todos los prefijos bajo un número AS.
Uso:
Para obtener la visibilidad de todos los prefijos de un número AS específico:

get_all_ip_visibility_for_AS(AS_number = 27773)

Para obtener detalles ROA e IRR para todos los prefijos bajo un número AS:

get_roa_irr_per_prefix(AS_number=27773)

Este código es esencialmente una herramienta para aquellos interesados en la salud y el estado de los sistemas autónomos y sus prefijos IP en el Internet global. Al consultar datos desde RIPE NCC, este script proporciona información valiosa sobre cómo se ven estos prefijos desde diferentes puntos de vista en la web, así como su conformidad con prácticas recomendadas como ROA e IRR.
