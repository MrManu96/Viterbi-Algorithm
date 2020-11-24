# -*- coding: utf-8 -*-

# Cabrera Sánchez Manuel Salvador
# Procesamiento de Lenguaje Natural
# Práctica no. 2

from __future__ import division
import os
import re
import nltk
import Stemmer
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import codecs
from operator import itemgetter

def max(list):
	maximo = list[0]
	for indice in range(1, len(list)):
		if list[indice] > maximo:
			maximo = list[indice]
	return maximo

def indmax(list):
	maximo = list[0]
	imax = 0
	for indice in range(1, len(list)):
		if list[indice] > maximo:
			maximo = list[indice]
			imax = indice
	return imax

corpus = "corpus_HMM.txt"
vocabulario = "token.txt"
frecuencias = "frecuencias.txt"
palabras = "palabras.txt"
etiquetas = "etiquetas.txt"
etiquetas_orden = "etiquetas_orden.txt"
palabras_orden = "palabras_orden.txt"
etiquetas_lista = []		# Lista con las etiquetas en orden alfabético y sin repetir (ALFABETO DE EMISIONES)
lista = []					# Lista con las etiquetas respetando el orden del corpus
lista_palabras = []			# Lista con las palabras en orden alfabético y sin repetir (ALFABETO DE OBSERVACIONES)
listap = []					# Lista con las palabras respetando el orden del corpus
frecuencia = []				# Frecuencia de las etiquetas 
contador_tokens = 0
modelo_leng = []
a_leng = []
modelo_mark = []
a_mark = []
palabras_lista_copia = []
listap2 = []

#################################################### SEPARANDO EN TOKENS

entrada = codecs.open(corpus,"r", "utf-8")
texto = entrada.read()
palabras_lista = texto.split()
#palabras_lista = nltk.word_tokenize(texto,"spanish")

#texto = textclean.clean(texto)
#palabras_lista = texto.split()
entrada.close()

#################################################### SEPARANDO PALABRAS Y ETIQUETAS

salida1 = codecs.open(palabras, "w", "utf-8")
salida2 = codecs.open(etiquetas, "w", "utf-8")
salida3 = codecs.open(palabras_orden, "w", "utf-8")
salida4 = codecs.open(etiquetas_orden, "w", "utf-8")
salida5 = codecs.open(frecuencias, "w", "utf-8")

for palabra in palabras_lista:
	if ((contador_tokens % 2) == 0):
		palabra = palabra.lower()
		listap.append(palabra)			# Palabras respetando el orden del corpus
		listap2.append(palabra)
		salida1.write(palabra+"\n")		# Escribimos todos los tokens en minusculas
		contador_tokens+=1
	else:
		palabras_lista_copia.append(palabra)
		lista.append(palabra)
		salida2.write(palabra+"\n")
		contador_tokens+=1

listap2.sort()
for palabra in listap2:
	if palabra not in lista_palabras:
		lista_palabras.append(palabra)

for palabra in lista_palabras:
	salida3.write(palabra+"\n")

i=-1
palabras_lista_copia.sort()
for palabra in palabras_lista_copia:
	if palabra in etiquetas_lista:
		frecuencia[i]+=1
	else:
		etiquetas_lista.append(palabra)
		frecuencia.append(1)
		i+=1

for dato in frecuencia:
	salida5.write(str(dato)+"\n")

for palabra in etiquetas_lista:
	salida4.write(palabra+"\n")

salida1.close()
salida2.close()
salida3.close()
salida4.close()
salida5.close()

print str(len(etiquetas_lista))

#################################################### OBTENIENDO VECTOR DE PROBABILIDADES INICIALES

for i in range(0,len(etiquetas_lista)):
	if lista[0] == etiquetas_lista[i]:
		a_leng.append( 2.00 / (1.00 + len(etiquetas_lista)) )
	else:
		a_leng.append( 1.00 / (1.00 + len(etiquetas_lista)) )
		
a_mark = a_leng			# Los vectores de probabilidades iniciales son iguales

#################################################### MATRIZ DE TRANSICIONES

contador = 0
for i in range(0, len(etiquetas_lista)):
	fila = []
	for j in range(0, len(etiquetas_lista)):
		for k in range (1, len(lista)):
			if lista[k] == etiquetas_lista[i]:
				anterior = lista[k-1]
				if anterior == etiquetas_lista[j]:
					contador += 1.00
		fila.append((contador+1.00) / (frecuencia[j]+len(etiquetas_lista)))
		contador = 0
	modelo_leng.append(fila)

print "A = "+str(a_leng)
print "M = "+str(modelo_leng)
print str(len(a_leng))
print str(len(modelo_leng))
print str(len(fila))

#################################################### MATRIZ DE EMISIONES

contador = 0
for i in range(0, len(lista_palabras)):
	fila = []
	for j in range(0, len(etiquetas_lista)):
		for k in range (0, len(listap)):
			if listap[k] == lista_palabras[i]:
				comparar = lista[k]
				if comparar == etiquetas_lista[j]:
					contador += 1.00
		fila.append((contador+1.00) / (frecuencia[j]+len(lista_palabras)))
		contador = 0
	modelo_mark.append(fila)

print modelo_mark
print str(len(modelo_mark))
print str(len(lista_palabras))

################################################### ALGORITMO DE VITERBI

A = modelo_leng
B = modelo_mark
P = a_leng

d = raw_input('Ingrese la cadena a etiquetar: \n')
d = d.split(" ")

delta1 = []
for i in range(0, len(lista_palabras)):
	if d[0] == lista_palabras[i]:
		renglon = B[i]
		for j in range(0, len(etiquetas_lista)):
			proba = P[j] * renglon[j]
			delta1.append(proba)

delta = []				# Matriz que contiene los valores delta
f = []					# Matriz que contiene los índices fi
for obs in range(1, len(d)):
	temp1 = []
	freng = []
	for eti in range(0, len(etiquetas_lista)):
		for i in range(0, len(lista_palabras)):
			if d[obs] == lista_palabras[i]:
				renglon1 = B[i]
				renglon2 = A[eti]
				deltatemp = []
				for j in range(0, len(etiquetas_lista)):
					proba = delta1[j] * renglon1[eti] * renglon2[j]
					deltatemp.append(proba)
				temp1.append(max(deltatemp))
				freng.append(indmax(deltatemp))
	delta.append(temp1)
	f.append(freng)

indice = len(delta)-1
etiquetado = []
etiquetado.append(indmax(delta[indice]))
etiqueta = etiquetado[0]

print etiquetas_lista[etiqueta]

i = len(delta)-1
while i > -1:
	reng = f[i]
	indice = reng[etiqueta]
	etiqueta = indice
	etiquetado.append(etiqueta)
	print etiquetas_lista[etiqueta]
	i -= 1

cadena = ''

i = len(etiquetado) - 1
while i > -1:
	numero = etiquetado[i]
	cadena = cadena + etiquetas_lista[numero] + ' '
	i -= 1

print '\n\n'
print 'La cadena ' + str(d) + ' fue etiquetada como: '
print cadena
