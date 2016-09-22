import agate, os.path, csv
from datetime import date


# Refine the huge individual contributions doc to only contributions from KY citizens
today = date.today()
datestamp = str(today.year) + str(today.month) + str(today.day)
infile = 'data/csv/process/' + datestamp + '_individual-contributions.csv'
outfile = 'data/csv/process/' + datestamp + '_ky-individual-contribs.csv'
headerfile = 'headers/itcont-header.csv'

with open(outfile, 'wb') as outcsv:
    writer = csv.writer(outcsv, delimiter='|')
    
    with open(headerfile, 'rb') as header:
        header_reader = csv.reader(header, delimiter='|')
        writer.writerows(header_reader)
        
    with open(infile, 'rb') as incsv:
        reader = csv.DictReader(incsv, delimiter='|')
        for row in reader:
            if row['STATE'] == 'KY':
                columns = [row['CMTE_ID'],row['AMNDT_IND'],row['RPT_TP'],row['TRANSACTION_PGI'],row['IMAGE_NUM'],row['TRANSACTION_TP'],row['ENTITY_TP'],row['NAME'],row['CITY'],row['STATE'],row['ZIP_CODE'],row['EMPLOYER'],row['OCCUPATION'],row['TRANSACTION_DT'],row['TRANSACTION_AMT'],row['OTHER_ID'],row['TRAN_ID'],row['FILE_NUM'],row['MEMO_CD'],row['MEMO_TEXT'],row['SUB_ID']]
                writer.writerow(columns)
                #writer.writerows(reader)            


#print os.path.isfile(filepath)
#all_contributions = agate.Table.from_csv(filepath, delimiter='|')
#ky_overall = all_contributions.where(
#        lambda r: r['STATE'] == 'KY'
#    )
#ky_overall.to_csv('data/csv/process/' + datestamp + '_ky-individual-contribs.csv', delimiter='|')