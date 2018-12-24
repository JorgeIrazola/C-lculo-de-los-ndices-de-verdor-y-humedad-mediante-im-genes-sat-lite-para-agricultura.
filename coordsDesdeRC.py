import requests
from xml.etree import ElementTree as ET
import geojson
import json

# defino el namespace
ns = "{http://www.catastro.meh.es/}"

# se realiza la peticion al catastro (con y sin SRS)
r = requests.get('http://ovc.catastro.meh.es/ovcservweb/ovcswlocalizacionrc/ovccoordenadas.asmx/Consulta_CPMRC?Provincia=&Municipio=&SRS=&RC=26095A00601778')
# r = requests.get('http://ovc.catastro.meh.es/ovcservweb/ovcswlocalizacionrc/ovccoordenadas.asmx/Consulta_CPMRC?Provincia=&Municipio=&SRS=EPSG:4258&RC=26086A00301130')

# contenido del xml de la request     
r.content

# se parsea el xml a una variable
root = ET.fromstring(r.content)

# Se recorre el xml y se obtienen los valores de xcen e ycen
for c in root.find('{ns}coordenadas/{ns}coord/{ns}geo'.format(ns=ns)): 
    if c.tag.endswith("xcen"):
        xcen = c.text
    if c.tag.endswith("ycen"):
        ycen = c.text


# guardo las corrdenadas xcen e ycen para generar un geojson
coordenadas = geojson.Point((xcen,ycen))
coordenadas = geojson.Point((round(float(xcen),6),round(float(ycen),6)))

# genero el archivo geojson con las coordenadas
with open('mat.geojson', 'w') as outfile:
    json.dump(coordenadas, outfile)

