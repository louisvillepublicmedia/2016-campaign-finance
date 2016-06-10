import agate
from datetime import date


# Refine the huge individual contributions doc to only contributions from KY citizens
today = date.today()
datestamp = str(today.year) + str(today.month) + str(today.day)
    
all_contributions = agate.Table.from_csv('data/csv/process/' + datestamp + '_individual-contributions.csv', delimiter='|')
ky_overall = all_contributions.where(
        lambda r: r['STATE'] == 'KY'
    )
ky_overall.to_csv('data/csv/process/' + datestamp + '_ky-individual-contribs.csv', delimiter='|')