try:
	from src.make_table_from_chat import make_table
except ModuleNotFoundError:
	from make_table_from_chat import make_table

from collections import Counter, OrderedDict
from datetime import date
from os import listdir
from pandas import DataFrame, concat

def month_count(df):

	month_list = []
	
	for day in df.date:
		month_list.append(int(day.split("/")[1]))
		
	month_num = {}
	
	month_num = dict(Counter(month_list))
	
	month_num = {k: v for k, v in sorted(month_num.items(), key=lambda item: item[0])}
		
	return month_num

def season_df(df):
	
	months = month_count(df)
	
	autumn, winter, spring, summer = [], [], [], []
		
	for i in months.items():
		if 3 <= i[0] <= 5:
			spring.append(i[1])
		elif 6 <= i[0] <= 8:
			summer.append(i[1])
		elif 9 <= i[0] <= 11:
			autumn.append(i[1])
		else:
			winter.append(i[1])
			
	autumn, winter, spring, summer = sum(autumn), sum(winter), sum(spring), sum(summer)
	
	seasons = [["aut",autumn], ["win",winter], ["spr",spring], ["sum",summer]]
	
	df = DataFrame(seasons)
	df.rename(columns = {0:"season", 1:"messages_count"}, inplace = True)
	
	return df

def season(df: DataFrame) -> dict[str:int]:
	
	months = month_count(df)
	
	autumn, winter, spring, summer = [], [], [], []
		
	for i in months.items():
		if 3 <= i[0] <= 5:
			spring.append(i[1])
		elif 6 <= i[0] <= 8:
			summer.append(i[1])
		elif 9 <= i[0] <= 11:
			autumn.append(i[1])
		else:
			winter.append(i[1])
			
	autumn, winter, spring, summer = sum(autumn), sum(winter), sum(spring), sum(summer)
	
	seasons = {"aut":autumn, "win":winter, "spr":spring, "sum":summer}
	
	return seasons

def season_dir(folder, destination=None, title_list=None):
	
	season_list = []
	
	if isinstance(folder[0], DataFrame):
		for i in range(len(folder)):
			season_dicts = season(folder[i])
			season_dicts["title"] = title_list[i]
			season_list.append(season_dicts)
	else:
		if isinstance(folder, list):
			for i in range(len(folder)):
				if folder[i].endswith(".txt"):
					season_dicts = season(make_table(f"{folder[i]}"))
					if title_list is not None:
						season_dicts["title"] = title_list[i]
					else:
						season_dicts["title"] = folder[i].replace(".txt","").split("/")[len(folder[i].split("/"))-1]
					season_list.append(season_dicts)
		else:
			for file in listdir(folder):
				if file.endswith(".txt"):
					filename = file.replace(".txt","")
					season_dicts = season(make_table(f"{folder}/{file}"))
					season_dicts['title'] = filename
					season_list.append(season_dicts)
	
	df = DataFrame(season_list)
	cols = df.columns.tolist()
	
	cols = cols[-1:] + cols[:-1]
	df = df[cols]
	
	if destination is not None:
		df.to_csv(destination, index = False)
	
	return df

def season_percentage(df: DataFrame, title) -> DataFrame:
	
	df = season_dir([df], title_list = [title])
	df = df.set_index("title")

	res = df.div(df.sum(axis = 1), axis = 0)
	res *= 100
	
	return res.reset_index()

def season_percentage_folder(folder: list[DataFrame], title_list:list[str]) -> DataFrame:
	
	dfs = []	

	for i in range(len(folder)):
		dfs.append(season_percentage(folder[i], title_list[i]))

	df = concat(dfs)
	
	return df
	
if __name__ == "__main__":

    input_text = "input_txt/chat_canzoniere_2022.txt"
    
    df = make_table(input_text)
    
    #print(season(df))

    #print(folder_to_csv("tests", "output_csv/season.csv"))
    
    #print(season_dir(["tests/test_chat.txt", "tests/chat_family.txt"], title_list=["test","family"]))
    
    dfs = season_dir([make_table("input_txt/chat_canzoniere_2022.txt"), make_table("input_txt/chat_family.txt")], title_list=["canzoniere", "family"])
    #print(dfs)
    
    print(season_percentage_folder([make_table("input_txt/chat_canzoniere_2022.txt")], title_list = ["canzoniere", "family"]))
