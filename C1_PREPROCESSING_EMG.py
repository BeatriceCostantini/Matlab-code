#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 10:02:31 2023

@author: dantetrabassi
"""
# Importo le librerie che mi servono per far runnare il codice
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt

# Carico il set di dati EMG che mi serve
file_path = '/Users/alba.dantonio/Desktop/EMG SP-HS/DATABASE_MEAN_ENVELOPE_FINAL_PARAPARESI.csv'
dataset = pd.read_csv(file_path)

# Escludo la prima osservazione di tutte le features e dell'output perchè credo sia un conteggio delle ragazze
dataset = dataset.iloc[1:, :]  # Escludo la prima riga

# Escludo le colonne che non mi servono
columns_to_exclude = ['ID', 'TRIAL', 'ON/OFF R_RF','ON/OFF R_VL', 'ON/OFF R_VM', 'ON/OFF R_G', 'ON/OFF R_BFCL','ON/OFF R_TA','ON/OFF R_PL','ON/OFF R_SO','ON/OFF R_GL','ON/OFF R_GMA']
dataset = dataset.drop(columns=columns_to_exclude)

# Encodizzo le colonne categoriche che hanno due possibili valori (ON/OFF muscolari)
#binary_columns = ['ON/OFF R_RF','ON/OFF R_VL', 'ON/OFF R_VM', 'ON/OFF R_G', 'ON/OFF R_BFCL','ON/OFF R_TA','ON/OFF R_PL','ON/OFF R_SO','ON/OFF R_GL','ON/OFF R_GMA']  # Sostituisci con i nomi delle tue colonne
#label_encoder = LabelEncoder()
#for col in binary_columns:
#    dataset[col] = label_encoder.fit_transform(dataset[col])

# Encodizzo la colonna "Phases" in maniera ordinata che rappresenta le fasi di ciclo del passo considerate da noi
#phases_mapping = {"HEEL CONTACT": 0, "SINGLE STANCE": 1, "TERMINAL STANCE": 2, "SWING": 3}
#dataset['Phases'] = dataset['Phases'].map(phases_mapping)

# Salvo la colonna 'Patology' scritta così per l'encoding che farò dopo
pathology_column = dataset['Patology']

# Escludo la colonna 'Patology' prima della standardizzazione che sceglierò
dataset = dataset.drop(columns=['Patology'])

# Standardizzazione fra 0 e 1 (uso la min max)
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(dataset.values)
dataset_scaled = pd.DataFrame(scaled_data, columns=dataset.columns)

# Aggiungo di nuovo la colonna 'Patology' al dataset standardizzato tramite minmax
dataset_scaled['Patology'] = pathology_column

# Encoding dell'output 'Patology' con 0 per 'NORMATIVO' e 1 per 'ATASSIA' (associa praticamente 0 alla prima classe che incontra che nel set mean envelope final sono i Normativi)
label_encoder_output = LabelEncoder()
dataset_scaled['Patology'] = label_encoder_output.fit_transform(dataset_scaled['Patology'])
dataset_scaled['Patology'] = dataset_scaled['Patology'].map({0: 1, 1: 0})

# Creo  heatmap di correlazione per andare a valutare il grado di correlazione parziale (multicollinearità?)
correlation_matrix = dataset_scaled.corr()

# Creazione della heatmap con alcuni parametri aggiuntivi per la visualizzazione
plt.figure(figsize=(12, 10))  # Dimensioni del plot

# Visualizzazione della heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)  # Aggiunta delle annotazioni e specifica del formato dei numeri

# Regolazione degli assi
plt.xticks(rotation=45)  # Ruota le etichette dell'asse x di 45 gradi
plt.yticks(rotation=0)   # Non ruota le etichette dell'asse y

# Titolo del plot
plt.title('Heatmap di Correlazione')

# Visualizzazione
plt.tight_layout()  # Per assicurare la corretta visualizzazione
plt.show()

# Salva il nuovo dataset encodificato come file CSV sul mio desktop
output_file_path = '/Users/alba.dantonio/Desktop/Dataset_Paraparesi_encodificato.csv'
dataset_scaled.to_csv(output_file_path, index=False)