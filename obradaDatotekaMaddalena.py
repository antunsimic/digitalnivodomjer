import pandas as pd #biblioteka za rad s podacima
import os #za pristupanje datotekama u direktoriju

def format_date(date):
    if pd.isnull(date) or date == '':
        return ''
    else:
        return date.strftime('%d.%m.%Y %H:%M:%S')

data_frames = []
excel_files = [file for file in os.listdir() if file.endswith('.xlsx')] #sve excel datoteke u trenutnom direktoriju

#iteracija kroz sve excel datoteke i zapisivanje podataka u liste
for file in excel_files:
    data = pd.read_excel(file)
    selected_columns = ['Module serial', 'Timestamp', 'Reading', 'Value7']
    data = data[selected_columns]
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%d.%m.%Y %H:%M:%S')
    data['Timestamp'] = data['Timestamp'].apply(format_date)
    data_frames.append(data)


