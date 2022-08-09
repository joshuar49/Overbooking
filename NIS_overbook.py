import random 
import statistics
import pprint
import csv 

time_list =  ['12AM-8AM','8AM-4PM','4PM-12AM']
year = int(input('Year: '))
wait_time = int(input("Average wait time for airport: "))/10

def timesplit(season_factor):
	time_dict = {}
	q = random.uniform(1, 5)
	q += wait_time
	q *= season_factor
	for time in time_list:
		if time == time_list[0]:
			lo, medl = (20/q), (30/q)
		elif time == time_list[1]:
			lo, medl = 40-(20/q), 60-(30/q)
		elif time == time_list[2]:
			lo, medl = 20, 30
		hi = 40-lo
		medh = 60-medl
		time_dict.update({time: flightns_input(lo, medl, medh, hi)})
	return time_dict

def flightns_input(lo, medl, medh, hi):
	samplelist = []
	for num in range(0, 20): samplelist.append(num)

	randomlist = random.choices(
		samplelist, 
		weights=(lo,lo,lo,lo,lo,medl,medl,medl,medl,medl,medh,medh,medh,medh,medh,hi,hi,hi,hi,hi), 
		k=50)
	return randomlist

def dayns_average(season):
	if season == "winter":
		season_factor = 4
	elif season == "summer":
		season_factor = 3
	elif season == "spring" or season == "fall":
		season_factor = 1
	else:
		print("Invalid Season")
		return -1

	time_dict = timesplit(season_factor)
	day_dict = {}
	for time in time_dict.keys():
		day_avg = statistics.mean(time_dict.get(time))
		day_dict.update({time:day_avg})
	print(day_dict)
	return day_dict

def longns(season, days):
	long_dict, season_dict = {}, {}
	for date in range(0, days):
		long_dict.update({date:dayns_average(season)})
	for time_sec in range(0, 3):
		timed_sum = 0
		for day_key in long_dict.keys():
			day_value = long_dict.get(day_key)
			for time in day_value.keys():
				if time == time_list[time_sec]:
					timed_sum += day_value.get(time)
			timed_average = timed_sum/days
		season_dict.update({time_list[time_sec]:(timed_average)})
#	pprint.pprint(season_dict)
	return season_dict

def longns_days(year):
	finalseason_dict = {}
	season_list = ['winter', 'spring', 'summer', 'fall']
	time_period = input('Select time period (month, week): ')
	for season in season_list:
		timeperiod_dict = {}
		if time_period == 'month':
			if season == 'winter':
				months = [12, 1, 2]
			elif season == 'spring':
				months = [3, 4, 5]
			elif season == 'summer':
				months = [6, 7, 8]
			elif season == 'fall':
				months = [9, 10, 11]
			else:
				print('Error')
				return -1
			for month in months:
				if month in {1, 3, 5, 7, 8, 10, 12}:
					days = 31
				elif month == 2:
					if leap_year(year):
						days = 29
					else:
						days = 28
				else:
					days = 30
				timeperiod_dict.update({month:longns(season, days)})
				finalseason_dict.update({season:timeperiod_dict})
		elif time_period == 'week':
			timeperiod_dict = {}
			for week in range(0, 13):
				days = 7
				timeperiod_dict.update({week:longns(season, days)})
		else:
			print('Invalid Selection')
#	pprint.pprint(finalseason_dict)
	return finalseason_dict

def leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False

def puttofile():
	with open('overbook.csv', 'w+') as f:
		for y in range(year, year+10):
			print(y)
			final_dict = longns_days(y)
			for season in final_dict.keys():
	#			print(season)
				for month in final_dict[season].keys():
	#				print(month)
					for time in final_dict[season][month].keys():
						f.write("%s,%s,%s,%s,%s\n"%(str(y),season, month, time, final_dict[season][month].get(time)))
puttofile()