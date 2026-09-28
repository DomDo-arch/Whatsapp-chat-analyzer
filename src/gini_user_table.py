try:
	from src.user_filter import filter_user_df
	from src.make_table_from_chat import make_table
except ModuleNotFoundError:
	from user_filter import filter_user_df
	from make_table_from_chat import make_table
	
import numpy as np	
from collections import Counter
from pandas import DataFrame

def gini(x):
    # Convert to a NumPy array and sort in ascending order
    x = np.asarray(x, dtype=np.float64)
    sorted_x = np.sort(x)
    n = len(x)
    
    # Check for zero mean to avoid division by zero
    if np.sum(sorted_x) == 0:
        return 0.0
        
    # Relative mean absolute difference formula
    # G = sum_i (2i - n - 1) * x_i / (n * sum_i x_i)
    index = np.arange(1, n + 1)
    return (np.sum((2 * index - n - 1) * sorted_x)) / (n * np.sum(sorted_x))
   
def gini_user_df(df):
	
	users = [i for i in list(set(df.user_event)) if len(i)<25 and i != ""]

	def get_user_messages(user):
		
		user_message = []
		
		for i in range(len(df)):
			if df.user_event[i] == user:
				user_message.append(df.message[i])
			
		user_words = []	
		for message in user_message:
			for word in message.split():
				user_words.append(word.replace("?", "").replace(",","").replace(".", "").replace(";","").replace("<","").replace(">","").lower().replace("(","").replace(")",""))
				
		#return Counter(user_words)
		#print(gini(list(Counter(user_words).values())))
		return gini(list(Counter(user_words).values()))
	
	#user = get_user_messages("Domingo")
	#print(user)
	
	user_gini = []
	for user in users:
		user_gini.append([user, get_user_messages(user)])
		
	df = DataFrame(user_gini)
	df.rename(columns = {0:"user",1:"user_gini"}, inplace = True)
	
	df = df.sort_values('user', ascending = True)
	
	return df

   
if __name__ == "__main__":
	
	input_txt = "tests/chat_woz_mnghè.txt"
	df = make_table(input_txt)
	
	df = gini_user_df(df)
	
	print(df)