from __future__ import absolute_import, print_function

import sys

from weatherlink.importer import Importer
from weatherlink.utils import calculate_all_record_values

import functools
import operator
from datetime import datetime
import pandas as pd
pd.options.display.max_columns = 500
pd.options.display.max_rows = 500

importer = Importer(sys.argv[1])

print('Reading file %s' % importer.file_name)
print('Year %s' % importer.year)
print('Month %s' % importer.month)
print()

importer.import_data()

all_values = []
for day, day_index in enumerate(importer.header.day_indexes):
	if day > 0 and day_index.record_count > 0:
		print('Day %s (%s records, offset %s):' % (day, day_index.record_count, day_index.start_index))
		print('-' * 250)

		summary = importer.daily_summaries[day]
		output = ''
		for item in summary.DAILY_SUMMARY_ATTRIBUTE_MAP:
			if item[0][-8:] != '_version':
				output += str(summary[item[0]] or '-') + '  '
		print(f'summary -> {output}')
		print('-' * 250)

		assert day_index.record_count - 2 == len(importer.daily_records[day])


		for record in importer.daily_records[day]:
			values = calculate_all_record_values(record)
			output = str(record.date) + '  (' + str(record.timestamp) + ')  '
			for item in record.RECORD_ATTRIBUTE_MAP_WLK:
				if item[0] != '__special' and item[0][-8:] != '_version':
					output += str(record[item[0]] or '-') + '  '
					if item[0].startswith("wind_direction"):
						if record[item[0]]:
							values[f"{item[0]}_degrees"] = record[item[0]].degrees
							values[f"{item[0]}"] = record[item[0]]
						else:
							values[f"{item[0]}_degrees"] = None
							values[f"{item[0]}"] = None
					else:
						values[item[0]] = record[item[0]] or None
			output += str(record.rain_amount) + '  ' + str(record.rain_rate) + '  '
			values['datetime'] = str(record.date)
			all_values.append(values)
			# print(values)
			print(f'values -> {output}')

		# print(importer.daily_records)
		# print(type(importer.daily_records))

df = pd.DataFrame(all_values)

print(df.dtypes)

df['date'] = df.datetime.str.slice(start=0, stop=10)
# print(df.head())
df = df[df.datetime.str.slice(start=0, stop=10) == '2020-08-29']

print(df.T)
