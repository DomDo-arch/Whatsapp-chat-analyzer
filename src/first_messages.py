try:
	from src.make_table_from_chat import make_table
	from src.words_stats import words_stats
except ModuleNotFoundError:
	from make_table_from_chat import make_table
	from words_stats import words_stats

from collections import Counter
from pandas import DataFrame

def first_message_each_day(df):
	
	dates = list(df.date)
	indexes = []
	users = []
	
	for i in dates:
		indexes.append(dates.index(i))
		
	indexes = sorted(list(set(indexes)))
	
	for i in indexes:
		if len(df.user_event[i]) < 25:
			users.append(df.user_event[i])
		
	users = dict(Counter(users))
	
	users = {k: v for k, v in sorted(users.items(), key=lambda item: item[0])}
	
	return users

def first_message_each_day_user(df):

	dates = list(df.date)
	indexes = []
	
	date_a, hours_a, users_a, message_a, weekday_a = [], [], [], [], []
	
	for i in dates:
		indexes.append(dates.index(i))
		
	indexes = sorted(list(set(indexes)))
	
	for i in indexes:
		if len(df.user_event[i]) < 25:
			date_a.append(df.date[i])
			hours_a.append(df.hours[i])
			users_a.append(df.user_event[i])
			message_a.append(df.message[i])
			weekday_a.append(df.weekday[i])
			
	df = DataFrame(data = 
	{"date":date_a,
	"hours":hours_a,
	"weekday":weekday_a,
	"user_event":users_a,
	"message":message_a}
	)
	
	return df

def first_message_each_day_df(df):
	
	df = first_message_each_day(df)
	
	col_rows = []
	
	for i in df.items():
		col_rows.append([i[0], i[1]])
		
	df = DataFrame(col_rows)
	df.rename(columns = {0:"user",1:"messages_count"}, inplace = True)
	
	return df
	

if __name__ == "__main__":
	
	input_txt = "tests/en_chat.txt"
	
	# Dataframes
	df = make_table(input_txt)
	
	df_a = first_message_each_day(df)
	df_b = first_message_each_day_df(df)
	df_c = first_message_each_day_user(df)
	
	print(df_c)