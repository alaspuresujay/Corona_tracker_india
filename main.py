# importing libraries

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import os
import numpy as np
import matplotlib.pyplot as plt



extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
URL = 'https://www.mohfw.gov.in/'

SHORT_HEADERS = ['SNo', 'State','Indian-Confirmed',
				'Foreign-Confirmed','Cured','Death']

response = requests.get(URL).content
soup = BeautifulSoup(response, 'html.parser')
header = extract_contents(soup.tr.find_all('th'))

stats = []
all_rows = soup.find_all('tr')

for row in all_rows:
	stat = extract_contents(row.find_all('td'))
	if stat:
		if len(stat) == 5:
			# last row
			stat = ['', *stat]
			stats.append(stat)
		elif len(stat) == 6:
			stats.append(stat)

stats[-1][1] = "Total Cases"
table1 = tabulate(stats,headers=SHORT_HEADERS)
total = stats[-1]
# print(table1)
# stats.remove(stats[-1])
objects = []
for row in stats:
	objects.append(row[1])

y_pos = np.arange(len(objects)+1)

performance = []
for row in stats:
	performance.append(int(row[2].strip('#')) + int(row[3]))

table = tabulate(stats, headers=SHORT_HEADERS)
print(table)
fig, ax = plt.subplots(figsize=(10, 8))

ax.barh(objects, performance, align='center', alpha=0.5,
		color=(234 / 256.0, 128 / 256.0, 252 / 256.0),
		edgecolor=(106 / 256.0, 27 / 256.0, 154 / 256.0))

ax.set_yticks(y_pos, objects)
ax.set_xlim(1, 140)
ax.set_xlabel('Number of Cases\nDeveloped by Sujay - alaspuresujay.github.io')
ax.set_title('Corona Virus Cases in India')
fig.suptitle('Corona Tracker India', fontsize=16)
plt.annotate((str(performance[-1])+"    Death-" + str(total[-1])), xy=(100, y_pos[27]), xytext=(10, 0),
             # Horizontally shift label by `space`
             textcoords="offset points",  # Interpret `xytext` as offset in points
             va='center',  # Vertically center label
             color='black',
             ha='right')
for i in range(len(objects)):
	if performance[i] < 10:
		space = 10
		ext = 50
	else:
		space = -1
		ext = 50
	if performance[i]>129:
		ext=-40
	plt.annotate((str(performance[i])), xy=(performance[i], y_pos[i]), xytext=(space, 0),
				 # Horizontally shift label by `space`
				 textcoords="offset points",  # Interpret `xytext` as offset in points
				 va='center',  # Vertically center label
				 color='black',
				 ha='right')
	plt.annotate(("Death-" + str(stats[i][5])), xy=(performance[i], y_pos[i]), xytext=(space+ext, 0),
				 # Horizontally shift label by `space`
				 textcoords="offset points",  # Interpret `xytext` as offset in points
				 va='center',  # Vertically center label
				 color='red',
				 ha='right')
plt.show()