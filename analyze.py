import agate, os, itertools, time, datetime, glob
from datetime import date

text_type = agate.Text()

tester = agate.TypeTester(force={
    'contb_receipt_dt': agate.Text()
})

today = date.today()
datestamp = str(today.year) + str(today.month) + str(today.day)

ky_candidates_file = str(glob.glob('data/csv/process/*ky-candidate-contributions.csv')[0])
ky_all_contributions_file = str(glob.glob('data/csv/process/*ky-individual-contribs.csv')[0])
cmte_list_file = str(glob.glob('data/csv/process/*cmte-list.csv')[0])


ky_candidate_contributions = agate.Table.from_csv(ky_candidates_file, column_types=tester)
ky_all_contributions = agate.Table.from_csv(ky_all_contributions_file, delimiter='|')
cmte_list = agate.Table.from_csv(cmte_list_file, delimiter='|')

current_candidate_cmte_ids = ['C00580100', 'C00577130', 'C00581876', 'C00575795', 'C00574624']
    #Trump, Donald J. = C00580100
    #Sanders, Bernard = C00577130
    #Kasich, John R. = C00581876
    #Clinton, Hillary Rodham = C00575795
    #Cruz, Rafael Edward 'Ted' = C00574624


def print_state():
  
  generated_js.write('state = "Kentucky"')
  
def print_updated():

  generated_js.write('updated = "' + time.strftime("%x") + '"\n')
  #print 'updated = "' + time.strftime("%x") + '"'

def print_ky_overall_summary():
       
    # How much money has been donated by Kentuckians to the 2016 presidential race?
    ky_contrib_sum = ky_all_contributions.aggregate(agate.Sum('TRANSACTION_AMT'))
    # How many contributions have Kentuckians made to the presidential race?
    ky_contrib_count = ky_all_contributions.aggregate(agate.Count())
    
    print(str(ky_contrib_count) + ' donations, totaling $' + str(ky_contrib_sum) + ' have been donated by Kentuckians to the 2016 presidential race.')
    
    generated_js.write('total_donated_sum = ' + str(ky_contrib_sum) + '\ntotal_donated_count = ' + str(ky_contrib_count) + '\n')

    

def print_ky_candidate_summary():
    
    # How much money has been donated by Kentuckians to the presidential candidates?
    ky_candidate_sum = ky_candidate_contributions.aggregate(agate.Sum('contb_receipt_amt'))
    # How many contributions have Kentuckians made to presidential candidates?
    ky_candidate_count = ky_candidate_contributions.aggregate(agate.Count())
    
    print(str(ky_candidate_count) + ' donations, totaling $' + str(ky_candidate_sum) + ' have been donated by Kentuckians specifically to the 2016 presidential candidates.')
        
    generated_js.write('total_candidate_donated_sum = ' + str(ky_candidate_sum) + '\ntotal_candidate_donated_count = ' + str(ky_candidate_count) + '\n')

# How much money has been donated by Kentuckians to the current 2016 presidential candidates?
def print_ky_current_candidate_sum():
    current_cand_ky_contrib = ky_candidate_contributions.where(
        lambda r: r['cmte_id'] in current_candidate_cmte_ids
    )
    
    ky_current_candidate_count = current_cand_ky_contrib.aggregate(agate.Count())
    ky_current_candidate_sum = current_cand_ky_contrib.aggregate(agate.Sum('contb_receipt_amt'))
    current_candidate_count = len(current_candidate_cmte_ids)
    
    print('There are currently ' + str(current_candidate_count) + ' candidates running for president. Those ' + str(current_candidate_count) + ' candidates have received ' + str(ky_current_candidate_count) + ' donations totaling $' + str(ky_current_candidate_sum))
    
    
    

# Which committees are Republican and which are Democratic? This will come from 
# cm16.csv file.
# How much money has been donated by Kentuckians to Democratic candidate committees? Republican candidate committees?
def print_contributions_by_cmte_type():
    #republican_type = ['REP']
    #democrate_type = ['DEM']
    #
    ## Creating lists of republican and democratic cmte_ids
    #rep_cmte_list = cmte_list.where(
    #    lambda r: r['CMTE_PTY_AFFILIATION'] in republican_type
    #)
    #dem_cmte_list = cmte_list.where(
    #    lambda r: r['CMTE_PTY_AFFILIATION'] in democrate_type
    #)
    #rep_cmte_id_list = []
    #for row in rep_cmte_list.rows:
    #    rep_cmte_id_list.append(row['CMTE_ID'])
    #dem_cmte_id_list = []
    #for row in dem_cmte_list.rows:
    #    dem_cmte_id_list.append(row['CMTE_ID'])
    rep_cmte_id_list = [
        'C00579458', 'C00573519', 'C00580399', 'C00574624', 'C00577312', 
        'C00578757', 'C00577981', 'C00581876', 'C00575449', 'C00458844', 
        'C00578492', 'C00580100', 'C00580480'
    ]
    # Jeb Bush = C00579458
    # Carson = C00573519
    # Christie = C00580399
    # Cruz = C00574624
    # Fiorino = C00577312
    # Graham = C00578757
    # Huckabee = C00577981
    # Kasich = C00581876
    # Paul = C00575449
    # Rubio = C00458844
    # Santorum = C00578492
    # Trump = C00580100
    # Walker = C00580480
    
    
    dem_cmte_id_list = ['C00575795', 'C00583146', 'C00578658', 'C00577130', 'C00581215']
    # Clinton = C00575795
    # Lessig = C00583146
    # OMalley = C00578658
    # Sanders = C00577130
    # Webb = C00581215
    
    # Run through all the individual contributions and pull out the ones made
    # to republican committees and then those made to democratic committees.

    rep_contributions = ky_candidate_contributions.where(
        lambda r: r['cmte_id'] in rep_cmte_id_list
    )
    dem_contributions = ky_candidate_contributions.where(
        lambda r: r['cmte_id'] in dem_cmte_id_list
    )
    
    rep_contrib_count = rep_contributions.aggregate(agate.Count())
    rep_contrib_sum = rep_contributions.aggregate(agate.Sum('contb_receipt_amt'))
    print(str(rep_contrib_count) + ' contributions to Republican committees, totaling $' + str(rep_contrib_sum))
    generated_js.write('to_republicans = ' + str(rep_contrib_sum) + '\n')
    
    
    dem_contrib_count = dem_contributions.aggregate(agate.Count())    
    dem_contrib_sum = dem_contributions.aggregate(agate.Sum('contb_receipt_amt'))
    print(str(dem_contrib_count) + ' contributions to Democratic committees, totaling $' + str(dem_contrib_sum))
    generated_js.write('to_democrats = ' + str(dem_contrib_sum) + '\n')
        


# How much money has been donated to each presidential candidate from Kentuckians?
# How many donations did each presidential candidate receive from Kentuckians?
# Who were the top candidate KY donors, by amount donated?
def ky_by_candidate():
    
    generated_js.write('candidate_contributions = [')
    
    
    current_cand_ky_contrib = ky_candidate_contributions.where(
        lambda r: r['cmte_id'] in current_candidate_cmte_ids
    )
    current_candidate_groups = current_cand_ky_contrib.group_by('cand_nm')
    current_candidate_totals = current_candidate_groups.aggregate([
        ('contributions_count', agate.Count()),
        ('contributions_sum', agate.Sum('contb_receipt_amt'))
    ])
    sorted_current_candidate_totals = current_candidate_totals.order_by('contributions_sum', reverse=True)
    for row in sorted_current_candidate_totals.rows:
      generated_js.write('{name: "' + row[0] + '", count: ' + str(row[1]) + ', sum: ' + str(row[2]) + ', status: "current"},')


    dropped_cand_ky_contrib = ky_candidate_contributions.where(
        lambda r: r['cmte_id'] not in current_candidate_cmte_ids
    )
    dropped_candidate_groups = dropped_cand_ky_contrib.group_by('cand_nm')        
    dropped_candidate_totals = dropped_candidate_groups.aggregate([
        ('contributions_count', agate.Count()),
        ('contributions_sum', agate.Sum('contb_receipt_amt'))
    ])
    sorted_dropped_candidate_totals = dropped_candidate_totals.order_by('contributions_sum', reverse=True)    
    filtered_dropped_candidate_totals = sorted_dropped_candidate_totals.where(
        lambda r: r['contributions_sum'] > 25000
    )
    for row in filtered_dropped_candidate_totals.rows:
      generated_js.write('{name: "' + row[0] + '", count: ' + str(row[1]) + ', sum: ' + str(row[2]) + ', status: "dropped"},')
    
    
    generated_js.write(']\n')
    

def candidate_time_charts():
    os.remove('app/data/candidate_charts.js')
    text_type = agate.Text()
    datetime_type = agate.DateTime()
    chart_js = open('app/data/candidate_charts.js', 'a')
            
    candidate_contribs_with_monthyear = ky_candidate_contributions.compute([
        ('month_year', agate.Formula(text_type, lambda r: r['contb_receipt_dt'][-6:])),
        ('date', agate.Formula(text_type, lambda r: datetime.datetime.strptime(r['contb_receipt_dt'], '%d-%b-%y')))
    ])

    
    date_sorted_candidat_contribs = candidate_contribs_with_monthyear.order_by('date')
    restricted_date_candidate_contribs = date_sorted_candidat_contribs.where(
        lambda r: r['date'] > '2015-02-28 00:00:00'
    )
    
    by_candidate_contribs = candidate_contribs_with_monthyear.group_by('cand_nm')
    
    
    # We need a list of unique candidates and a list of unique month_years
    # Then we need to say, for each month_year and each candidate, how many contributions
    # happened. 
    # We only need to write one label variable for all candidates:
    # labels = ['FEB-15', 'MAR-15', etc...]
    # For each candidate, we need:
    # candidateName_series = [200, 34, 885, 123, etc...]
    
    # Get unique list of month_years.
    # These are our labels. 
    # We'll have to figure out how to sort these
    month_years = []
    for row in restricted_date_candidate_contribs.rows:
        month_year = row['month_year']
        if month_year in month_years:
            pass
        else:
            month_years.append(str(month_year))
    
    
    # Get unique list of candidates
    candidates = []
    for row in candidate_contribs_with_monthyear.rows:
        candidate = row['cand_nm']
        if candidate in candidates:
            pass
        else:
            candidates.append(candidate)
            
    
    candidate_month_year_groups = by_candidate_contribs.group_by(
        lambda r: r['month_year'],
        key_name='month_year_group'
    )
    
    month_year_counts = candidate_month_year_groups.aggregate([
        ('contribution_count', agate.Count()),
        ('contribution_sum', agate.Sum('contb_receipt_amt'))
    ])
    
    #month_year_counts.print_table(max_rows=200)
    
    chart_js.write('count_labels = ' + str(month_years) + '\n')     
            
    # For each candidate, each month, we want one value for count and one value for sum
    # If these values cannot be found in the month_year_counts table, then we should record a 0
    for candidate in candidates:
        count_value_list = []
        sum_value_list = []
        
        for month in month_years:
            contrib_count = 0
            contrib_sum = 0
            for row in month_year_counts.rows:
                if row['cand_nm'] == candidate:
                    
                    series_label = candidate.split(',')[0].lower()
                    if month == row['month_year_group']:
                        contrib_count = str(row['contribution_count'])
                        #contrib_count = '{:,f}'.format(row['contribution_count'])
                        contrib_count_dict = {}
                        contrib_count_dict['meta'] = str('Contributions to ' + candidate + ' for ' + month)
                        contrib_count_dict['value'] = contrib_count
                        count_value_list.append(dict(contrib_count_dict))
                        
                        contrib_sum = str(row['contribution_sum'])
                        #contrib_sum = '${:,.2f}'.format(row['contribution_sum'])
                        contrib_sum_dict = {}
                        contrib_sum_dict['meta'] = str('Amt. contributed to ' + candidate + ' for ' + month)
                        contrib_sum_dict['value'] = contrib_sum
                        sum_value_list.append(dict(contrib_sum_dict))
                    else:
                        pass
            if contrib_count == 0:
                contrib_count_dict = {}
                contrib_count_dict['meta'] = str('Contributions to ' + candidate + ' for ' + month)
                contrib_count_dict['value'] = '0'
                count_value_list.append(dict(contrib_count_dict))
            if contrib_sum == 0:
                contrib_sum_dict = {}
                contrib_sum_dict['meta'] = str('Amount contributed to ' + candidate + ' for ' + month)
                contrib_sum_dict['value'] = '0'
                sum_value_list.append(dict(contrib_sum_dict))

        chart_js.write(series_label + '_count_series = ' + str(count_value_list) + '\n')
        chart_js.write(series_label + '_sum_series = ' + str(sum_value_list) + '\n')

    chart_js.close()
    
        


# Who were the top candidate KY donors, by amount donated?
def top_ky_donors_candidates():
    contributor_groups = ky_candidate_contributions.group_by('contbr_nm')
    
    contributor_totals = contributor_groups.aggregate([
        ('contributions_count', agate.Count()),
        ('contributions_sum', agate.Sum('contb_receipt_amt'))
    ])
    sorted_contributor_totals = contributor_totals.order_by('contributions_sum', reverse=True)
    
    sorted_contributor_totals.print_table()
    
    generated_js.write('top_donors_to_candidates = [')
    for row in itertools.islice(sorted_contributor_totals.rows,0,5):
      generated_js.write('{name: "' + row[0] + '", count: ' + str(row[1]) + ', sum: ' + str(row[2]) + '},')
    generated_js.write(']\n')
    
    
# Who were the top PAC KY donors, by amount donated?
def top_ky_donors_pac():
    contributor_groups = ky_all_contributions.group_by('NAME')
    
    contributor_totals = contributor_groups.aggregate([
        ('contributions_count', agate.Count()),
        ('contributions_sum', agate.Sum('TRANSACTION_AMT'))
    ])
    sorted_contributor_totals = contributor_totals.order_by('contributions_sum', reverse=True)
    
    sorted_contributor_totals.print_table()
    
    generated_js.write('top_donors_to_pacs = [')
    for row in itertools.islice(sorted_contributor_totals.rows,0,5):
      generated_js.write('{name: "' + row[0] + '", count: ' + str(row[1]) + ', sum: ' + str(row[2]) + '},')
    generated_js.write(']\n')
    

os.remove('app/data/ky_totals.js')
generated_js = open('app/data/ky_totals.js', 'a')
candidate_time_charts()
top_ky_donors_pac()  
top_ky_donors_candidates()
ky_by_candidate()
print_contributions_by_cmte_type()
print_ky_candidate_summary()
print_ky_overall_summary()
print_updated()
print_state()
generated_js.close()