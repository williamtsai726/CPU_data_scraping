import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import numpy as np

from googletrans import Translator

# Create a Translator object
def translate (text):
  translator = Translator()

  # Detect the language of the text
  detected_language = translator.detect(text).lang

  # Translate the text to English
  translated_text = translator.translate(text, src=detected_language, dest='en')
  return translated_text

# method for converting time format
def date_convert (date):
  # Define the format of the input string
  input_format = '%d.%m.%Y'

  # Parse the input string into a datetime object
  date = datetime.strptime(date, input_format).strftime('%d %B %Y')

  # Format the datetime object to display day, month, and year
  return date

# method for grabing the header infomation
def info (website):
  trList = website.find('table')
  category = []
  data = []

  for row in trList.find_all('tr')[1:]:
    cells = row.find_all('td')
    if len(cells) == 2:  # Ensure there are at least two cells in the row
      category.append(translate(cells[0].text.strip()).text)
      data.append(translate(cells[1].text.strip()).text)

  return category, data

# find all benchmark
def benchmark(website):
  arr = []
  for i in website.find_all('div', class_ = 'chart chart--bar js-chart nojs-block'):
    arr.append(i.get('id'))
  unique = list(set(arr))
  return unique


# find all computer examined
def computer (info):
  arr = []
  for i in info.find_all('div', class_='chart__item'):
    arr.append(i.text)
  return arr

# the rating of the benchmark
def value (info):
  arr = []
  for i in info.find_all('div', class_ = 'chart__label'):
    arr.append(i.get('data-value'))
  return arr

def columnWidth(maps):
  max = 0
  max_index = 0
  count = 0
  for map in maps:
    if len(map) > max:
      max = len(map)
      max_index = count
    count += 1
  return max_index

url = "https://www.computerbase.de/2023-12/intel-meteor-lake-core-ultra-7-155h-test/"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser',from_encoding='utf-8')

# grab all the header information and put them onto one dataframe
website = soup.find('meta', attrs={'name':"application-name"}).get('content')
title = soup.find('h1').text.strip()
author = soup.find('span', class_='article-view__authors').find('span').text.strip()
date = date_convert(soup.find('time', class_='article-view__date').text.split(' ')[0])
data_collected_by = soup.find('div', class_='article-view__overline').text.split('\n')[6]
category, data = info(soup)

stat = {'Column A': ['website', 'url', 'title', 'author', 'date', 'data collected by'] + category,
        'Column B': [website, url, title, author, date, data_collected_by] + data}
df = pd.DataFrame(stat)
df.replace({' ': 'NA', np.nan: 'NA', '': 'NA', '?': 'NA'}, inplace=True)

Benchmark = benchmark(soup)

#put rating, computer into dictionary based on benchmark
maps = []
for mark in Benchmark:
  comp = computer(soup.find('div', id = mark))
  data = value(soup.find('div', id = mark))
  map = dict(zip(comp,data))
  maps.append(map)


# create the columns of the dataframe
index = columnWidth(maps)
laptop = computer(soup.find('div', id = Benchmark[index]))
laptop = list(set(laptop))
df2 = pd.DataFrame(columns=['Benchmark'] + laptop)

# fill in the dataframe
map = 0
for mark in Benchmark:
  row = {'Benchmark' : mark[9:]}
  for comp in laptop:
    row.update({comp:maps[map].get(comp)})
  map += 1
  df2.loc[len(df2)] = row
df2.replace({' ': 'NA', np.nan: 'NA', '': 'NA', '?': 'NA', 'None':'NA'}, inplace=True)


# concatenate the two dataframe and export as excel
result_df = pd.concat([df, df2], axis=1)
result_df.to_excel('benchmark3.xlsx', index=False)

