#Calculate NDVI for QGIS
# from QGIS import iface-> symbolic importation of iface object of QGIS
# import qgis

from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
import processing, os, ogr, csv, sys
from processing.core.Processing import Processing
from qgis.core import QgsRasterLayer, QgsApplication, QgsVectorFileWriter, QgsVectorLayer
from PyQt4.QtCore import QFileInfo

#import pandas as pd


qgis_prefix=r"C:\Program Files\QGIS 2.18\apps\qgis" # Indicamos donde esta el QGIS
QgsApplication.setPrefixPath(qgis_prefix, True) # Configuramos la aplicacion QGIS
app = QgsApplication([],True, None) # El True inhabilita la interfaz grafica
QgsApplication.initQgis() # Iniciamos la aplicacion QGIS


# Indice Diferencial de Vegetacion Normalizado
def NDVI (band4,band8,output):
    entries=[]
    #define raster 1 (band4)
    raster1 = QgsRasterCalculatorEntry()
    raster1.ref='band4@1'
    raster1.raster = band4
    raster1.bandNumber = 1
    entries.append(raster1)
    #define raster 2 (band8)
    raster2 = QgsRasterCalculatorEntry()
    raster2.ref = 'band8@1'
    raster2.raster = band8
    raster2.bandNumber = 1
    entries.append(raster2)
    #NDVI Procesado de las bandas
    # calc=QgsRasterCalculator('("band8@1"-"band4@1")/("band8@1"+"band4@1")',output,'GTiff',band8.extent(),band8.width(),band8.height(),entries)
    calc=QgsRasterCalculator('(("band8@1"-"band4@1")/("band8@1"+"band4@1"))*100',output,'GTiff',band8.extent(),band8.width(),band8.height(),entries)
    calc.processCalculation()
 
# Indice Diferencial de Agua Normalizado
def NDWI (band3,band8,output):
    entries=[]
    #define raster 1 (band8)
    raster1 = QgsRasterCalculatorEntry()
    raster1.ref='band8@1'
    raster1.raster = band8
    raster1.bandNumber = 1
    entries.append(raster1)
    #define raster 2 (band3)
    raster2 = QgsRasterCalculatorEntry()
    raster2.ref = 'band3@1'
    raster2.raster = band3
    raster2.bandNumber = 1
    entries.append(raster2)
    #NDWI Procesado de las bandas
    # calc=QgsRasterCalculator('("band3@1"-"band8@1")/("band3@1"+"band8@1")',output,'GTiff',band8.extent(),band8.width(),band8.height(),entries)
    calc=QgsRasterCalculator('(("band3@1"-"band8@1")/("band3@1"+"band8@1"))*100',output,'GTiff',band8.extent(),band8.width(),band8.height(),entries)
    calc.processCalculation()
  
  
def StringToRaster(raster):
    # Mira si se le pasa un string
    if isinstance(raster,basestring):
        fileInfo = QFileInfo(raster)
        baseName = fileInfo.baseName()
        path = fileInfo.filePath()
        # Chequea el base name y la ruta
        if (baseName and path):
            raster = QgsRasterLayer(path, baseName) # carga la capa raster
            if not raster.isValid():
                print ("Fallo al cargar la capa raster")
                return
        else:
            print ("Ruta de la capa raster o nombre de la capa incorrectos")
            return
    return raster


dir_imagenes = r'C:\Users\UserUNIR1\Desktop\FINAL_WIT\ImagenesSentinel2\imagenes'
os.chdir(dir_imagenes) # cambio de directorio para trabajar con las imagenes

for item in os.listdir(dir_imagenes): # examina todos los documentos en el directorio bas
    print (item)
    # os.chdir(item)
    
    for foto in os.listdir(item):    
    
        print (foto)
        ruta = os.path.abspath(item) # ruta absoluta
        print (ruta)
        
        if foto.endswith("B03.jp2") or foto.endswith("B03_10m.jp2"): # rasteriza la banda B03
            print ("b03")
            b03 = StringToRaster(ruta + r"/" + foto)
        if foto.endswith("B04.jp2") or foto.endswith("B04_10m.jp2"): # rasteriza la banda B04
            print ("B04")
            b04 = StringToRaster(ruta + r"/" +  foto)
        if foto.endswith("B08.jp2") or foto.endswith("B08_10m.jp2"): # rasteriza la banda B08
            print ("b08")
            b08 = StringToRaster(ruta + r"/" +  foto)        
           
    # Recorte de la capa b08 con la capa de parcela como mascara
    parcela = r"C:\Users\UserUNIR1\Desktop\FINAL_WIT\PARCELA_ENTREMONTES\parcela.shp"
    mask = r"C:\Users\UserUNIR1\Desktop\FINAL_WIT\MASA_ENTREMONTES\masa.shp"
    
    b08parcela = ruta + r"\b08parcela"
    b08masa = ruta + r"\b08masa"
    #print ("b08parcela")
    print ("b08masa")
    
    Processing.initialize()
    Processing.updateAlgsList()
    processing.runalg('gdalogr:cliprasterbymasklayer', 
                                 b08,      #INPUT <ParameterRaster>
                                 mask,     #MASK <ParameterVector>
                                 "0",      #NO_DATA <ParameterString>
                                 False,    #ALPHA_BAND <ParameterBoolean>
                                 True,     #CROP_TO_CUTLINE <ParameterBoolean>
                                 True,     #KEEP_RESOLUTION <ParameterBoolean>
                                 5,        #RTYPE <ParameterSelection>
                                 0,        #COMPRESS <ParameterSelection>
                                 1,        #JPEGCOMPRESSION <ParameterNumber>
                                 1,        #ZLEVEL <ParameterNumber>
                                 1,        #PREDICTOR <ParameterNumber>
                                 False,    #TILED <ParameterBoolean>
                                 0,        #BIGTIFF <ParameterSelection>
                                 False,    #TFW <ParameterBoolean>
                                 "",       #EXTRA <ParameterString>
                                 #b08parcela)   #OUTPUT <OutputRaster> 
                                 b08masa)   #OUTPUT <OutputRaster> 
         
    #print ("b08p")
    print ("b08m")
    #b08p = StringToRaster( ruta + r"\b08parcela.tif") # rasteriza la capa B08 cortada con las parcelas
    b08m = StringToRaster( ruta + r"\b08masa.tif") # rasteriza la capa B08 cortada con las parcelas
    
    # especifica como nombre le fecha de la imagen
    file_date = ruta.split('\\')[-1]
    nombre_date = r"{}/{}".format(dir_imagenes, file_date)

    #NDVI(b04,b08p,nombre_date + r"_ndvi.tiff") # calcula el NDVI
    #NDWI(b03,b08p,nombre_date + r"_ndwi.tiff") # calcula el NDWI
    NDVI(b04,b08m,nombre_date + r"_ndvi.tiff") # calcula el NDVI
    NDWI(b03,b08m,nombre_date + r"_ndwi.tiff") # calcula el NDWI
    
    processing.runalg('gdalogr:polygonize',nombre_date + r"_ndvi.tiff", 'NDVI', nombre_date + r"_ndvi.shp") # Raster to Vectorial NDVI
    processing.runalg('gdalogr:polygonize',nombre_date + r"_ndwi.tiff", 'NDWI', nombre_date + r"_ndwi.shp") # Raster to Vectorial NDWI
    
    processing.runalg("qgis:joinattributesbylocation", parcela, nombre_date + r"_ndvi.shp", u'intersects', 0, 0, '', 1, nombre_date + r"_ndvi_final.shp") # Unir atributos por localizacion NDVI
    processing.runalg("qgis:joinattributesbylocation", parcela, nombre_date + r"_ndwi.shp", u'intersects', 0, 0, '', 1, nombre_date + r"_ndwi_final.shp") # Unir atributos por localizacion NDWI
    
    fecha_captura = nombre_date[-21:-13]
    print (fecha_captura)
       
    #processing.runalg('qgis:fieldcalculator', nombre_date + r"_ndvi_final.shp", "fecha", 2, 10, 0, True, fecha_captura, nombre_date + r"_ndvi_final_con_fecha.shp") # Campo fecha NDVI
    #processing.runalg('qgis:fieldcalculator', nombre_date + r"_ndwi_final.shp", "fecha", 2, 10, 0, True, fecha_captura, nombre_date + r"_ndwi_final_con_fecha.shp") # Campo fecha NDWI
    
    
        
    #SHP to CSV NDVI
    shpfile = nombre_date + r"_ndvi_final.shp" #sys.argv[1]
    csvfile = nombre_date + r"_ndvi.csv" #sys.argv[2]

    #Open files NDVI
    csvfile=open(csvfile,'wb')
    ds=ogr.Open(shpfile)
    lyr=ds.GetLayer()

    #Get field names NDVI
    dfn=lyr.GetLayerDefn()
    nfields=dfn.GetFieldCount()
    fields=[]
    for i in range(nfields):
        fields.append(dfn.GetFieldDefn(i).GetName())
    fields.append('fecha')
    fields.append('kmlgeometry')   
    csvwriter = csv.DictWriter(csvfile, fields)
    try:csvwriter.writeheader() #python 2.7+
    except:csvfile.write(','.join(fields)+'\n')

    # Write attributes and kml out to csv NDVI
    for feat in lyr:
        attributes=feat.items()
        geom=feat.GetGeometryRef()
        attributes['fecha']=fecha_captura
        attributes['kmlgeometry']=geom.ExportToKML()
        csvwriter.writerow(attributes)

    #clean up NDVI
    del csvwriter,lyr,ds
    csvfile.close()
                     
    
    #SHP to CSV NDWI    
    shpfile = nombre_date + r"_ndwi_final.shp" #sys.argv[1]
    csvfile = nombre_date + r"_ndwi.csv" #sys.argv[2]

    #Open files NDWI
    csvfile=open(csvfile,'wb')
    ds=ogr.Open(shpfile)
    lyr=ds.GetLayer()

    #Get field names NDWI
    dfn=lyr.GetLayerDefn()
    nfields=dfn.GetFieldCount()
    fields=[]
    for i in range(nfields):
        fields.append(dfn.GetFieldDefn(i).GetName())
    fields.append('fecha')
    fields.append('kmlgeometry')
    csvwriter = csv.DictWriter(csvfile, fields)
    try:csvwriter.writeheader() #python 2.7+
    except:csvfile.write(','.join(fields)+'\n')

    # Write attributes and kml out to csv NDWI
    for feat in lyr:
        attributes=feat.items()
        geom=feat.GetGeometryRef()
        attributes['fecha']=fecha_captura
        attributes['kmlgeometry']=geom.ExportToKML()
        csvwriter.writerow(attributes)

    #clean up NDWI
    del csvwriter,lyr,ds
    csvfile.close()
    
    #Columna fecha NDWI
    
        
    
        
#app.exit()
