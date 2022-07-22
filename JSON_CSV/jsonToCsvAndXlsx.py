import json
import csv
import math
import os
from pathlib import Path
import pandas as pd

def JSONS_TO_CSV_and_XLSX():
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

def XLSX_TO_JSONS_and_CSV():
	for file in Path("XLSX").glob('*.xlsx'):

		print(file.name)

		try:
			x = pd.read_excel("XLSX/" + file.name, sheet_name="objects")
		except:
			x = pd.read_excel("XLSX/" + file.name, sheet_name="Лист1")
		x.fillna("", inplace=True)
		if not os.path.exists("CSV"):
			os.makedirs("CSV")
		x.to_csv("CSV/" + file.name[:-5] + '.csv', index=False)



		count = 0

		headers = ["WhoTalk", "Line_Rus", "Line_Eng", #"Line_Esp", "Line_Ukr", "Line_Deu", "Line_Pl",
				   "Tags", "Expressions", "OnEnd"]
		data = {"objects":[]}
		for i in range(len(x)):
			values = {}
			for columTitle in headers:
				if columTitle in x:
					values[columTitle] = x.loc[i][columTitle]
			data["objects"].append(values)

		# Serializing json
		json_object = json.dumps(data, indent=4, ensure_ascii=False)

		# Writing to sample.json
		with open("JSONS/" + file.name[:-5]+".json", "w", encoding="utf-8") as outfile:
			outfile.write(json_object)

XLSX_TO_JSONS_and_CSV()
