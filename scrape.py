import urllib, zipfile, os, csv, time, glob
from datetime import date

# Clear the data directories so you can download fresh files
def clear_data_directory():
    zipfiles = glob.glob("data/*.zip")
    for f in zipfiles:
        os.remove(f)
        
    csvfiles = glob.glob('data/csv/*.csv')
    for f in csvfiles:
        os.remove(f)
        
    processfiles = glob.glob('data/csv/process/*.csv')
    for f in processfiles:
        os.remove(f)
    

# Download and unpack donations by KY citizens to canddiates
def download_state_candidate_contributions():
    today = date.today()
    datestamp = str(today.year) + str(today.month) + str(today.day)
    
    urllib.urlretrieve('ftp://ftp.fec.gov/FEC/Presidential_Map/2016/P00000001/P00000001-KY.zip', 'data/P00000001-KY.zip')
    with zipfile.ZipFile('data/P00000001-KY.zip', 'r') as z:
        downloaded = z.extractall("data/csv")
        
    
    # Remove extraneous column and save with datestamp
    with open('data/csv/P00000001-KY.csv',"rb") as incsv:
        reader = csv.reader(incsv)
        with open('data/csv/process/' + datestamp + '_ky-candidate-contributions.csv','wb') as outcsv:
            writer = csv.writer(outcsv)
            # We're writing individual rows because there seems to be an issue with this
            # table and extra, invisible data in the 19th column. Need to drop that 
            # column before we begin analyzing 
            for row in reader:
                writer.writerow((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17]))
                
    
# Download and unpack all individual contributions
def download_individual_contrib():
    today = date.today()
    datestamp = str(today.year) + str(today.month) + str(today.day)
    
    urllib.urlretrieve('ftp://ftp.fec.gov/FEC/2016/indiv16.zip', 'data/indiv16.zip')
    with zipfile.ZipFile('data/indiv16.zip', "r") as z:
        z.extractall("data/txt")
        
    # convert to csv
    csv_file = os.rename('data/txt/itcont.txt', 'data/csv/itcont.csv')
    
    # add header row
    with open('data/csv/process/' + datestamp + '_individual-contributions.csv', 'wb') as outcsv:
        writer = csv.writer(outcsv)
        
        with open('headers/itcont-header.csv', 'rb') as incsv:
            reader = csv.reader(incsv)
            writer.writerows(reader)
            with open('data/csv/itcont.csv', 'rb') as indata:
                data_reader = csv.reader(indata)
                writer.writerows(data_reader)

        
# Download and unpack committee list
def download_cmte_list():
    today = date.today()
    datestamp = str(today.year) + str(today.month) + str(today.day)
    
    urllib.urlretrieve('ftp://ftp.fec.gov/FEC/2016/cm16.zip', 'data/cm16.zip')
    with zipfile.ZipFile('data/cm16.zip', "r") as z:
        z.extractall("data/txt")
        
    # convert to csv
    csv_file = os.rename('data/txt/cm.txt', 'data/csv/cm.csv')
    
    # add header row
    with open('data/csv/process/' + datestamp + '_cmte-list.csv', 'wb') as outcsv:
        writer = csv.writer(outcsv)
        
        with open('headers/cm-header.csv', 'rb') as incsv:
            reader = csv.reader(incsv)
            writer.writerows(reader)
            with open('data/csv/cm.csv', 'rb') as indata:
                data_reader = csv.reader(indata)
                writer.writerows(data_reader)
       

clear_data_directory()
download_state_candidate_contributions()
download_individual_contrib()
download_cmte_list()