# 2016-campaign-finance
Scripts to pull *individual state* campaign finance data and process for display online.

Run the files in this order:
1. `python scrape.py`
2. `python segment.py`
3. `python analyze.py`

## scrape.py
NOTE: This script clears out your data folder before it starts pulling down new FEC files. If you want/need to keep your old FEC data files, move them elsewhere before you run `scrape.py`.

This script scrapes data from the FEC. Before running this file, make sure you create a data directory in the main project folder. The data directory has been gitignored here because who wants to store all that FEC data on the github? Not I.

This script currently scrapes 3 files:
- [State-based contributions](http://www.fec.gov/disclosurep/PDownload.do) to presidential candidates
- [Contributions by individuals](http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml) to all PACs, presidential and otherwise
- [List of committees](http://www.fec.gov/finance/disclosure/metadata/DataDictionaryCommitteeMaster.shtml)

## segment.py
Making queries on indiv16 data file takes forever. `segment.py` segments that file by an individual state so that they process of querying goes much more quickly.

## analyze.py
`analyze.py` answers a variety of campaign-finance-related questions, then writes those answers as json objects to javascript files. These javascript files are then used by the "app" to present state-based, campaign-finance data in a mildly interactive way.

This document contains functions that are not currently used in the app. Some were created to quickly answer questions I had of the data. This file is well documented. I encourage you to go through it, see what it does, and implement additional features if you choose to.

Known issues: 
- An attempt to discern party-affiliation from the FEC committees download showed that many committees, including presidential PACs, failed to list a party. You can see this in the `print_contributions_by_cmte_type()` function. This is problematic if you're trying to determine how much $$ was contributed to Democratic committees and how much to Republican. Since we switched to a much more candidate-centric way of analyzing the campaign contributions, we were simply able to create a list of candidates and their affiliations. It would be nice to be able to query all contributions though... candidate and otherwise.
