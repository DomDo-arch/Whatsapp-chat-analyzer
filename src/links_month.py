try:
	from src.make_table_from_chat import make_table
	from src.date_format import date_format
except ModuleNotFoundError:
	from make_table_from_chat import make_table
	from date_format import date_format

from pandas import DataFrame
from os import listdir
from collections import Counter

def count_links(df):
	
	links_list = []
	
	for i in range(len(df)):
		if df.message[i].startswith("http"):
			if date_format == "%d/%m/%y":
				links_list.append(int(df.date[i].split("/")[1]))
			elif date_format == "%m/%d/%y":
				links_list.append(int(df.date[i].split("/")[0]))
			
	links_dict = dict(Counter(links_list))
	
	links_dict = {k: v for k, v in sorted(links_dict.items(), key=lambda item: item[0])}

	return(links_dict)

def count_links_df(df):
	
	df = count_links(df)
	
	col_rows = []
	
	num_name_short = {0:"title", 1:"jan",2:"feb",3:"mar",4:"apr",5:"may",6:"jun",7:"jul",8:"aug",9:"sep",10:"oct",11:"nov",12:"dec","title":"title"}

	for i in df.items():
		if i[0] != "title":
			col_rows.append([num_name_short[i[0]], i[1]])
	
	df = DataFrame(col_rows)
	
	df.rename(columns = {0:"month",1:"month_count"}, inplace = True)
	
	return df

def count_links_month(folder):
	
	files = []
	
	for file in os.listdir(folder):
		if file.endswith(".txt"):
			files.append(count_links(f"{folder}/{file}"))
	
	df = DataFrame(files)
	
	cols = df.columns.tolist()
	
	num_name_short = {0:"title", 1:"jan",2:"feb",3:"mar",4:"apr",5:"may",6:"jun",7:"jul",8:"aug",9:"sep",10:"oct",11:"nov",12:"dec"}
	
	cols = cols[-1:] + cols[:-1]
	df = df[cols]
	
	df_a = df.title.values.astype(str).argsort()
	
	df = DataFrame(df.values[df_a])
	df.rename(columns = num_name_short, inplace = True)		
	
	return df

def links_month_dir(folder, destination=None, title_list=None):
	
	links_list = []
	
	if isinstance(folder[0], DataFrame):
		for i in range(len(folder)):
			links_dicts = count_links(folder[i])
			links_dicts["title"] = title_list[i]
			links_list.append(links_dicts)

	elif isinstance(folder, list):
		for i in range(len(folder)):
			if folder[i].endswith(".txt"):
				links_dicts = count_links(make_table(f"{folder[i]}"))
				if title_list is not None:
					links_dicts["title"] = title_list[i]
				else:
					links_dicts["title"] = folder[i].replace(".txt","").split("/")[len(folder[i].split("/"))-1]
				links_list.append(links_dicts)
	else:	
		for file in listdir(folder):
			if file.endswith(".txt"):
				links_dicts = count_links(make_table(f"{folder}/{file}"))
				filename = file.replace(".txt","")
				links_dicts["title"] = filename
				links_list.append(links_dicts)
			
	df = DataFrame(links_list)
	
	num_name_short = {1:"jan",2:"feb",3:"mar",4:"apr",5:"may",6:"jun",7:"jul",8:"aug",9:"sep",10:"oct",11:"nov",12:"dec"}
	
	cols = df.columns.tolist()
	
	cols.remove("title")
	cols = sorted(cols)
	cols.append("title")
	cols = cols[-1:] + cols[:-1]
	
	df = df[cols]
	
	df.rename(columns = num_name_short, inplace = True)
	
	if destination is not None:
		df.to_csv(destination, index = False)

	return df
	
if __name__ == "__main__":
	
	df = make_table("tests/test_chat.txt")
	
	#print(count_links_df(df))
	#links_month_dir("tests", "output_csv/links_month.csv")
	#print(folder_to_csv("tests"))
	
	#print(links_month_dir(["tests/test_chat.txt","tests/chat_family.txt"], title_list=["test", "family"]))
	
	print(links_month_dir([make_table("tests/test_chat.txt"), make_table("tests/chat_family.txt")], title_list=["test", "test1"]))
