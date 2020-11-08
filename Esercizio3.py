# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 13:02:32 2020

@author: gaiad
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Leggo lista dei log anonimizzati in formato json e memorizzo su struttura dati python
fin=open('/Users/gaiad/Downloads/input_data (1).json','r')
text=fin.read()
data1=json.loads(text)[0]


df=pd.DataFrame(data1, columns=['Data/Ora','ID','UC','contesto evento','componente','evento','descrizione','origine','IP'])


#Numero totale utenti 
users=df['ID'].unique()
tot_users=df['ID'].unique().size

#Numero log per utente
numlog_utente=df['ID'].value_counts()

#Lista eventi e numero log per evento
lista_eventi=list((df['evento']))
numlog_evento=df['evento'].value_counts()

#Quanti log ogni giorno
dt=pd.to_datetime(df['Data/Ora'])
lista_giorni=dt.dt.day
numlog_giorno=lista_giorni.value_counts()


#Creo tre sottoprogrammi che stampano: numero dei log per utente, per evento, e al giorno
i=0
def num_log_utente():
  print('Il numero totale degli utenti è : ' + str(tot_users))
  print('\n\n')
  print('Il numero dei log per ogni utente è : ' + '\n')
  for i in range(len(numlog_utente)):
    print('%s: %d \n' % (numlog_utente.index[i],numlog_utente[i])) 
    
def num_log_evento():
  print('\n\n')
  print('Il numero dei log per ogni evento è : ' + '\n')
  for i in range(len(numlog_evento)):
    print('%s: %d \n' % (numlog_evento.index[i],numlog_evento[i]))

def num_log_giorno():
  print('\n\n')
  print('Il numero dei log ogni giorno è : ' + '\n')
  for i in range(len(numlog_giorno)):
    print('%s: %d \n' % (numlog_giorno.index[i],numlog_giorno.iloc[i]))



num_log_utente()
num_log_evento()
num_log_giorno()


#Creo le tre liste con i log che ogni utente ha fatto per i tre eventi più significativi
numlog_utente_evento1=[]
numlog_utente_evento2=[]
numlog_utente_evento3=[]

def creo_lista1(users):
  for user in users:
    if user not in numlog_utente_evento1: 
       user= df.loc [(df ['ID'] == user) & (df ['evento'] == 'Visualizzato modulo corso')].shape[0]  
       numlog_utente_evento1.append(user)
    user+=1
creo_lista1(users)
    
def creo_lista2(users):
  for user in users:
    if user not in numlog_utente_evento2:
       user= df.loc [(df ['ID'] == user) & (df ['evento'] == 'Visualizzato corso')].shape[0]
       numlog_utente_evento2.append(user)
    user+=1
creo_lista2(users)
    
def creo_lista3(users):
  for user in users:
    if user not in numlog_utente_evento3:
       user= df.loc [(df ['ID'] == user) & (df ['evento'] == 'Aggiornato completamento attività del corso')].shape[0]
       numlog_utente_evento3.append(user)
    user+=1
creo_lista3(users)

#Creo un dataframe le cui righe sono gli accessi di ciascun utente ai tre eventi significativi

df_ = pd.DataFrame({'Visualizzato modulo corso':numlog_utente_evento1 , 'Visualizzato corso': numlog_utente_evento2 , 'Aggiornato completamento attività del corso':numlog_utente_evento3 }, index=users)

#Trasformo dataframe in matrice e faccio la media totale e la media relativa a ciascun utente
mat=df_.values
media_totale=np.mean(mat)


media_utente=[]
for i in range(len(mat)):
    m=np.mean(mat[i])
    media_utente.append(m)
media_utente=pd.Series(media_utente, index=users)

#Clusterizzo i dati in studenti attivi e inattivi
attivi=[]
inattivi=[]
i=0
for i in range(len(media_utente)):
  if media_utente[i]< media_totale:
    inattivi.append(media_utente.index[i])
  else:
    attivi.append(media_utente.index[i])


#Plot della distribuzione degli utenti in funzione della media di accessi ai tre eventi
x = users
y = media_utente

y1=np.empty(114); y1.fill(media_totale)
y1=(y1)

fig, ax = plt.subplots(1, figsize=(15, 10))
fig.suptitle('Scatterplot utenti')
# Creo lo Scatter Plot
ax.plot(x,y1)
ax.scatter(x, y,
 color="green", # Color of the dots
 s=30, # Size of the dots
 alpha=1, # Alpha/transparency of the dots (1 is opaque, 0 is transparent)
 linewidths=1) # Size of edge around the dots
ax.set_xlabel('utenti')
ax.set_ylabel('media utente per i tre eventi')
ax.plot(y1, color="blue", linewidth=2.5, linestyle="-", label="media totale")
ax.legend(loc='best')
plt.show()





