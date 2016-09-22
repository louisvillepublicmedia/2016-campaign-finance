import agate, os, itertools, time, datetime, glob, csv
from datetime import date

text_type = agate.Text()
datetime_type = agate.DateTime()

tester = agate.TypeTester(force={
    'contb_receipt_dt': agate.Text()
})

today = date.today()
datestamp = str(today.year) + str(today.month) + str(today.day)

ky_candidates_file = str(glob.glob('data/csv/process/*ky-candidate-contributions.csv')[0])

ky_candidate_contributions = agate.Table.from_csv(ky_candidates_file, column_types=tester)

current_candidate_cmte_ids = ['C00580100','C00575795']
    #Trump, Donald J. = C00580100
    #Sanders, Bernard = C00577130
    #Kasich, John R. = C00581876
    #Clinton, Hillary Rodham = C00575795
    #Cruz, Rafael Edward 'Ted' = C00574624
    
    
def candidate_brackets(contributions):
    #brackets
    #bracket1 = 200 and under
    #bracket2 = 200.01 - 499.99
    #bracket3 = 500 - 999.99
    #bracket4 = 1,000 - 1,999,99
    #bracket5 = 2,000 and over
    
    for candidate in current_candidate_cmte_ids:
        total_contribs = []
        bracket1 = []
        bracket2 = []
        bracket3 = []
        bracket4 = []
        bracket5 = []
        
        if candidate == 'C00580100':
            candidate_nm = 'Trump, Donald J.'
        if candidate == 'C00575795':
            candidate_nm = 'Clinton, Hillary Rodham'
    
        for row in contributions.rows:
            if row['cmte_id'] == candidate:
                total_contribs.append(row['contb_receipt_amt'])
                if row['contb_receipt_amt'] <= 200:
                    bracket1.append(row['contb_receipt_amt'])
                elif row['contb_receipt_amt'] > 200 and row['contb_receipt_amt'] < 500:
                    bracket2.append(row['contb_receipt_amt'])
                elif row['contb_receipt_amt'] >= 500 and row['contb_receipt_amt'] < 1000:
                    bracket3.append(row['contb_receipt_amt'])
                elif row['contb_receipt_amt'] >= 1000 and row['contb_receipt_amt'] < 2000:
                    bracket4.append(row['contb_receipt_amt'])
                elif row['contb_receipt_amt'] >= 2000:
                    bracket5.append(row['contb_receipt_amt'])
        
        count_total_contribs = len(total_contribs)                   
        count_bracket1 = len(bracket1)
        count_bracket2 = len(bracket2)
        count_bracket3 = len(bracket3)
        count_bracket4 = len(bracket4)
        count_bracket5 = len(bracket5)
        
        perc_bracket1 = (float(count_bracket1) / float(count_total_contribs))*100
        perc_bracket2 = (float(count_bracket2) / float(count_total_contribs))*100
        perc_bracket3 = (float(count_bracket3) / float(count_total_contribs))*100
        perc_bracket4 = (float(count_bracket4) / float(count_total_contribs))*100
        perc_bracket5 = (float(count_bracket5) / float(count_total_contribs))*100
        
        print candidate_nm
        print 'total contribution count: ' + str(count_total_contribs)
        print '$200 and under: ' + str(count_bracket1) + ' (' + str(perc_bracket1) + '%)'
        print '$200.01 - $499.99: ' + str(count_bracket2) + ' (' + str(perc_bracket2) + '%)'
        print '$500 - $999.99: ' + str(count_bracket3) + ' (' + str(perc_bracket3) + '%)'
        print '$1,000 - $1,999,99: ' + str(count_bracket4) + ' (' + str(perc_bracket4) + '%)'
        print '$2,000 and over: ' + str(count_bracket5) + ' (' + str(perc_bracket5) + '%)'
        
def monthly_contrib_count():
            
    candidate_contribs_with_monthyear = ky_candidate_contributions.compute([
        ('month_year', agate.Formula(text_type, lambda r: r['contb_receipt_dt'][-6:])),
        ('date', agate.Formula(text_type, lambda r: datetime.datetime.strptime(r['contb_receipt_dt'], '%d-%b-%y')))
    ])
    
    july16_contributions = candidate_contribs_with_monthyear.where(
        lambda r: r['month_year'] == 'JUL-16'
    )
    
    positive_contributions = july16_contributions.where(
        lambda r: r['contb_receipt_amt'] > 0
    )
                
    candidate_brackets(july16_contributions)
    
    
def time_span():
            
    candidate_contribs_with_monthyear = ky_candidate_contributions.compute([
        ('month_year', agate.Formula(text_type, lambda r: r['contb_receipt_dt'][-6:])),
        ('date', agate.Formula(text_type, lambda r: datetime.datetime.strptime(r['contb_receipt_dt'], '%d-%b-%y')))
    ])
    
    candidate_contribs_with_monthyear.to_csv('data/csv/process/' + datestamp + 'ky-contribs-with-monthyear.csv')
        

    
    

time_span()   
#monthly_contrib_count()
#candidate_brackets(ky_candidate_contributions)