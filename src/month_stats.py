try:
	from src.make_table_from_chat import make_table
	from src.date_format import date_format
except ModuleNotFoundError:
	from make_table_from_chat import make_table

from collections import Counter, OrderedDict
from datetime import date
from os import listdir
from pandas import DataFrame

def month_count(df, date_format):

	month_list = []
	
	date_list = date_format.replace("%","").split("/")
	month_index = date_list.index("m")
	
	for day in df.date:
		month_list.append(int(day.split("/")[month_index]))
		
	month_num = {}
	
	month_num = dict(Counter(month_list))
	
	found_keys = list(month_num.keys())
	
	for i in list(range(1,13)):
		if i not in found_keys:
			month_num[i] = 0
	
	month_num = {k: v for k, v in sorted(month_num.items(), key=lambda item: item[0])}
			
	return month_num

def month_count_df(df, date_format):
	
	df = month_count(df, date_format)
	
	col_rows = []
	
	num_name_short = {0:"title", 1:"jan",2:"feb",3:"mar",4:"apr",5:"may",6:"jun",7:"jul",8:"aug",9:"sep",10:"oct",11:"nov",12:"dec","title":"title"}
	
	for i in df.items():
		if i[0] != "title":
			col_rows.append([num_name_short[i[0]], i[1]])
	
	df = DataFrame(col_rows)
	
	df.rename(columns = {0:"month",1:"messages_count"}, inplace = True)
	
	return df

def month_dir(folder, destination=None, title_list=None):
	
	month_list = []
	
	if isinstance(folder[0], DataFrame):
		for i in range(len(folder)):
			month_dict = month_count(folder[i])
			month_dict["title"] = title_list[i]
			month_list.append(month_dict)
	else:
		if isinstance(folder, list):
			for i in range(len(folder)):
				if folder[i].endswith(".txt"):
					month_dict = month_count(make_table(f"{folder[i]}"))
					if title_list is not None:
						month_dict["title"] = title_list[i]
					else:
						month_dict["title"] = folder[i].replace(".txt", "").split("/")[len(folder[i].split("/"))-1]
					month_list.append(month_dict)
		else:
			for file in listdir(folder):
				if file.endswith(".txt"):
					filename = file.replace(".txt", "").split("/")[len(file.split("/"))-1]
					month_dict = month_count(make_table(f"{folder}/{file}"))
					month_dict['title'] = filename
					amonth_list.append(month_dict)
	
	df = DataFrame(month_list)
	
	cols = df.columns.tolist()
	
	num_name_short = {1:"jan",2:"feb",3:"mar",4:"apr",5:"may",6:"jun",7:"jul",8:"aug",9:"sep",10:"oct",11:"nov",12:"dec"}
	
	cols = cols[-1:] + cols[:-1]
	df = df[cols]
	
	df.rename(columns = num_name_short, inplace = True)
	
	if destination is not None:
		df.to_csv(destination, index = True)
	
	return df
	
if __name__ == "__main__":

    input_text = "tests/chat_woz_mnghè.txt"
    
    #df = make_table(input_text)
    
    #print(month_count(df))
    
    #print(month_dir("src/tests"))
    #print(month_dir([make_table("tests/chat_pasquetta.txt"), make_table("tests/chat_family.txt")], title_list=["test1","test2"]))
    
