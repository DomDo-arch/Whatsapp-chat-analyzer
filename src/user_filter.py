try:
	from src.make_table_from_chat import make_table
except ModuleNotFoundError:
	from make_table_from_chat import make_table

from datetime import date
from pandas import DataFrame

def filter_user_df(df, username):
	
	dates = []
	hours = []
	message_contents = []
	users = []
	weekday_num = []
	
	for i in range(len(df)):
		if df.user_event[i] == username:
			dates.append(df.date[i])
			hours.append(df.hours[i])
			weekday_num.append(df.weekday[i])
			users.append(df.user_event[i])
			message_contents.append(df.message[i])
			
			
	df = DataFrame(data = 
    {"date":dates,
    "hours":hours,
    "weekday":weekday_num,
    "user_event":users,
    "message":message_contents}
    )
    
	return df

if __name__ == "__main__":
	
	df = make_table("tests/test_chat.txt")
    
	print(filter_user_df(df, "Domingo"))