
from bs4 import BeautifulSoup
from pathlib import Path
import codecs
import csv
import html.parser
import os.path
import sys

def main():
	fileok = True
	if len(sys.argv) == 2:
		path = sys.argv[1]
		if os.path.isfile(path):
			history_to_csv(path)
		else:
			fileok = False
	else:
		fileok = False
	if not fileok:
		error_exit()

def error_exit():
	print('Pas de fichier HTML indiqué ou fichier invalide.')
	exit()

def history_to_csv(path):
	file = codecs.open(path, encoding='utf-8')
	content = file.read()
	file.close()
	soup = BeautifulSoup(content, 'html.parser')
	tbody = soup.find('tbody')
	rows = [['Date', 'Lieu', 'Type d\'accompagnement', 'Nb personnes', 'Activités', 'Notes']]
	for tr in tbody.find_all('tr'):
		cells = tr.find_all('td')
		if len(cells) < 7:
			error_exit()
		# THIS IS HIGHLY DEPENDENT ON CURRENT PAGE BEHAVIOR, PLEASE CHANGE IF NECESSARY
		date = cells[0].string
		place = cells[2].string
		acc_type = cells[3].find('img').get('alt')
		nb_acc = cells[4].string
		activities = ';'.join([x.get('alt') for x in cells[5].find_all('img')])
		notes = cells[6].string
		rows.append([date, place, acc_type, nb_acc, html.unescape(activities), notes])
	if len(tbody.find_all('tr')) == 0:
		error_exit()

	outpath = Path(path)
	with open(outpath.with_suffix('.csv'), 'w', newline='') as file:
	    writer = csv.writer(file, delimiter='\t')
	    writer.writerows(rows)



if __name__ == '__main__':
	main()