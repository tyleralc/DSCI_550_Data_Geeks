import pandas as pd
from bs4 import BeautifulSoup
import requests
import math
from googlesearch import search

#get first 3 unique journals from first page
def pubmed_journals(url):
    journals = []
    content = requests.get(url)
    soup = BeautifulSoup(content.content, 'html.parser')
    for link in soup.find_all('span', {'class': 'docsum-journal-citation short-journal-citation'}):
        entry = link.get_text().split('.')[0]
        if entry not in journals:
            journals.append(entry)
    return journals[0:3]

#output total publications
def pubmed_results(url):
    pub = ''
    content = requests.get(url)
    soup = BeautifulSoup(content.content, 'html.parser')
    for link in soup.find_all('meta', {'name': 'log_resultcount'}):
        pub = link['content']
    return pub

#output years paper were published
def pubmed_year(url):
    year = []
    content = requests.get(url)
    soup = BeautifulSoup(content.content, 'html.parser')
    for link in soup.find_all('span', {'class': 'docsum-journal-citation short-journal-citation'}):
        if link.get_text()[0:4].isdigit() == True:
            year.append(link.get_text()[0:4])
       # elif link.get_text()[0:4] == '':
        #    return year
        elif link.get_text()[-5:-1].isdigit() == True:
            year.append(link.get_text()[-5:-1])
    return year

#add other journals to df
def upload_journal(df, all_authors):
    other_journals = []
    for i in range(len(all_authors)):
      temp_authors = all_authors[i].split(', ')
      pub_journals = []
      for j in range(len(temp_authors)):
        temp_journals = []
        link = 'https://pubmed.ncbi.nlm.nih.gov/?term='
        for k in range(len(temp_authors[j].split(' '))):
          link = link + temp_authors[j].split(' ')[k] + '%20'
        link = link[:-3]
        temp_journals = pubmed_journals(link)
        pub_journals.append(temp_journals)
      other_journals.append(pub_journals)
      print(i)
    df['Other Journals'] = other_journals
    return df

def upload_rate_duration(df, all_authors):
    duration_career = []
    pub_rate = []
    i = 0
    for i in range(len(all_authors)):
      temp_authors = all_authors[i].split(', ')
      dur = []
      rate = []
      for j in range(len(temp_authors)):
        pub_year = []
        temp_journals = []
        link = 'https://pubmed.ncbi.nlm.nih.gov/?term='
        for k in range(len(temp_authors[j].split(' '))):
          link = link + temp_authors[j].split(' ')[k] + '%20'
        link = link[:-3]
        pub_year = pubmed_year(link)
        pub_num = pubmed_results(link)
        if pub_num == '':
          pub_num = 1
        if int(pub_num) > 200:
          pub_num = 200
        for k in range(1,math.ceil(float(pub_num)/10)):
          page_link = link + '&page=' + str(k+1)
          pub_year = pub_year + pubmed_year(page_link)
        if len(pub_year) == 0:
          dur = -1
          temp_rate = -1
        else:
          dur = float(max(pub_year)) - float(min(pub_year)) + 1
          temp_rate = round(float(pub_num)/dur,2)
        if j == 0:
          duration_career.append(dur)
        rate.append(temp_rate)
      pub_rate.append(rate)
      print(i)
    df['Publication Rate'] = pub_rate
    df['Duration of Career'] = duration_career
    return df

def affiliated_univ(DOI):
  try:
    response = requests.get('https://journals.plos.org/plosone/article/authors?id='+str(DOI))
    soup = BeautifulSoup(response.content, 'html.parser')
    affiliation=soup.find("meta",{"name":"citation_author_institution"})
    return affiliation['content']
  except:
    response = requests.get('https://pubmed.ncbi.nlm.nih.gov/?term='+str(DOI))
    soup = BeautifulSoup(response.content, 'html.parser')
    soup.find_all('li', {"data-affiliation-id": "affiliation-1"})

    for text in soup.find_all('li', {"data-affiliation-id": "affiliation-1"}):
      affiliation=text.text[2:]
      break
    return affiliation

def upload_affiliated_univ(df, journal_link):
    affiliation_list=[]
    for doi in journal_link:
        print(doi)
        if affiliated_univ(doi) is None:
            affiliation_list.append('-1')
        else:
            affiliation_list.append(affiliated_univ(doi))
    df['Affiliation University'] = affiliation_list
    return df

def get_highest_degree(author_name, degrees):
    link = ''
    query = author_name + ' Research Gate'
    for k in search(query, stop=1):
        if 'https://www.researchgate.net/profile/' in k:
            link = k
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')
            print(soup.find_all('title'))
            if len(soup.find_all('title')) == 0:
                return -1
            listofattributes = soup.find_all('title')[0].getText().split('|')
            for word in listofattributes:
                if word.strip().lower() in degrees:
                    return word.strip()
                if 'phd' in word.strip().lower():
                    return 'PhD'
    return -1

def upload_highest_degree(df, all_authors, degrees):
    author_list = [x.split(',')[0] for x in all_authors]
    highest_degree = []
    for author_name in author_list:
        degree = get_highest_degree(author_name, degrees)
        # print((author_name, degree)) 
        highest_degree.append(degree)
    df['Highest Degree'] = highest_degree
    return df

def get_degree_area(author_name):
    link = ''
    query = author_name + ' Research Gate'
    for k in search(query, stop=1):
        if 'https://www.researchgate.net/profile/' in k:
            link = k
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')
            if len(soup.find_all('title')) == 0:
                return -1
            listofattributes = soup.find_all('title')[0].getText().split('|')
            for word in listofattributes:
                if 'department of' in word.strip().lower():
                    return word.split('of')[1].strip()
    return -1

def upload_degree_area(df, all_authors):
    author_list = [x.split(',')[0] for x in all_authors]
    degree_area = []
    for author_name in author_list:
        area = get_degree_area(author_name)
        #print((author_name, area))
        degree_area.append(area)
    df['Degree Area'] = degree_area
    return df

#Function for lab size just using plos one --> keep
def lab_size(DOI):
    response = requests.get('https://journals.plos.org/plosone/article/authors?id='+str(DOI))
    soup = BeautifulSoup(response.content, 'html.parser')
    affiliation=soup.find_all("meta",{"name":"citation_author_institution"})
    univ_list=[]
    for element in affiliation:
        univ_list.append(element['content'])
    for element in univ_list[1:]:
        if element != univ_list[0]:
            univ_list.remove(element)
    return len(univ_list)

def upload_lab_size(df, all_authors, journal_link):
    lab_size_list=[]
    lab_size_list_revised=[]
    for doi in journal_link:
        print(doi)
        try:
            lab_size_list.append(lab_size(doi))
        except:
            lab_size_list.append('N/A')
    for index in range(len(lab_size_list)):
        print(index)
        if lab_size_list[index] != 0:
            lab_size_list_revised.append(lab_size_list[index])
        else:
            author_list = list(all_authors[index].split(','))
            lab_size_list_revised.append(len(author_list))
    df['Lab Size'] = lab_size_list_revised
    print(df)
    return df

#Part 4
#starting dataframe
df = pd.read_csv('Original Bik dataset - papers with endpoint reached.tsv', sep='\t', encoding = 'utf-8')
journal_link = df['DOI']
all_authors = df['Authors'].tolist()
degrees = ['phd', 'dphil', 'doctor of philosophy', 'doctor of engineering', 'doctor', 'ph.d', 'ph.d.', 'dba', 'masters', 'ms', 'msc']


#Functions to add features to df
#df = upload_journal(df, all_authors)
#df = upload_rate_duration(df, all_authors)
#df = upload_affiliated_univ(df, journal_link)
#df = upload_highest_degree(df, all_authors, degrees)
#df = upload_degree_area(df, all_authors)
#df = upload_lab_size(df, all_authors, journal_link)


#Write df onto excel tsv
df.to_csv('test.tsv', sep='\t')

#Part 5
