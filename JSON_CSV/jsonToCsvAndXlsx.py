import json
import csv
import os
from pathlib import Path
import pandas as pd

for file in Path("JSONS").glob('*.json'):
	with open("JSONS/" + file.name, encoding='utf-8-sig') as json_file:
		jsondata = json.load(json_file)['objects']

	print(file.name)

	if not os.path.exists("CSV"):
		os.makedirs("CSV")
	data_file = open("CSV/" + file.name[:-5] + '.csv', 'w', newline='', encoding='utf-8-sig')
	csv_writer = csv.writer(data_file)

	count = 0
	for data in jsondata:
		if count == 0:
			header = ["WhoTalk", "Line_Rus", "Line_Eng", "Line_Esp", "Line_Ukr", "Line_Deu", "Line_Pl", "Tags", "Expressions", "OnEnd"]
			csv_writer.writerow(header)
			count += 1

		values = []
		for columTitle in header:
			v = ""
			if columTitle in data:
				v = data[columTitle]
			values.append(v)
		csv_writer.writerow(values)

	data_file.close()

	# Reading the csv file
	df_new = pd.read_csv("CSV/" + file.name[:-5] + '.csv')


	if not os.path.exists("XLSX"):
		os.makedirs("XLSX")
	# saving xlsx file
	GFG = pd.ExcelWriter("XLSX/" + file.name[:-5] + '.xlsx')
	df_new.to_excel(GFG, sheet_name="objects", index=False)
	GFG.save()

