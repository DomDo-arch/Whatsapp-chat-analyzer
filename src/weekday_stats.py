try:
	from src.make_table_from_chat import make_table
except ModuleNotFoundError:
	from make_table_from_chat import make_table

from collections import Counter, OrderedDict
from datetime import date
from os import listdir
from pandas import DataFrame, concat

def weekday(df):

	week_day = []
	
	for day in df.weekday:
		week_day.append(day)
		
	week_num = {}
	
	week_num = dict(Counter(week_day))

	num_name = {0:"monday",1:"tuesday",2:"wednesday",3:"thursday",4:"friday",5:"saturday",6:"sunday"}

	week_num_list = []
	
	for i in week_num.items():
		week_num_list.append((num_name[i[0]], i[1]))
		
	week_num_dict = dict(week_num_list)
	
	week_num = {k: v for k, v in sorted(week_num.items(), key=lambda item: item[0])}
	
	return week_num

def weekday_df(df):
	
	df = weekday(df)
	
	col_rows = []
	
	num_name_short = {0:"mon",1:"tue",2:"wed",3:"thu",4:"fri",5:"sat",6:"sun"}
	
	for i in df.items():
		if i[0] != "title":
			col_rows.append([num_name_short[i[0]], i[1]])
		
	df = DataFrame(col_rows)
	df.rename(columns = {0:"weekday",1:"messages_count"}, inplace = True)
	
	return df
	
def weekday_folder(folder, destination=None, title_list=None):
	
	weekday_list = []
	
	if isinstance(folder[0], DataFrame):
		for i in range(len(folder)):
			weekday_dicts = weekday(folder[i])
			weekday_dicts["title"] = title_list[i]
			weekday_list.append(weekday_dicts)
	else:
		if isinstance(folder, list) == True:
			for file in range(len(folder)):
				if folder[file].endswith(".txt"):
					weekday_dicts = weekday(make_table(f"{folder[file]}"))
					if title_list is not None:
						weekday_dicts["title"] = title_list[file]
					else:
						weekday_dicts["title"] = folder[file].replace(".txt","")
					weekday_list.append(weekday_dicts)
		else:
			for file in listdir(folder):
				if file.endswith(".txt"):
					weekday_dicts = weekday(make_table(f"{folder}/{file}"))
					weekday_dicts["title"] = file.replace(".txt","")
					weekday_list.append(weekday_dicts)
	
	
	df = DataFrame(weekday_list)
	
	cols = df.columns.tolist()
	
	num_name_short = {0:"mon",1:"tue",2:"wed",3:"thu",4:"fri",5:"sat",6:"sun"}
	
	cols.remove("title")
	cols = sorted(cols)
	cols.append("title")
	cols = cols[-1:] + cols[:-1]

	df = df[cols]
	
	df.rename(columns = num_name_short, inplace = True)
	
	if destination is not None:
		df.to_csv(destination, index = False)
		
	return df

def weekday_percentage(df: DataFrame, title: str) -> DataFrame:
	
	df = weekday_folder([df], title_list = [title])
	df = df.set_index("title")
	
	res = df.div(df.sum(axis = 1), axis = 0)
	res *= 100
	
	return res.reset_index()

def weekday_percentage_folder(folder: list[DataFrame], title_list: list[str]) -> DataFrame:
	
	dfs = []
	
	for i in range(len(folder)):
		dfs.append(weekday_percentage(folder[i], title_list[i]))
	
	df = concat(dfs)
	
	return df

def find_max_week(df: DataFrame, index: int) -> list[str, str, float]:

	max_value = max([i for i in df.iloc[index, :].dropna() if isinstance(i, float)])
	titles = list(df.title)
	
	max_index = 0
	for i in range(len(df.columns)):
		if df.iloc[index, i] == max_value:
			max_index = i
			
	return [titles[index], df.columns[max_index], max_value]

def find_min_week(df: DataFrame, index: int) -> list[str, str, float]:

	min_value = min([i for i in df.iloc[index, :].dropna() if isinstance(i, float)])
	titles = list(df.title)
	
	min_index = 0
	for i in range(len(df.columns)):
		if df.iloc[index, i] == min_value:
			min_index = i
			
	return [titles[index], df.columns[min_index], min_value]

def find_max_week_dir(df: DataFrame) -> DataFrame:
	
	cols = []
	
	for i in range(len(df)):
		cols.append(find_max_week(df, i))
		
	df = DataFrame(cols)
	df.rename(columns = {0: "chat", 1: "weekday", 2:"percentage"}, inplace = True)
	
	return df

def find_min_week_dir(df: DataFrame) -> DataFrame:
	
	cols = []
	
	for i in range(len(df)):
		cols.append(find_min_week(df, i))
		
	df = DataFrame(cols)
	df.rename(columns = {0: "chat", 1: "weekday", 2:"percentage"}, inplace = True)
	
	return df
	
if __name__ == "__main__":

    input_text = "input_txt/chat_canzoniere_2022.txt"
    df = make_table(input_text)
    
    #print(weekday_df(df))
    
    #weekday_folder("tests", "output_csv/weekday_stats.csv")
    #print(weekday_folder("tests"))
    
    #print(weekday_folder(['tests/chat_family.txt', 'tests/test_chat.txt'], title_list = ["chat_family", "test_chat"]))
    #print(weekday_folder(['tests/chat_family.txt', 'tests/test_chat.txt']))
    #print(weekday_folder("tests"))
    
    #print(listdir("tests"))
    #print(weekday_folder("/var/folders/92/38pmsvzd7_35gjg64y3ztjk80000gn/T"))
    
    #print(weekday_folder([make_table("input_txt/chat_family.txt"), make_table("input_txt/chat_mamma.txt")], title_list=["family", "mother"]))
    
    print(weekday_percentage(df, title = "canzoniere"))
    
    dfs = weekday_percentage_folder([df, make_table("input_txt/chat_family.txt")], title_list = ["canzoniere", "chat_family"])
    
    #print(dfs)
    
    print(find_min_week_dir(dfs))
    
