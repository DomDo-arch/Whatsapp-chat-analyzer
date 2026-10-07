try:
	from src.make_table_from_chat import make_table
	from src.words_stats import words_stats
except ModuleNotFoundError:
	from make_table_from_chat import make_table
	from words_stats import words_stats

from collections import Counter
from pandas import DataFrame
from datetime import datetime, timedelta

def filter_messages_by_date(df, date):
	
	df_counter = Counter(df.date)

	date_a, hours_a, user_event_a, message_a, weekday_a = [], [], [], [], []
	
	for i in range(len(df)):
		if df.date[i] == date:
			date_a.append(df.date[i])
			hours_a.append(df.hours[i])
			user_event_a.append(df.user_event[i])
			message_a.append(df.message[i])
			weekday_a.append(df.weekday[i])
			
	df = DataFrame(data = 
	{"date":date_a,
	"hours":hours_a,
	"weekday":weekday_a,
	"user_event":user_event_a,
	"message":message_a}
	)
	
	return df

def filter_messages_date_interval(df, start_date, end_date):
	
	df_counter = Counter(df.date)
	
	date_a, hours_a, user_event_a, message_a, weekday_a = [], [], [], [], []
	
	start_date = datetime.strptime(start_date, date_format)
	end_date = datetime.strptime(end_date, date_format)
	
	for i in range(len(df)):
		if start_date <= datetime.strptime(df.date[i], date_format) <= end_date:
			date_a.append(df.date[i])
			hours_a.append(df.hours[i])
			user_event_a.append(df.user_event[i])
			message_a.append(df.message[i])
			weekday_a.append(df.weekday[i])
			
	df = DataFrame(data = 
	{"date":date_a,
	"hours":hours_a,
	"weekday":weekday_a,
	"user_event":user_event_a,
	"message":message_a}
	)

	return df

def filter_messages_days_interval(df, start_date, days_interval, date_format):
	
	df_counter = Counter(df.date)
	
	date_a, hours_a, user_event_a, message_a, weekday_a = [], [], [], [], []
	
	start_date = datetime.strptime(start_date, date_format)
	end_date = start_date - timedelta(days = days_interval)
	
	for i in range(len(df)):
		if end_date <= datetime.strptime(df.date[i], date_format) <= start_date:
			date_a.append(df.date[i])
			hours_a.append(df.hours[i])
			user_event_a.append(df.user_event[i])
			message_a.append(df.message[i])
			weekday_a.append(df.weekday[i])
			
	df = DataFrame(data = 
	{"date":date_a,
	"hours":hours_a,
	"weekday":weekday_a,
	"user_event":user_event_a,
	"message":message_a}
	)

	return df
		
def message_date_list(df):
	
	df_counter = Counter(df.date)
	message_day = []
	
	for i in df_counter.items():
		message_day.append([i[1], i[0]])
		
	for i in sorted(message_day):
		print(i[0], i[1])
		
def days_without_sending_message(df, date_format):
	
	first_chat_date = df.date[0]
	last_chat_date = df.date[len(df.date)-1]

	first_chat_date = datetime.strptime(first_chat_date, date_format)
	last_chat_date = datetime.strptime(last_chat_date, date_format)
	
	chat_duration = (last_chat_date - first_chat_date).days
	
	days_with_messages = len(set(df.date)) - 1
	
	days_without_messages = chat_duration - days_with_messages
	
	percent_days_with_messages = 100*days_with_messages/chat_duration
	
	return chat_duration, days_with_messages, percent_days_with_messages

if __name__ == "__main__":
	
	input_txt = "tests/test_chat.txt"
	
	# Dataframes
	df = make_table(input_txt)
	
	#df_a = filter_messages_by_date(df, "10/01/26")
	
	#df_b = filter_messages_date_interval(df, "26/8/25", "10/6/26")
	
	#df_c = filter_messages_days_interval(df, df.date[len(df.date)-1], 90)
	
	print(days_without_sending_message(df))
	
	print(df)
