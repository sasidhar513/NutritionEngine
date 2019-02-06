import csv

	with open(fileName, mode='rt') as f, open('sorted'+fileName, 'w') as final:
		writer = csv.writer(final, delimiter='^')
		reader = csv.reader(f, delimiter='^')
		_ = next(reader)
		sorted1 = sorted(reader, key=lambda row: str(row[0]))
		#sorted2 = sorted(sorted1, key=lambda row: int(row[2]))
		for row in sorted1:
			writer.writerow(row)