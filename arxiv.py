#!/usr/bin/env python
# coding: utf-8

# Todo: Make a commandline tool which can search ArXiv for a particular keyword released in the past week and download the top 5 search results.


import requests
import webbrowser 
import datetime
import sys
import bs4
import re


'''This part processes the search terms typed by the user '''
searchterms= sys.argv[1:]
searchstring=''

for word in searchterms:
    if(searchstring == ''):
        searchstring=word
    else:    
        searchstring=searchstring+'+'+ str(word)

        
''' This part finds out todays date and the date a week ago'''
today=datetime.date.today() # this is the date only in the YYYY-MM-DD format
week_ago = today-datetime.timedelta(days=30) # this was the date last week

'''This is the search results page. It searches for the search string in the abstracts of Physics > Cond-mat'''
link='https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term='+searchstring+'&terms-0-field=abstract&classification-physics=y&classification-physics_archives=cond-mat&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date='+str(week_ago)+'&date-to_date='+str(today)+'&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first'
webbrowser.open(link) #optional. Can open the search results page in a new tab.

''' requests the webpage from ArXiv'''
res = requests.get(link)
res.raise_for_status()

bs4obj=bs4.BeautifulSoup(res.text,features="lxml") # this is a beautifulsoup object made from the webpage. The parser is lxml.

elems = bs4obj.select('.arxiv-result a') # all objects with an 'a' tag within the result class 

dwldlinkregex=re.compile(r'pdf') #a regular expression which checks if there is 'pdf' in the link
allres=[]

''' This part searches through a list of all hyperlinks and selects only the links to the pdfs. For each result there are multiple links
one for the abstract, one for the pdf and one for each author'''

for i in range(len(elems)):
    ans=elems[i].get('href') # gathering all links
    if(ans): #checking if ans is empty
        match=dwldlinkregex.search(ans) # using regex to only select links with pdf in the name
        if(match): #checking if there is a match
             print('Found a pdf: ' + ans)
             allres.append(ans)


if(len(allres)!=0):
    print ('A total of %d matches were found.' % len(allres))
    print('Do you wish to download the top 5 files? type y/n')
    Ans=input()

    '''This part downloads the top 5 pdfs and stores them in a folder on the desktop.'''
    if(Ans=='y'):
        print("Downloading...")
        for j in range (min(5,len(allres))):
             url=allres[j] +'.pdf'
             req=requests.get(url)
             req.raise_for_status()
             try:
                 with open('/Users/NikhilStuff/Desktop/papers/'+allres[j][22:]+'.pdf',"wb") as pdf: # We are downloading each pdf in chunks
                     for chunk in req.iter_content(chunk_size=1024): 
                         # writing one chunk at a time to pdf file 
                         if chunk: 
                             pdf.write(chunk)
             except:
                 print('There was a problem downloading the files.')
else:
    print('Sorry! No matches found.')





