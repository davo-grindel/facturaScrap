import pdfplumber
import os
from os import listdir
from os.path import isfile, join
import csv
import re

directory = './procesar/'
data = [['Numero de Factura', 'Fecha', 'C.U.I.T.', 'IVA', 'Total Bruto Gravado', 'Total general']]
n_ = r'^N°'
fecha_ = r'^Fecha:'
t___ = r'^C\.U\.I\.T\.:'
gravado = r'^IVA..Total.Bruto.Gravado'
general = r'^Total.General'
iva_text = r'IVA.\d'


def scrape_pdf(files):
    for f in files:
        print('PROCESS FILE...', f)
        with pdfplumber.open(directory+f) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()
            split = text.split('\n')
            for i in range(len(split)):
                if re.match(n_, split[i]):
                    x = re.search(r'(\d+-\d+)', split[i])
                    factura_nun = x.group()
                elif re.match(fecha_, split[i]):
                    x = re.search(r'(\d+\.\d+\.\d+)', split[i])
                    fecha = x.group()
                elif re.match(t___, split[i]):
                    x = re.search(r'(\d+-\d+-\d+)', split[i])
                    cuit = x.group()
                elif re.match(gravado, split[i]):
                    x = re.split('%', split[i])
                    y = re.search(r'[0-9][0-9]', x[0])
                    total_bruto_gravado=x[1].lstrip()
                elif re.match(general, split[i]):
                    t = re.split(' ', split[i])
                    total_general = t[2].lstrip()
                elif re.match(iva_text,split[i]):
                    spl = re.split('%', split[i])
                    iva = re.search(r'[0-9][0-9]', spl[0])
                    iva = iva.group()
            data.append([factura_nun, fecha, cuit, iva, total_bruto_gravado, total_general])
        os.rename(directory + f, './scrapeadas/' + f)
    pass


files = [f for f in listdir(directory) if isfile(join(directory, f))]
if not files:
    input('There is no files to process in directory procesar')
    exit()
else:
    scrape_pdf(files)
    csv_file_path = 'carga facturas.csv'
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"CSV file '{csv_file_path}' created successfully.")
