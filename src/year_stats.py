try:
	from src.make_table_from_chat import make_table
except ModuleNotFoundError:
	from make_table_from_chat import make_table

from collections import Counter, OrderedDict
from datetime import date
from pandas import DataFrame

def year_messages_df(df):

	years = []
	
	for day in df.date:
		years.append(int(day.split("/")[2]))

	years = dict(Counter(years))
	years_list = []
	
	for i in years.items():
		years_list.append([i[0], i[1]])
		
	df = DataFrame(years_list)
	df.rename(columns = {0:"year",1:"messages_count"}, inplace = True)
	
	return df

def years_messages_list(df_a):
    	
    total_list = []
    	
    for i in range(len(df_a)):
    	total_list.append(tuple([df_a.year[i], df_a.messages_count[i]]))
    		
    return total_list
    
def year_dir(dfs_list):
    	
    dfs, total_list = [], []
    c = Counter()

    for i in dfs_list:
    	dfs.append(years_messages_list(i))
    
    for i in dfs:
    	for j in i:
    		total_list.append(j)
    	
    for year,messages_count in total_list:
    	c[year] += messages_count
    		
    dfs_values = []
    	
    for i in c.items():
    	dfs_values.append([i[0], i[1]])
    		
    df = DataFrame(dfs_values)
    	
    df.rename(columns = {0:"year",1:"messages_count"}, inplace=True)
    df = df.sort_values('year', ascending=True)
    	
    return df	


if __name__ == "__main__":

    input_text = "tests/test_chat.txt"
    df = make_table(input_text)
    
    df_a = year_messages_df(make_table("tests/test_chat.txt"))
    df_b = year_messages_df(make_table("tests/chat_family.txt"))
    
    print(year_dir([df_a, df_b]))