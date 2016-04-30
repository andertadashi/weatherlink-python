from __future__ import absolute_import

import collections
import datetime
import decimal

"""
It is important that all of the math in this module takes place using decimal precision. Floating-point precision is
far too inaccurate and can cause errors of greater than plus/minus one degree in the results.
"""

ZERO = decimal.Decimal('0')
ONE = decimal.Decimal('1')
TWO = decimal.Decimal('2')
FOUR = decimal.Decimal('4')
FIVE = decimal.Decimal('5')
TEN = decimal.Decimal('10')
ONE_TENTH = decimal.Decimal('0.1')
ONE_HUNDREDTH = ONE_TENTH * ONE_TENTH
ONE_THOUSANDTH = ONE_TENTH * ONE_HUNDREDTH
FIVE_NINTHS = decimal.Decimal('5.0') / decimal.Decimal('9.0')
NINE_FIFTHS = decimal.Decimal('9.0') / decimal.Decimal('5.0')

CELSIUS_CONSTANT = decimal.Decimal('32')
KELVIN_CONSTANT = decimal.Decimal('459.67')
KILOPASCAL_MERCURY_CONSTANT = decimal.Decimal('0.295299830714')
MILLIBAR_MERCURY_CONSTANT = KILOPASCAL_MERCURY_CONSTANT * ONE_TENTH
METERS_PER_SECOND_CONSTANT = decimal.Decimal('0.44704')

# Wet bulb constants used by NOAA/NWS in its wet bulb temperature charts
WB_0_00066 = decimal.Decimal('0.00066')
WB_0_007 = decimal.Decimal('0.007')
WB_0_114 = decimal.Decimal('0.114')
WB_0_117 = decimal.Decimal('0.117')
WB_2_5 = decimal.Decimal('2.5')
WB_6_11 = decimal.Decimal('6.11')
WB_7_5 = decimal.Decimal('7.5')
WB_14_55 = decimal.Decimal('14.55')
WB_15_9 = decimal.Decimal('15.9')
WB_237_7 = decimal.Decimal('237.7')

# Dew point constants used by NOAA/NWS in the August-Roche-Magnus approximation with the Bogel modification
DP_A = decimal.Decimal('6.112')  # millibars
DP_B = decimal.Decimal('17.67')  # no units
DP_C = decimal.Decimal('243.5')  # degrees Celsius
DP_D = decimal.Decimal('234.5')  # degrees Celsius

# Heat index constants used by NOAA/NWS in its heat index tables
HI_SECOND_FORMULA_THRESHOLD = decimal.Decimal('80.0')
HI_0_094 = decimal.Decimal('0.094')
HI_0_5 = decimal.Decimal('0.5')
HI_1_2 = decimal.Decimal('1.2')
HI_61_0 = decimal.Decimal('61.0')
HI_68_0 = decimal.Decimal('68.0')
HI_C1 = decimal.Decimal('-42.379')
HI_C2 = decimal.Decimal('2.04901523')
HI_C3 = decimal.Decimal('10.14333127')
HI_C4 = decimal.Decimal('-0.22475541')
HI_C5 = decimal.Decimal('-0.00683783')
HI_C6 = decimal.Decimal('-0.05481717')
HI_C7 = decimal.Decimal('0.00122874')
HI_C8 = decimal.Decimal('0.00085282')
HI_C9 = decimal.Decimal('-0.00000199')
HI_FIRST_ADJUSTMENT_THRESHOLD = (decimal.Decimal('80.0'), decimal.Decimal('112.0'), decimal.Decimal('13.0'), )
HI_13 = decimal.Decimal('13')
HI_17 = decimal.Decimal('17')
HI_95 = decimal.Decimal('95')
HI_SECOND_ADJUSTMENT_THRESHOLD = (decimal.Decimal('80.0'), decimal.Decimal('87.0'), decimal.Decimal('85.0'), )
HI_85 = decimal.Decimal('85')
HI_87 = decimal.Decimal('87')

# Wind chill constants used by NOAA/NWS in its wind chill tables
WC_C1 = decimal.Decimal('35.74')
WC_C2 = decimal.Decimal('0.6215')
WC_C3 = decimal.Decimal('35.75')
WC_C4 = decimal.Decimal('0.4275')
WC_V_EXP = decimal.Decimal('0.16')

# Constants used by Davis Instruments for its THW calculations
THW_INDEX_CONSTANT = decimal.Decimal('1.072')

# Constants used by the Australian Bureau of Meteorology for its apparent temperature (THSW) calculations
THSW_0_348 = decimal.Decimal('0.348')
THSW_0_70 = decimal.Decimal('0.70')
THSW_4_25 = decimal.Decimal('4.25')
THSW_6_105 = decimal.Decimal('6.105')
THSW_17_27 = decimal.Decimal('17.27')
THSW_237_7 = decimal.Decimal('237.7')

HEAT_INDEX_THRESHOLD = decimal.Decimal('70.0')  # degrees Fahrenheit
WIND_CHILL_THRESHOLD = decimal.Decimal('40.0')  # degrees Fahrenheit
DEGREE_DAYS_THRESHOLD = decimal.Decimal('65.0')  # degrees Fahrenheit


def _as_decimal(value):
	return value if isinstance(value, decimal.Decimal) else decimal.Decimal(value or '0')


def convert_fahrenheit_to_kelvin(temperature):
	return ((temperature + KELVIN_CONSTANT) * FIVE_NINTHS).quantize(ONE_THOUSANDTH)


def convert_kelvin_to_fahrenheit(temperature):
	return ((temperature * NINE_FIFTHS) - KELVIN_CONSTANT).quantize(ONE_THOUSANDTH)


def convert_fahrenheit_to_celsius(temperature):
	return (temperature - CELSIUS_CONSTANT) * FIVE_NINTHS


def convert_celsius_to_fahrenheit(temperature):
	return (temperature * NINE_FIFTHS) + CELSIUS_CONSTANT


def convert_inches_of_mercury_to_kilopascals(barometric_pressure):
	return (barometric_pressure / KILOPASCAL_MERCURY_CONSTANT).quantize(ONE_HUNDREDTH)


def convert_inches_of_mercury_to_millibars(barometric_pressure):
	return (barometric_pressure / MILLIBAR_MERCURY_CONSTANT).quantize(ONE_HUNDREDTH)


def convert_miles_per_hour_to_meters_per_second(wind_speed):
	return wind_speed * METERS_PER_SECOND_CONSTANT


def calculate_wet_bulb_temperature(temperature, relative_humidity, barometric_pressure):
	T = temperature
	RH = _as_decimal(relative_humidity)
	P = convert_inches_of_mercury_to_millibars(barometric_pressure)
	Tdc = (
		T - (WB_14_55 + WB_0_114 * T) * (1 - (ONE_HUNDREDTH * RH)) -
		((WB_2_5 + WB_0_007 * T) * (1 - (ONE_HUNDREDTH * RH))) ** 3 -
		(WB_15_9 + WB_0_117 * T) * (1 - (ONE_HUNDREDTH * RH)) ** 14
	)
	E = WB_6_11 * 10 ** (WB_7_5 * Tdc / (WB_237_7 + Tdc))
	return (
		(((WB_0_00066 * P) * T) + ((4098 * E) / ((Tdc + WB_237_7) ** 2) * Tdc)) /
		((WB_0_00066 * P) + (4098 * E) / ((Tdc + WB_237_7) ** 2))
	).quantize(ONE_TENTH)


def _dew_point_gamma_m(T, RH):
	return (
		RH / 100 * (
			(DP_B - (T / DP_D)) * (T / (DP_C + T))
		).exp()
	).ln()


def calculate_dew_point(temperature, relative_humidity):
	T = convert_fahrenheit_to_celsius(temperature)
	RH = _as_decimal(relative_humidity)
	return convert_celsius_to_fahrenheit(
		(DP_C * _dew_point_gamma_m(T, RH)) / (DP_B - _dew_point_gamma_m(T, RH))
	).quantize(ONE_TENTH)


def _abs(d):
	return max(d, -d)


def calculate_heat_index(temperature, relative_humidity):
	if temperature < HEAT_INDEX_THRESHOLD:
		return None

	T = temperature
	RH = _as_decimal(relative_humidity)

	# Formulas and constants taken from http://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
	heat_index = HI_0_5 * (T + HI_61_0 + ((T - HI_68_0) * HI_1_2) + (RH * HI_0_094))
	heat_index = (heat_index + T) / TWO  # This is the average

	if heat_index < HI_SECOND_FORMULA_THRESHOLD:
		return heat_index.quantize(ONE_TENTH, rounding=decimal.ROUND_UP)

	heat_index = (
		HI_C1 + (HI_C2 * T) + (HI_C3 * RH) + (HI_C4 * T * RH) + (HI_C5 * T * T) +
		(HI_C6 * RH * RH) + (HI_C7 * T * T * RH) + (HI_C8 * T * RH * RH) + (HI_C9 * T * T * RH * RH)
	)

	if (HI_FIRST_ADJUSTMENT_THRESHOLD[0] <= T <= HI_FIRST_ADJUSTMENT_THRESHOLD[1] and
				RH < HI_FIRST_ADJUSTMENT_THRESHOLD[2]):
		heat_index -= (
			((HI_13 - RH) / FOUR) * ((HI_17 - _abs(T - HI_95)) / HI_17).sqrt()
		)
	elif (HI_SECOND_ADJUSTMENT_THRESHOLD[0] <= T <= HI_SECOND_ADJUSTMENT_THRESHOLD[1] and
							RH > HI_SECOND_ADJUSTMENT_THRESHOLD[2]):
		heat_index += (
			((RH - HI_85) / TEN) * ((HI_87 - T) / FIVE)
		)

	return heat_index.quantize(ONE_TENTH, rounding=decimal.ROUND_UP)


def calculate_wind_chill(temperature, wind_speed):
	if temperature > WIND_CHILL_THRESHOLD:
		return None

	T = temperature
	WS = _as_decimal(wind_speed)

	if WS == ZERO:  # No wind results in no chill, so skip it
		return T

	V = WS ** WC_V_EXP
	wind_chill = (
		WC_C1 + (WC_C2 * T) - (WC_C3 * V) + (WC_C4 * T * V)
	).quantize(ONE_TENTH)

	return T if wind_chill > T else wind_chill


def calculate_thw_index(temperature, relative_humidity, wind_speed):
	hi = calculate_heat_index(temperature, relative_humidity)
	WS = _as_decimal(wind_speed)
	if not hi:
		return None
	return (
		hi - (THW_INDEX_CONSTANT * WS).quantize(ONE_TENTH, rounding=decimal.ROUND_DOWN)
	)


def calculate_thsw_index(temperature, relative_humidity, solar_radiation, wind_speed):
	T = convert_fahrenheit_to_celsius(temperature)
	RH = _as_decimal(relative_humidity)
	WS = convert_miles_per_hour_to_meters_per_second(_as_decimal(wind_speed))
	E = RH / 100 * THSW_6_105 * (THSW_17_27 * T / (THSW_237_7 + T)).exp()
	Thsw = T + (THSW_0_348 * E) - (THSW_0_70 * WS) + THSW_0_70 * (solar_radiation / (WS + 10)) - THSW_4_25
	return convert_celsius_to_fahrenheit(Thsw).quantize(ONE_TENTH)


def calculate_cooling_degree_days(average_temperature):
	if average_temperature <= DEGREE_DAYS_THRESHOLD:
		return None
	return average_temperature - DEGREE_DAYS_THRESHOLD


def calculate_heating_degree_days(average_temperature):
	if average_temperature >= DEGREE_DAYS_THRESHOLD:
		return None
	return DEGREE_DAYS_THRESHOLD - average_temperature


def calculate_10_minute_wind_average(records):
	speed_queue = collections.deque(maxlen=10)
	direction_queue = collections.deque(maxlen=10)
	timestamp_queue = collections.deque(maxlen=10)
	current_max = ZERO
	current_direction_list = []
	current_timestamp_list = []

	for (wind_speed, wind_speed_direction, timestamp_station, minutes_covered, ) in records:
		if minutes_covered > 10:
			# We can't calculate this unless all the records cover 10 or fewer minutes
			return None, None, None, None

		wind_speed = _as_decimal(wind_speed)

		# We want each record to be present in the queue the same number of times as minutes it spans
		# So if a record spans 5 minutes, it counts as 5 items in the 10-minute queue
		speed_queue.extend([wind_speed] * minutes_covered)
		direction_queue.extend([wind_speed_direction] * minutes_covered)

		# The timestamp is special, because we need to do some math with it
		if minutes_covered == 1:
			timestamp_queue.append(timestamp_station)
		else:
			# The timestamp represents the end of the time span
			timestamp_queue.extend(
				[timestamp_station - datetime.timedelta(minutes=i) for i in range(minutes_covered - 1, -1, -1)]
			)

		if len(speed_queue) == 10:
			# This is the rolling average of the last 10 minutes
			average = sum(speed_queue) / 10
			if average > current_max:
				current_max = average
				current_direction_list = list(direction_queue)
				current_timestamp_list = list(timestamp_queue)

	if current_max > ZERO:
		wind_speed_high_10_minute_average = current_max

		wind_speed_high_10_minute_average_direction = None
		wind_speed_high_10_minute_average_start = None
		wind_speed_high_10_minute_average_end = None

		if current_direction_list:
			count = collections.Counter(current_direction_list)
			wind_speed_high_10_minute_average_direction = count.most_common()[0][0]

		if current_timestamp_list:
			wind_speed_high_10_minute_average_start = current_timestamp_list[0]
			wind_speed_high_10_minute_average_end = current_timestamp_list[-1]

		return (
			wind_speed_high_10_minute_average,
			wind_speed_high_10_minute_average_direction,
			wind_speed_high_10_minute_average_start,
			wind_speed_high_10_minute_average_end,
		)

	return None, None, None, None
assert (
	calculate_10_minute_wind_average([]) == (None, None, None, None, )
)
assert (
	calculate_10_minute_wind_average(
		[
			(1, 'NW', datetime.datetime(2016, 4, 29, 6, 5), 5, ),
			(1, 'NNW', datetime.datetime(2016, 4, 29, 6, 15), 10, ),
			(2, 'WNW', datetime.datetime(2016, 4, 29, 6, 26), 11, ),
			(1, 'NE', datetime.datetime(2016, 4, 29, 6, 27), 1, ),
		],
	) == (None, None, None, None, )
)
assert (
	calculate_10_minute_wind_average(
		[
			(1, 'NW', datetime.datetime(2016, 4, 29, 6, 10), 10, ),
			(1, 'NNW', datetime.datetime(2016, 4, 29, 6, 20), 10, ),
			(2, 'WNW', datetime.datetime(2016, 4, 29, 6, 30), 10, ),
			(1, 'NE', datetime.datetime(2016, 4, 29, 6, 40), 10, ),
		],
	) ==
	(decimal.Decimal('2'), 'WNW', datetime.datetime(2016, 4, 29, 6, 21), datetime.datetime(2016, 4, 29, 6, 30), )
)
assert (
	calculate_10_minute_wind_average(
		[
			(1, 'NW', datetime.datetime(2016, 4, 29, 6, 5), 5, ),
			(1, 'NNW', datetime.datetime(2016, 4, 29, 6, 10), 5, ),
			(2, 'WNW', datetime.datetime(2016, 4, 29, 6, 15), 5, ),
			(1, 'NE', datetime.datetime(2016, 4, 29, 6, 20), 5, ),
		],
	) ==
	(decimal.Decimal('1.5'), 'NNW', datetime.datetime(2016, 4, 29, 6, 6), datetime.datetime(2016, 4, 29, 6, 15), )
)
assert (
	(
		calculate_10_minute_wind_average(
			[
				(1, 'NW', datetime.datetime(2016, 4, 29, 6, 2), 2, ),
				(1, 'NNW', datetime.datetime(2016, 4, 29, 6, 4), 2, ),
				(2, 'N', datetime.datetime(2016, 4, 29, 6, 6), 2, ),
				(1, 'NE', datetime.datetime(2016, 4, 29, 6, 8), 2, ),
				(3, 'NE', datetime.datetime(2016, 4, 29, 6, 10), 2, ),
				(1, 'N', datetime.datetime(2016, 4, 29, 6, 12), 2, ),
				(2, 'NE', datetime.datetime(2016, 4, 29, 6, 14), 2, ),
				(1, 'NNW', datetime.datetime(2016, 4, 29, 6, 16), 2, ),
				(1, 'NNW', datetime.datetime(2016, 4, 29, 6, 18), 2, ),
				(2, 'NNW', datetime.datetime(2016, 4, 29, 6, 20), 2, ),
			],
		)
	) == (decimal.Decimal('1.8'), 'NE', datetime.datetime(2016, 4, 29, 6, 5), datetime.datetime(2016, 4, 29, 6, 14), )
)


def _append_to_list(l, v):
	if v:
		l.append(v)


def calculate_all_record_values(record):
	arguments = {}

	wind_speed = _as_decimal(record.get('wind_speed'))
	wind_speed_high = record.get('wind_speed_high')
	humidity_outside = record.get('humidity_outside')
	humidity_inside = record.get('humidity_inside')
	barometric_pressure = record.get('barometric_pressure')
	temperature_outside = record.get('temperature_outside')
	temperature_outside_low = record.get('temperature_outside_low')
	temperature_outside_high = record.get('temperature_outside_high')
	temperature_inside = record.get('temperature_inside')
	solar_radiation = record.get('solar_radiation')
	solar_radiation_high = record.get('solar_radiation_high')

	if wind_speed:
		ws_mpm = wind_speed / 60
		distance = ws_mpm * record['minutes_covered']
		arguments['wind_run_distance_total'] = distance

	if humidity_outside and barometric_pressure:
		if temperature_outside:
			a = calculate_wet_bulb_temperature(temperature_outside, humidity_outside, barometric_pressure)
			if a:
				arguments['temperature_wet_bulb'] = a
		if temperature_outside_low:
			a = calculate_wet_bulb_temperature(temperature_outside_low, humidity_outside, barometric_pressure)
			if a:
				arguments['temperature_wet_bulb_low'] = a
		if temperature_outside_high:
			a = calculate_wet_bulb_temperature(temperature_outside_high, humidity_outside, barometric_pressure)
			if a:
				arguments['temperature_wet_bulb_high'] = a

	if humidity_outside:
		a = []
		b = []
		if temperature_outside:
			_append_to_list(a, calculate_dew_point(temperature_outside, humidity_outside))
			_append_to_list(b, calculate_heat_index(temperature_outside, humidity_outside))
		if temperature_outside_low:
			_append_to_list(a, calculate_dew_point(temperature_outside_low, humidity_outside))
			_append_to_list(b, calculate_heat_index(temperature_outside_low, humidity_outside))
		if temperature_outside_high:
			_append_to_list(a, calculate_dew_point(temperature_outside_high, humidity_outside))
			_append_to_list(b, calculate_heat_index(temperature_outside_high, humidity_outside))
		if a:
			arguments['dew_point_outside'] = a[0]
			arguments['dew_point_outside_low'] = min(a)
			arguments['dew_point_outside_high'] = max(a)
		if b:
			arguments['heat_index_outside'] = b[0]
			arguments['heat_index_outside_low'] = min(b)
			arguments['heat_index_outside_high'] = max(b)

	if humidity_inside and temperature_inside:
		a = calculate_dew_point(temperature_inside, humidity_inside)
		b = calculate_heat_index(temperature_inside, humidity_inside)
		if a:
			arguments['dew_point_inside'] = a
		if b:
			arguments['heat_index_inside'] = b

	if (wind_speed or wind_speed_high) and (temperature_outside or temperature_outside_high or temperature_outside_low):
		a = []
		if wind_speed and temperature_outside:
			_append_to_list(a, calculate_wind_chill(temperature_outside, wind_speed))
		if wind_speed and temperature_outside_high:
			_append_to_list(a, calculate_wind_chill(temperature_outside_high, wind_speed))
		if wind_speed and temperature_outside_low:
			_append_to_list(a, calculate_wind_chill(temperature_outside_low, wind_speed))
		if wind_speed_high and temperature_outside:
			_append_to_list(a, calculate_wind_chill(temperature_outside, wind_speed_high))
		if wind_speed_high and temperature_outside_high:
			_append_to_list(a, calculate_wind_chill(temperature_outside_high, wind_speed_high))
		if wind_speed_high and temperature_outside_low:
			_append_to_list(a, calculate_wind_chill(temperature_outside_low, wind_speed_high))
		if a:
			arguments['wind_chill'] = a[0]
			arguments['wind_chill_low'] = min(a)
			arguments['wind_chill_high'] = max(a)

	if humidity_outside and (temperature_outside or temperature_outside_high or temperature_outside_low):
		ws = wind_speed if wind_speed else 0
		wsh = wind_speed_high if wind_speed_high else 0

		a = []
		if temperature_outside:
			_append_to_list(a, calculate_thw_index(temperature_outside, humidity_outside, ws))
			_append_to_list(a, calculate_thw_index(temperature_outside, humidity_outside, wsh))
		if temperature_outside_high:
			_append_to_list(a, calculate_thw_index(temperature_outside_high, humidity_outside, ws))
			_append_to_list(a, calculate_thw_index(temperature_outside_high, humidity_outside, wsh))
		if temperature_outside_low:
			_append_to_list(a, calculate_thw_index(temperature_outside_low, humidity_outside, ws))
			_append_to_list(a, calculate_thw_index(temperature_outside_low, humidity_outside, wsh))
		if a:
			arguments['thw_index'] = a[0]
			arguments['thw_index_low'] = min(a)
			arguments['thw_index_high'] = max(a)

		if solar_radiation or solar_radiation_high:
			a = []
			if temperature_outside and solar_radiation:
				_append_to_list(a, calculate_thsw_index(temperature_outside, humidity_outside, solar_radiation, ws))
				_append_to_list(a, calculate_thsw_index(temperature_outside, humidity_outside, solar_radiation, wsh))
			if temperature_outside_high and solar_radiation:
				_append_to_list(
					a,
					calculate_thsw_index(temperature_outside_high, humidity_outside, solar_radiation, ws),
				)
				_append_to_list(
					a,
					calculate_thsw_index(temperature_outside_high, humidity_outside, solar_radiation, wsh),
				)
			if temperature_outside_low and solar_radiation:
				_append_to_list(
					a,
					calculate_thsw_index(temperature_outside_low, humidity_outside, solar_radiation, ws),
				)
				_append_to_list(
					a,
					calculate_thsw_index(temperature_outside_low, humidity_outside, solar_radiation, wsh),
				)
			if temperature_outside and solar_radiation_high:
				_append_to_list(
					a,
					calculate_thsw_index(temperature_outside, humidity_outside, solar_radiation_high, ws),
				)
				_append_to_list(
					a,
					calculate_thsw_index(temperature_outside, humidity_outside, solar_radiation_high, wsh),
				)
			if temperature_outside_high and solar_radiation_high:
				_append_to_list(
					a,
					calculate_thsw_index(temperature_outside_high, humidity_outside, solar_radiation_high, ws),
				)
				_append_to_list(
					a,
					calculate_thsw_index(temperature_outside_high, humidity_outside, solar_radiation_high, wsh),
				)
			if temperature_outside_low and solar_radiation_high:
				_append_to_list(
					a,
					calculate_thsw_index(temperature_outside_low, humidity_outside, solar_radiation_high, ws),
				)
				_append_to_list(
					a,
					calculate_thsw_index(temperature_outside_low, humidity_outside, solar_radiation_high, wsh),
				)
			if a:
				arguments['thsw_index'] = a[0]
				arguments['thsw_index_low'] = min(a)
				arguments['thsw_index_high'] = max(a)

	return arguments
