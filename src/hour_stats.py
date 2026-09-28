try:
	from src.make_table_from_chat import make_table
except ModuleNotFoundError:
	from make_table_from_chat import make_table

from collections import Counter, OrderedDict
from datetime import date
from os import listdir
from pandas import DataFrame

def hour(df):

	hours = []
	
	for hour in df.hours:
		if hour != "":
			hours.append(int(hour.split(":")[0]))

	hour_num = {}
	
	hour_num = dict(Counter(hours))
	
	hour_num = {k: v for k, v in sorted(hour_num.items(), key=lambda item: item[0])}
	
	return hour_num

def hour_df(df):
	
	df = hour(df)
	
	col_rows = []
	
	for i in df.items():
		col_rows.append([i[0], i[1]])
		
	df = DataFrame(col_rows)
	df.rename(columns = {0:"hour",1:"hour_count"}, inplace = True)
	
	return df

def day_part_df(df):
	
	df = hour_df(df)
	first_half_day, second_half_day = [], []
	
	for i in range(len(df)):
		if 0 <= df.hour[i] <= 11:
			first_half_day.append(df.hour_count[i])
		else:
			second_half_day.append(df.hour_count[i])
			
	col_rows = ["first_half_day", sum(first_half_day)], ["second_half_day", sum(second_half_day)]
	
	df = DataFrame(col_rows)
	df.rename(columns = {0:"day_part",1:"messages_count"}, inplace = True)
	
	return df

def day_part(df):
	
	df = hour_df(df)
	first_half_day, second_half_day = [], []
	
	for i in range(len(df)):
		if 0 <= df.hour[i] <= 11:
			first_half_day.append(df.hour_count[i])
		else:
			second_half_day.append(df.hour_count[i])
			
	col_rows = [sum(first_half_day), sum(second_half_day)]
	
	return col_rows

def hour_dir(folder, destination=None, title_list=None):
	
	weekday_list = []
	
	if isinstance(folder, list):
		for file in range(len(folder)):
			if folder[file].endswith(".txt"):
				day_parts = day_part(make_table(f"{folder[file]}"))
				if title_list is not None:
					filename = title_list[file]
				else:
					filename = folder[file].replace(".txt","").split("/")[len(folder[file].split("/"))-1]
				weekday_list.append([filename, day_parts[0], day_parts[1]])
	else:
		for file in listdir(folder):
			if file.endswith(".txt"):
				day_parts = day_part(make_table(f"{folder}/{file}"))
				filename = file.replace(".txt","")
				weekday_list.append([filename, day_parts[0], day_parts[1]])
			
	df = DataFrame(weekday_list)
	
	df.rename(columns = {0:"title", 1:"first_half_day",2:"second_half_day"}, inplace = True)
	
	if destination is not None:
		df.to_csv(destination, index = False)

	return df

def hour_stats_dir(folder, destination=None, title_list=None):
	
	hour_list = []
	
	if isinstance(folder[0], DataFrame):
		for i in range(len(folder)):
			hour_dicts = hour(folder[i])
			hour_dicts["title"] = title_list[i]
			hour_list.append(hour_dicts)
	else:
		if isinstance(folder, list):
			for i in range(len(folder)):
				if folder[i].endswith(".txt"):
					hours_dicts = hour(make_table(folder[i]))
					if title_list is not None:
						hours_dicts["title"] = title_list[i]
					else:
						hours_dicts["title"] = folder[i].replace(".txt","").split("/")[len(folder[i].split("/"))-1]
					hour_list.append(hours_dicts)
		else:
			for i in listdir(folder):
				if file.endswith(".txt"):
					hours_dicts = hour(make_table(i))
					hours_dicts["title"] = i.replace(".txt","").split("/")[len(i.split("/"))-1]
					hour_list.append(hours_dicts)
			
				
	df = DataFrame(hour_list)
	
	cols = df.columns.tolist()
	
	cols.remove("title")
	cols = sorted(cols)
	cols.append("title")
	cols = cols[-1:] + cols[:-1]

	df = df[cols]
	
	if destination is not None:
		df.to_csv(destination, index=False)
	
	return df		

import seaborn as sns

import matplotlib.pyplot as plt
import numpy as np

xlabels = ["test1", "test2"]
table = [[1,2],[3,4]]

#plt.figure(figsize=(2,2))
#sns.heatmap(table, xticklabels=xlabels)
#plt.show()
	
	
if __name__ == "__main__":

    input_text = "tests/test_chat.txt"
    
    #df = make_table(input_text)
    
    #print(day_part(df))
    #print(hour_dir("tests", destination="output_csv/hour_stats.csv"))
    #print(hour_dir(["tests/test_chat.txt", "tests/chat_pasquetta.txt"], title_list = ["test", "pasquetta"]))
    
    #print(hour_df(make_table("tests/test_chat.txt")))
    #print(hour(make_table(input_text)))
    
    #print(hour_stats_dir(["tests/test_chat.txt", "tests/chat_pasquetta.txt"], title_list=["test1", "test2"]))
    
    df = hour_stats_dir(["tests/test_chat.txt", "tests/chat_pasquetta.txt"], title_list=["test1", "test2"])
    
    title_label = list(df.title)
    df = df.drop(columns=['title'])

    plt.figure(figsize=(len(df.columns),len(df)))
    sns.heatmap(df, yticklabels=title_label, annot=True)

    plt.show()