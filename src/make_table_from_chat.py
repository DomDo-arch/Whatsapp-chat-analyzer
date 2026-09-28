try:
	from src.date_format import date_format
	from src.am_pm_format import am_pm_format
	from src.ios_format import ios_format
except ModuleNotFoundError:
	from date_format import date_format
	from am_pm_format import am_pm_format
	from ios_format import ios_format
	
from re import findall
from datetime import date
from pandas import DataFrame
    
def make_table(input_text_file):
    
    # Initialize empty lists to convert to columns
    dates = []
    hours = []
    message_contents = []
    users = []
    weekday_num = []
    
    # Make dates, hours columns
    date_pattern = r'\d{2}/\d{2}/\d{2}'
    hours_pattern = r'\d{2}:\d{2}'

    # Read exported chat
    with open(input_text_file, "r") as file:
        file = file.readlines()
        
        for row in file:
            if len(findall(date_pattern, row)) != 0:
            	# iOS chat detection
            	if ios_format == True:
            		if am_pm_format == True:
            			hours.append(f"{row.split()[1]} {row.split()[2]}")
            		else:
            			hours.append(f"{row.split()[1].replace(']','')}")	
            		
            		users.append((row.split("]")[1].split(":"))[0].strip())
            		message_list = (row.split("]")[1].split(":")[1:])
            		
            		if message_list[0].startswith(" http"):
            			link = ':'.join(message_list).strip()
            			message_contents.append(link)
            		else:
            			message_contents.append((':'.join((row.split("]")[1].split(":")[1:]))))
            	# Android chat
            	else:  
            		if am_pm_format == True:
            			hours.append(f"{row.split()[1]} {row.split()[2]}")
            			message_contents.append((':'.join(' '.join(row.split()[3:]).split(":")[1:])).strip())
            	
            			users.append(' '.join(row.split()[3:]).split(":")[0])
            	
            			dates.append(' '.join(findall(date_pattern, row)).split()[0])
            		else:
            			if findall(hours_pattern, row):
            				hours.append(f"{row.split()[1]}")
            		
            				message_contents.append((':'.join(' '.join(row.split()[3:]).split(":")[1:])).strip())
            	
            				users.append(' '.join(row.split()[3:]).split(":")[0])
            	
            				dates.append(' '.join(findall(date_pattern, row)).split()[0])
    
    date_list = date_format.replace("%", "").split("/")
    	
    day_index = date_list.index("d")
    month_index = date_list.index("m")
    year_index = date_list.index("y")
    	
    for i in range(len(dates)):
    	date_a = dates[i].split("/")
    	
    	day = int(date_a[day_index])
    	month = int(date_a[month_index])
    	year = 2000+int(date_a[year_index])
    		
    	weekday_num.append(date(year, month, day).weekday())
   	
   	# Debug
    #print(len(dates), len(hours), len(message_contents), len(users), len(weekday_num))
    
    df = DataFrame(data = 
    {"date":dates,
    "hours":hours,
    "weekday":weekday_num,
    "user_event":users,
    "message":message_contents}
    )

    return df

if __name__ == "__main__":

	#df = make_table("src/tests/chat_family.txt")
	#df = make_table("src/en_tests/en_chat.txt")
	#df = make_table("tests/chat_woz_mnghè.txt")
    
	#print(df)
	
	#for i in range(len(df)): print(df.hours[i], df.user_event[i])
	
	#df = make_table("tests/ios_chat.txt")
	#df = make_table("tests/chat_woz_mnghè.txt")
	df = make_table("en_tests/en_chat.txt")
			
	print(df.hours)