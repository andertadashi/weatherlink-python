from __future__ import absolute_import, print_function

import sys

from weatherlink.importer import Importer
from weatherlink.utils import calculate_all_record_values

import functools
import operator

import pandas as pd
pd.options.display.max_columns = 500
pd.options.display.max_rows = 500

importer = Importer(sys.argv[1])

print('Reading file %s' % importer.file_name)
print('Year %s' % importer.year)
print('Month %s' % importer.month)
print()

importer.import_data()

for day, day_index in enumerate(importer.header.day_indexes):
	if day > 0 and day_index.record_count > 0:
		print('Day %s (%s records, offset %s):' % (day, day_index.record_count, day_index.start_index))
		print('-' * 250)

		summary = importer.daily_summaries[day]
		output = ''
		for item in summary.DAILY_SUMMARY_ATTRIBUTE_MAP:
			if item[0][-8:] != '_version':
				output += str(summary[item[0]] or '-') + '  '
		print(output)
		print('-' * 250)

		assert day_index.record_count - 2 == len(importer.daily_records[day])

		all_values = []
		for record in importer.daily_records[day]:
			values = calculate_all_record_values(record)
			output = str(record.date) + '  (' + str(record.timestamp) + ')  '
			for item in record.RECORD_ATTRIBUTE_MAP_WLK:
				if item[0] != '__special' and item[0][-8:] != '_version':
					output += str(record[item[0]] or '-') + '  '
					if item[0].startswith("wind_direction"):
						print(record[item[0]].degrees)
					values[item[0]] = record[item[0]] or None
			output += str(record.rain_amount) + '  ' + str(record.rain_rate) + '  '
			values['datetime'] = str(record.date)
			all_values.append(values)
			print(output)

		# print(importer.daily_records)
		# print(type(importer.daily_records))

		df = pd.DataFrame(all_values)
		print(df.wind_direction_prevailing)
		df['wind_direction_prevailing_value'] = df.wind_direction_prevailing.apply(lambda r: r.degrees if r else None)
		df['wind_direction_speed_high_value'] = df.wind_direction_speed_high.apply(lambda r: r.degrees if r else None)


		print(df.head().T)

