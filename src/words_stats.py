try:
	from src.make_table_from_chat import make_table
	from src.gini_index import gini
except ModuleNotFoundError:
	from make_table_from_chat import make_table
	from gini_index import gini

from collections import Counter
from pandas import DataFrame
from os import listdir, path, mkdir
from datetime import datetime, timedelta
import numpy as np

def words_stats(df):

    words = []
    
    for sentence in df.message.values:
        for word in sentence.split():
            words.append(word.replace("?", "").replace(",","").replace(".", "").replace(";","").replace("<","").replace(">","").lower().replace("(","").replace(")",""))
        
    words_count = Counter(words)
    
    return words_count
    
def count_messages_df(df):
    
    # Messages sent by each user
    user_messages_count = Counter(df.user_event.values)
    
    users = []
    messages = []
    
    # Filter messages
    for user in user_messages_count.items():
        if len(user[0]) < 25 and user[0] != "":
            users.append(user[0])
            messages.append(user[1])
            
        df_user_messages = DataFrame(data = 
        {"user":users,
        "messages_count":messages}
        )
    
    messages = df_user_messages.sort_values('user', ascending = True)
        
    return messages
   
def count_words_df(df):

    words_count = words_stats(df)
    
    word_item = []
    word_count = []
    
    for word in words_count.most_common(): #[::-1]
        word_item.append(word[0])
        word_count.append(word[1]) 

    df_word_frequency = DataFrame(data = 
    {"word":word_item,
    "word_count":word_count})
        
    return df_word_frequency
    
def chat_to_csv(input_chat, destination):
    
    df = make_table(input_chat)
    
    messages = count_messages_df(df)
    words = count_words_df(df)

    if path.isdir(f"{destination}") == False:
    	mkdir(f"{destination}")
    
    file = input_chat.replace('.txt','').split('/')
    
    filename = f"{file[len(file)-1]}"
    
    # Export dataframe to csv
    messages.to_csv(f'{destination}/{filename}_messages.csv')
    words.to_csv(f'{destination}/{filename}_words.csv')
    
def words_stats_dir(input_folder, destination):

	for chat in listdir(input_folder):
		if chat.endswith(".txt"):
			chat_to_csv(f"{input_folder}/{chat}", destination)	

def total_messages_dir(folder, destination=None, title_list=None):
	
	cols = []

	if isinstance(folder[0], DataFrame):
		for i in range(len(folder)):
			cols.append([title_list[i], len(folder[i])])
	else:
		for i in range(len(folder)):
			if title_list is not None:
				cols.append([title_list[i], len(make_table(folder[i]))])
			else:
				cols.append([folder[i].split("/")[len(folder[i].split("/"))-1].replace(".txt",""), len(make_table(folder[i]))])
		
	df = DataFrame(cols)
	df.rename(columns = {0:"chat", 1:"messages_count"}, inplace = True)
	
	return df

def users_z_score(df) -> DataFrame:

	z_scores = []

	messages_a = count_messages_df(df)

	messages= list(messages_a.messages_count)

	std = np.std(messages)
	avg = sum(messages)/len(messages)

	for i in range(len(messages)):
		z_scores.append([messages_a.user[i], (messages_a.messages_count[i]-avg)/std])
	
	df = DataFrame(z_scores)
	df.rename(columns = {0:"user", 1:"z_score"}, inplace = True)

	df = df.sort_values("z_score", ascending = False)

	return df

if __name__ == "__main__":
	
	pass
	df = make_table("tests/chat_woz_mnghè.txt")

	# Export single chat to csv
	#chat_to_csv("tests/test_chat.txt", "csv_outputs")
	
	#words_stats_dir("tests", "output_csv/words_stats")
	
	#print(words_stats(df))
	#print(total_messages_dir(["src/tests/chat_family.txt", "src/tests/chat_mamma.txt"], title_list = ["test", "test1"]))
	#print(total_messages_dir([make_table("src/tests/chat_family.txt")], title_list = ["test"]))
	
	print(users_z_score(df))