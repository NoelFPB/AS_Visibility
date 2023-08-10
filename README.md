# Visibilidad de IPs y BGP Script

Este script se conecta a la API de RIPE NCC para obtener información sobre visibilidad, ROA (Route Origin Authorization) e IRR (Internet Routing Registry) para direcciones IP y números de sistemas autónomos (AS).

## 📜 Índice

- [Funciones](#-funciones)
- [Uso](#-uso)

## 🛠️ Funciones:

### 1. `get_ip_visibility(ip_address)`:
- **Entrada**: Dirección IP.
- **Salida**: Datos de visibilidad de la dirección IP.
- **Descripción**: Conecta con la API para obtener datos de visibilidad para un prefijo IP específico.

### 2. `get_percent_visibility(ip_address)`:
- **Entrada**: Salida de la función get_ip_visibility. Es decir datos de visibilidad de la dirección IP.
- **Salida**: Lista con visibilidad total, nombres de los colectores, países de los colectores y porcentaje de visibilidad por colector.
- **Descripción**: Calcula el porcentaje de visibilidad para un prefijo IP basándose en la data recolectada de la función anterior.

### 3. `get_all_ip_visibility_for_AS(AS_number)`:
- **Entrada**: Número de sistema autónomo (AS).
- **Descripción**: Para un número AS dado, recupera la visibilidad de todos los prefijos y genera una tabla con detalles.

### 4. `get_all_prefix_per_AS(AS_number)`:
- **Entrada**: Número de sistema autónomo (AS).
- **Salida**: Conjunto de todos los prefijos pertenecientes a un número AS.
- **Descripción**: Recopila todos los prefijos IP asociados con un número AS específico.

### 5. `get_roa(prefix, AS_number)`:
- **Entrada**: Prefijo IP, Número de sistema autónomo (AS).
- **Salida**: Datos ROA del prefijo para el número AS especificado.
- **Descripción**: Consulta la validación ROA para un prefijo y número AS específico.

### 6. `get_irr(prefix)`:
- **Entrada**: Prefijo IP.
- **Salida**: Datos IRR del prefijo.
- **Descripción**: Obtiene la consistencia del enrutamiento del prefijo desde el IRR.

### 7. `get_roa_irr_per_prefix(AS_number)`:
- **Entrada**: Número de sistema autónomo (AS).
- **Salida**: Diccionario con detalles ROA e IRR para cada prefijo bajo el número AS especificado.
- **Descripción**: Combina las funciones anteriores para proporcionar una visión completa de ROA e IRR para todos los prefijos bajo un número AS.

## 🔧 Uso:

1. Para obtener la visibilidad de todos los prefijos de un número AS específico:

```python
get_all_ip_visibility_for_AS(AS_number = 27773)
