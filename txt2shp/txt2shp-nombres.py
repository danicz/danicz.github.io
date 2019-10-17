import osgeo.ogr as ogr
import osgeo.osr as osr
import csv
import argparse
import re

#NOMBRE DE ARCHIVO DE ENTRADA Ej.:
# 101-NO2G-5-1.txt
#  |       | |--Version
#  |       |----Nivel de acceso
#  |------------Codigo de objeto geografico

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--file_in", help="Nombre de archivo a procesar con path, ej: D:\IDECOM\IDECOM_20190507_1419\\101-NO2G-1-1.txt")
parser.add_argument("-c", "--cod", help="Codigo numerico del objeto geografico [101, 102, 103] -(x default del nombre de entrada)")
parser.add_argument("-v", "--ver", help="Numero de version -(x default del nombre de entrada)")
parser.add_argument("-o", "--file_out", help="Nombre del archivo shape de salida -(x default del nombre de entrada)")

args = parser.parse_args()
 

if args.file_in:
	print ("El nombre de archivo a procesar es (x parametro): ", args.file_in)
	filein = args.file_in
else:
	filein ="D:\Laburo\IDECOM\ArchivosTXT\IDECOM_20190507_1419\\101-NO2G-1-1.txt"

#obtener nombre del archivo del dato de entrada de todo el path mas el nombre del archivo
x = filein.split("\\")
l=len(x)
nombrefile= x[l-1]
print(nombrefile)
#obtener del nombre:
#  nro. objeto (101,102, 103)
#  nivel de acceso
#  version
partes= nombrefile.split("-")
objeto=partes[0]
nivel=partes[2]
vers=partes[3]
versi = vers.split(".")
version=vers[0]
	

if args.cod:
	print ("Codigo numerico del objeto geografico (x parametro): ", args.cod)
	objeto = args.cod
else:
	print ("Codigo numerico del objeto geografico (x nombre de archivo de entrada): ", objeto)

if args.ver:
	print ("Numero de version (x parametro): ", args.ver)
	version = args.ver
else:
	print ("Numero de version (x nombre de archivo de entrada): ", version)

if args.file_out:
	print ("Nombre del archivo shape de salida(x parametro): ", args.file_out)
	fileout = args.file_out
	y=fileout.split('.')
	nombrefileout=y[0]
else:
	#VER TEMA DIRECTORIO de salida
	y=nombrefile.split('.')
	nombrefileout=y[0]
	fileout= nombrefileout+".shp"
	print ("Nombre del archivo shape de salida (x nombre de archivo de entrada): ", fileout)





# Uso de dictionary reader para la lectura del archivo
reader = csv.DictReader(open(filein,"rt"),
    delimiter='|',
    quoting=csv.QUOTE_NONE)

headers = reader.fieldnames

print(headers)

# Seteo de el driver para el shapefile
driver = ogr.GetDriverByName("ESRI Shapefile")



# Crear el data source que sera el shapefile de salida
data_source = driver.CreateDataSource(fileout)



# crear la spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

# crear el layer
layer = data_source.CreateLayer(nombrefileout, srs, ogr.wkbPoint)



cuicom = ogr.FieldDefn("CUICOM", ogr.OFTString);
cuicom.SetWidth(11);
layer.CreateField(cuicom);

# Agregar campos, (grabandolos con nombres descriptivos 29/8/19)
for i in headers:
  if i == 'ANTCOT':
    layer.CreateField(ogr.FieldDefn("Cota", ogr.OFTInteger))
  elif i ==  'BD3GPP':  
    bd3gpp = ogr.FieldDefn("Banda", ogr.OFTString);
#lo cambie de 10 a 2 x requerimiento
    bd3gpp.SetWidth(2); 
    layer.CreateField(bd3gpp);
  elif i == 'ACTUAL':  
    actual = ogr.FieldDefn("Fecha", ogr.OFTString);
    actual.SetWidth(8);
    layer.CreateField(actual);
  elif i == 'OPERAT':  
    operat = ogr.FieldDefn("Operativo", ogr.OFTString);
    operat.SetWidth(2);
    layer.CreateField(operat);
  elif i =='OBSERV':  
    observ = ogr.FieldDefn("Observ", ogr.OFTString);
    observ.SetWidth(15);
    layer.CreateField(observ);
  elif i =='LONDEC':  
    londec = ogr.FieldDefn("Longitud", ogr.OFTReal);
    londec.SetPrecision(6);
    londec.SetWidth(12);
    layer.CreateField(londec);
  elif i =='LATDEC':  
    latdec = ogr.FieldDefn("Latitud", ogr.OFTReal);
    latdec.SetPrecision(6);
    latdec.SetWidth(12);
    layer.CreateField(latdec);
  elif i == 'ANTALT':
    layer.CreateField(ogr.FieldDefn("Altura", ogr.OFTInteger))    
  elif i == 'ANTACI':
    layer.CreateField(ogr.FieldDefn("Acimut", ogr.OFTInteger))    
  elif i == 'VINCFO':  
    vincfo = ogr.FieldDefn("VinculoFO", ogr.OFTString);
    vincfo.SetWidth(2);
    layer.CreateField(vincfo);
  elif i == 'VINCRE':  
    vincre = ogr.FieldDefn("VinculoRad", ogr.OFTString);
    vincre.SetWidth(2);
    layer.CreateField(vincre);
  elif i == 'POTCAN':
    layer.CreateField(ogr.FieldDefn("Potxcanal", ogr.OFTInteger))    
  elif i == 'ANTTIL':
    layer.CreateField(ogr.FieldDefn("Tilt", ogr.OFTInteger))    
  elif i =='ANTGAN':  
    antgan = ogr.FieldDefn("Ganancia", ogr.OFTReal);
    antgan.SetPrecision(2);
    antgan.SetWidth(5);
    layer.CreateField(antgan);
  elif i == 'VINTRA':
    layer.CreateField(ogr.FieldDefn("CapRadio", ogr.OFTInteger))    
  elif i =='PROCED':  
    proced = ogr.FieldDefn("Proced", ogr.OFTString);
    proced.SetWidth(15);
    layer.CreateField(proced);
  elif i =='IDEORI':  
    ideori = ogr.FieldDefn("IdOrigen", ogr.OFTString);
    ideori.SetWidth(15);
    layer.CreateField(ideori);
  elif i =='IDESEC':  
    idesec = ogr.FieldDefn("IdDesc", ogr.OFTString);
    idesec.SetWidth(15);
    layer.CreateField(idesec);
  elif i =='ANBANA':  
    anbana = ogr.FieldDefn("AnchoBanda", ogr.OFTReal);
    anbana.SetPrecision(2);
    anbana.SetWidth(5);
    layer.CreateField(anbana);
  else:
    layer.CreateField(ogr.FieldDefn(i, ogr.OFTString));

#contador de registro
i=0

#Tabla de conversion de valores en el campo BD3GPP para 2G y 3G
#tabla = {'a': 850, 
#  'A': 1900,            
#  'A’': 850,
#  'A”': 850,
#  'AÂ’': 850,          
#  'B': 850,
#  'B’': 850,
#  'C': 1900,
#  'D': 1900}

tabla = {'A': 1900,            
  'C': 1900,
  'D': 1900}



# Para cada registro de entrada graba los datos y el objeto geografico  (grabandolos con nombres descriptivos 29/8/19)
for row in reader:
  
  #generacion de CUICOM
  i=i+1
  cuicom=objeto + version.zfill(2) + str(i).zfill(6)
  feature = ogr.Feature(layer.GetLayerDefn())
  feature.SetField('CUICOM', cuicom)
  
# Para cada campo graba los datos  
  for j in headers:
# Correcion de datos x pedido
# filtrar de la banda todo lo que no sea numero y dejar solo los dos primeros numeros en caso de tener mas, y loguear.
  		
    if j == 'BD3GPP':
      a=row[j]
#2G y 3G
      if objeto in ["101","102"]:
        if a in tabla.keys():
          str1 = tabla[a]
        else:
          str1 ="850"
        print("CUICOM:", cuicom, " BD3GPP original:", a, "corregido:", str1)
        feature.SetField("Banda", str1)
          
#4G          
      elif not(a.isdigit() & (len(a)<=2)):
        dig=0
        corregir=0
        str1=""
        for k in a:
          if k.isdigit():
            if (dig < 2):
              dig = dig+1
              str1= str1+str(k)
        if (str1==""):
          str1="0"
        print("CUICOM:", cuicom, " BD3GPP original:", a, "corregido:", str1)
        feature.SetField("Banda", str1)
      else:
        feature.SetField("Banda", row[j])

    elif j == 'ACTUAL':
#Correcion de fecha de "2019-03-21 16:17:16" -->20190321
      act=row[j]
      fechas= re.split("[\s-]", act)
      fecha= fechas[0]+fechas[1]+fechas[2]
      feature.SetField("Fecha", fecha) 
    else:
      if j == 'ANTCOT':
        feature.SetField("Cota", row[j])
      elif j == 'OPERAT':  
        feature.SetField("Operativo", row[j])
      elif j =='OBSERV':  
        feature.SetField("Observ", row[j])
      elif j =='LONDEC':  
        feature.SetField("Longitud", row[j])
      elif j =='LATDEC':  
        feature.SetField("Latitud", row[j])
      elif j == 'ANTALT':
        feature.SetField("Altura", row[j])
      elif j == 'ANTACI':
        feature.SetField("Acimut", row[j])
      elif j == 'VINCFO':  
        feature.SetField("VinculoFO", row[j])
      elif j == 'VINCRE':  
        feature.SetField("VinculoRad", row[j])
      elif j == 'POTCAN':
        feature.SetField("Potxcanal", row[j])
      elif j == 'ANTTIL':
        feature.SetField("Tilt", row[j])
      elif j =='ANTGAN':  
        feature.SetField("Ganancia", row[j])
      elif j == 'VINTRA':
        feature.SetField("CapRadio", row[j])
      elif j =='PROCED':  
        feature.SetField("Proced", row[j])
      elif j =='IDEORI':  
        feature.SetField("IdOrigen", row[j])
      elif j =='IDESEC':  
        feature.SetField("IdDesc", row[j])
      elif j =='ANBANA':  
        feature.SetField("AnchoBanda", row[j])
      else:
        feature.SetField(j, row[j])
          

  wkt = "POINT(%f %f)" %  (float(row['LONDEC']) , float(row['LATDEC']))
  point = ogr.CreateGeometryFromWkt(wkt)
  feature.SetGeometry(point)
  layer.CreateFeature(feature)
  feature = None

data_source = None
