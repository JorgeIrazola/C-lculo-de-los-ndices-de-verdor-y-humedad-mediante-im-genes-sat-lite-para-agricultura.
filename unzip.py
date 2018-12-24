import os, zipfile, re
import shutil 

# definicion de constantes
dir_name = r'C:\Users\UserUNIR1\Desktop\FINAL_WIT\ImagenesSentinel2'
extension = ".zip"
carpeta = ".SAFE"
contador = 1

# cambio de directorio para trabajar con las imagenes comprimidas
os.chdir(dir_name) 

for item in os.listdir(dir_name): # examina todos los documentos en el directorio base
    if item.endswith(extension): # busca entre esos archivos los que tengan extension ".zip" 
        file_name = os.path.abspath(item) # coge la ruta absoluta de los archivos
        file_date = file_name.split('\\')[-1][11:32] # coge la fecha archivos
                
        zip_ref = zipfile.ZipFile(item) # crea el objeto zipfile
        
        for file in zip_ref.namelist(): # examina todos los documentos en el .zip
            
            # busca las fotografias de las bandas infrarojas B03, B04 y B08
            if re.match(r'.*B03.*\.jp2', file) or re.match(r'.*B04.*\.jp2', file) or re.match(r'.*B08.*\.jp2', file):
                                
                zip_ref.extract(file, dir_name) # extrae imagen satelite                
                
                # selecciona o crea el directorio donde guardar las imagenes
                directorio = r"{}/imagenes/{}".format(dir_name, file_date)
                if not os.path.exists(directorio): os.makedirs(directorio)
                                    
                shutil.copy2(file, directorio ) # copia a imagenenes 
                #zip_ref.extractall(dir_name) # extract file to dir
        zip_ref.close() # cierra el objeto zipfile
        contador += 1
        # os.remove(file_name) # borra el archivo .zip 

for item in os.listdir(dir_name): # examina todos los documentos en el directorio base
    if item.endswith(carpeta): # busca la extension ".SAFE" de las imagenes decomprimidas
        shutil.rmtree(item) # borra la carpeta .SAFE con las imagenes descargadas