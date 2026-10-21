try:
	from src.make_table_from_chat import make_table
except ModuleNotFoundError:
	from make_table_from_chat import make_table

from collections import Counter, OrderedDict
from datetime import date
from os import listdir
from pandas import DataFrame, concat

def am_pm_format(df):
	
	am_pm_format = False
	
	for hour in df.hours:
		if "AM" in hour or "PM" in hour:
			am_pm_format = True
		else:
			am_pm_format = False
			
	return am_pm_format

def hour_am_pm(df):
	
	hours_am, hours_pm = [], []
	
	for hour in df.hours:
		if hour != "":
			if "AM" in hour:
				hours_am.append(int(hour.split(":")[0]))
			else:
				hours_pm.append(int(hour.split(":")[0]))
	
	hours_am_num = dict(Counter(hours_am))
	hours_pm_num = dict(Counter(hours_pm))
	
	hours_am_num = {k:v for k,v in sorted(hours_am_num.items(), key=lambda item: item[0])}
	hours_pm_num = {k:v for k,v in sorted(hours_pm_num.items(), key=lambda item: item[0])}
	
	
	return hours_am_num, hours_pm_num

def hour_am_pm_df(df):
	
	df = hour_am_pm(df)
	
	col_rows_am, col_rows_pm = [], []
	
	for i in df[0].items():
		col_rows_am.append([i[0], i[1]])
	for i in df[1].items():
		col_rows_pm.append([i[0], i[1]])
	
	df_am = DataFrame(col_rows_am)
	df_pm = DataFrame(col_rows_pm)
	
	df_am.rename(columns = {0:"hour", 1:"hour_count"}, inplace = True)
	df_pm.rename(columns = {0:"hour", 1:"hour_count"}, inplace = True)
	
	return df_am, df_pm

def day_part_am_pm(df):
	
	pm_count, am_count = 0, 0
	
	for i in df.hours:
		if "PM" in i:
			pm_count += 1
		else:
			am_count += 1
			
	col_rows = [["first_half_day", am_count], ["second_half_day", pm_count]]
	
	df = DataFrame(col_rows)
	df.rename(columns = {0:"day_part", 1:"message_count"}, inplace = True)
	
	return df

def day_hour_am_pm_df(df, day_hour):
	
	day_hour_am_hour, day_hour_pm_hour = [], []
	
	for i in range(len(df)):
		if "AM" in df.hours[i]:
			day_hour_am_hour.append([df.day_hour[i], int(df.hours[i].split(":")[0])])
		else:
			day_hour_pm_hour.append([df.day_hour[i], int(df.hours[i].split(":")[0])])
	
	mon_am_hour, mon_pm_hour = [], []
	
	for i in day_hour_am_hour:
		if i[0] == day_hour:
			if i[1] != "":
				mon_am_hour.append(int(i[1]))
				
	for i in day_hour_pm_hour:
		if i[0] == day_hour:
			if i[1] != "":
				mon_pm_hour.append(int(i[1]))
	
	mon_am_hour = Counter(mon_am_hour)
	mon_pm_hour = Counter(mon_pm_hour)
	
	mon_am_hour = {k:v for k,v in sorted(mon_am_hour.items(), key=lambda item: item[0])}
	mon_pm_hour = {k:v for k,v in sorted(mon_pm_hour.items(), key=lambda item: item[0])}
	
	return mon_am_hour, mon_pm_hour

def week_day_hour_am_pm_df(df):
	
	day_hour_day_hour_am_cols, day_hour_day_hour_pm_cols = [], []
	
	for day_hour in range(7):
		day_hour_day_hour_am_cols.append(day_hour_am_pm_df(df, day_hour)[0])
		day_hour_day_hour_pm_cols.append(day_hour_am_pm_df(df, day_hour)[1])
		
	df_am = DataFrame(day_hour_day_hour_am_cols)
	df_pm = DataFrame(day_hour_day_hour_pm_cols)
	
	df_am.sort_index(axis=1, inplace=True)
	df_pm.sort_index(axis=1, inplace=True)
	
	return df_am, df_pm
#
def hour(df):
	
	hours = []
	
	for hour in df.hours:
		if hour != "":
			hours.append(int(hour.split(":")[0]))

	hour_num = {}
	
	hour_num = dict(Counter(hours))
	
	hour_num = {k: v for k, v in sorted(hour_num.items(), key=lambda item: item[0])}
		
	return hour_num
#			
def hour_df(df):
	
	df = hour(df)
	
	col_rows = []
	
	for i in df.items():
		col_rows.append([i[0], i[1]])
		
	df = DataFrame(col_rows)
	df.rename(columns = {0:"hour",1:"hour_count"}, inplace = True)
	
	return df
#
def day_part_df(df):
	
	df = hour_df(df)
	first_half_day, second_half_day = [], []
	
	for i in range(len(df)):
		if 0 <= df.hour[i] <= 11:
			#print(df.hour[i], df.hour_count[i])
			first_half_day.append(df.hour_count[i])
		else:
			#print(df.hour[i], df.hour_count[i])
			second_half_day.append(df.hour_count[i])
			
	col_rows = ["first_half_day", sum(first_half_day)], ["second_half_day", sum(second_half_day)]
	
	df = DataFrame(col_rows)
	df.rename(columns = {0:"day_part",1:"messages_count"}, inplace = True)
	
	return df
#
def week_day_hour_df(df, day_hour):

	day_hour_hour = []
	
	for i in range(len(df)):
		day_hour_hour.append([df.day_hour[i], df.hours[i].split(":")[0]])
		
	mon_hour = []
	
	for i in day_hour_hour:
		if i[0] == day_hour:
			if i[1] != "":
				mon_hour.append(int(i[1]))
			
	mon_hour = Counter(mon_hour)
	
	mon_hour = {k: v for k, v in sorted(mon_hour.items(), key=lambda item: item[0])}

	return mon_hour

#
def week_day_hour_df(df):
	
	day_hour_day_hour_cols = []
	
	for day_hour in range(7):
		day_hour_day_hour_cols.append(day_hour_df(df, day_hour))
		
	df = DataFrame(day_hour_day_hour_cols)
	
	df.sort_index(axis=1, inplace=True)
	
	return df

def folder_to_csv_am(folder):
	
	for file in listdir(folder):
		if file.endswith(".txt"):
			hour_dicts_am = hour_am_pm(make_table(f"{folder}/{file}"))[0]
			hour_dicts_am["title"] = file.replace(".txt", "")
			print(hour_dicts_am)

def day_hour_dir(folder, destination=None, title_list=None):
	
	hour_list = []
	
	if isinstance(folder[0], DataFrame):
		for i in range(len(folder)):
			hour_dicts = hour(folder[i])
			hour_dicts["title"] = title_list[i]
			hour_list.append(hour_dicts)
	else:
		if isinstance(folder, list):
			for file in range(len(folder)):
				if folder[file].endswith(".txt"):
					hour_dicts = hour(make_table(f"{folder[file]}"))
					if title_list is not None:
						hour_dicts["title"] = title_list[file]
					else:
						hour_dicts["title"] = folder[file].replace(".txt", "").split("/")[len(folder[file].split("/"))-1]
					hour_list.append(hour_dicts)
		else:
			for file in listdir(folder):
				if file.endswith(".txt"):
					hour_dicts = hour(make_table(f"{folder}/{file}"))
					hour_dicts["title"] = file.replace(".txt","")
					hour_list.append(hour_dicts)
			
	df = DataFrame(hour_list)
	
	cols = df.columns.tolist()

	cols.remove("title")
	cols = sorted(cols)
	cols.append("title")
	cols = cols[-1:] + cols[:-1]
	
	df = df[cols]
	
	if destination is not None:
		df.to_csv(destination, index = False)
		
	return df

def day_hour_percentage(df: DataFrame, title: str) -> DataFrame:
	
	df = day_hour_dir([df], title_list = [title])
	df = df.set_index("title")
	
	res = df.div(df.sum(axis = 1), axis = 0)
	res *= 100
	
	return res.reset_index()

def day_hour_percentage_folder(folder: list[DataFrame], title_list: list[str]) -> DataFrame:
	
	dfs = []
	
	for i in range(len(folder)):
		dfs.append(day_hour_percentage(folder[i], title_list[i]))
	
	df = concat(dfs)
	
	return df

def find_max_day_hour(df: DataFrame, index: int) -> list[str, str, float]:

	max_value = max([i for i in df.iloc[index, :].dropna() if isinstance(i, float)])
	titles = list(df.title)
	
	max_index = 0
	for i in range(len(df.columns)):
		if df.iloc[index, i] == max_value:
			max_index = i
			
	return [titles[index], df.columns[max_index], max_value]

def find_min_day_hour(df: DataFrame, index: int) -> list[str, str, float]:

	min_value = min([i for i in df.iloc[index, :].dropna() if isinstance(i, float)])
	titles = list(df.title)
	
	min_index = 0
	for i in range(len(df.columns)):
		if df.iloc[index, i] == min_value:
			min_index = i
			
	return [titles[index], df.columns[min_index], min_value]

def find_max_day_hour_dir(df: DataFrame) -> DataFrame:
	
	cols = []
	
	for i in range(len(df)):
		cols.append(find_max_day_hour(df, i))
		
	df = DataFrame(cols)
	df.rename(columns = {0: "chat", 1: "day_hour", 2:"percentage"}, inplace = True)
	
	return df

def find_min_day_hour_dir(df: DataFrame) -> DataFrame:
	
	cols = []
	
	for i in range(len(df)):
		cols.append(find_min_day_hour(df, i))
		
	df = DataFrame(cols)
	df.rename(columns = {0: "chat", 1: "day_hour", 2:"percentage"}, inplace = True)
	
	return df

if __name__ == "__main__":

    df = make_table("input_txt/chat_family.txt")
    
    #print(day_hour_df(df, 1))
    #print(day_hour_day_hour_df(df))
    
    #print(hour(df))
    #print(hour_am_pm(df))
    #print(hour_df(df))
    #print(hour_am_pm_df(df))
    #print(day_part_am_pm(df))
    #print(day_hour_df(df, 1))
    #print(day_hour_am_pm_df(df, 1))
    #print(day_hour_day_hour_am_pm_df(df))
    #print(am_pm_format(df))
    #print(hour_am_pm_df(df))
    
    #print(folder_to_csv_am("tests"))
    #print(folder_to_csv("tests", "output_csv/day_hour_stats.csv"))
    #print(day_hour_dir(["tests/test_chat.txt", "tests/chat_pasquetta.txt"], title_list = ["test", "pasquetta"]))
    
    #print(day_hour_dir([make_table("tests/test_chat.txt")], title_list=["test"]))
    
    #print(hour(make_table(input_text)))
    
    #print(day_hour_df(make_table(input_text), 1))
    
    dfs = day_hour_percentage_folder([df, make_table("input_txt/chat_family.txt")], title_list = ["woz mnghè", "chat_family"])   
    print(dfs)
