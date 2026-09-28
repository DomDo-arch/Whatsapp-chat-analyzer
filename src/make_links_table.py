try:
	from src.make_table_from_chat import make_table
except ModuleNotFoundError:
	from make_table_from_chat import make_table

from datetime import date
from pandas import DataFrame
from os import listdir
from collections import Counter, defaultdict

def make_links_table(df):
	
	dates, hours, weekday_num, users, links = [], [], [], [], []
	
	for i in range(len(df)):
		if df.message[i].startswith("http"):
			dates.append(df.date[i])
			links.append(':'.join(df.message[i].split()))
			hours.append(df.hours[i])
			weekday_num.append(df.weekday[i])
			users.append(df.user_event[i])
			
	df = DataFrame(data = 
	{"date":dates,
    "hours":hours,
    "weekday":weekday_num,
    "user_event":users,
    "message":links}
    )
    
	return df
	
	# Export dataframe to csv
	#df.to_csv(f"{input_txt.replace('.txt', "")}_links_table.csv", index = True)
	
def count_links(input_txt):
	
	df = make_table(input_txt)
	df = make_links_table(df)
	
	count = 0
	
	for i in range(len(df)):
		if df.message[i].startswith("http"):
			count += 1
			
	return count
	
def make_table_count_links(folder, destination = None):
	
	filenames = []
	
	for file in listdir(folder):
		if file.endswith(".txt"):
			filenames.append([file.replace(".txt",""), count_links(f"{folder}/{file}")])
	
	df = DataFrame(sorted(filenames))
	
	df.rename(columns = {0:"chat", 1:"links"}, inplace = True)
	
	if destination is not None:
		df.to_csv(f"{destination}.csv", index = True)
	
	return df
	
def user_links_df(df):
	
	df = make_links_table(df)
	
	user_links_count = Counter(df.user_event)
	
	user_links = DataFrame(user_links_count.items(), columns = ["user", "link"])
	user_links = user_links.sort_values("user", ascending = True)

	return user_links

def domains_df(df):
	
	df = make_links_table(df)
	
	links = [link for link in df.message]
	domains = []
	
	for link in links:
		domains.append(link.split("/")[2])
		
	dict_domains = dict(Counter(domains))
	
	df = DataFrame(dict_domains.items(), columns = ["domain", "domain_count"])
	df = df.sort_values("domain", ascending = True)
	
	return df

def make_domains_count_dir(folder, destination=None, title_list=None):
	
	file_domains = []
	
	if isinstance(folder[0], DataFrame):
		for i in range(len(folder)):
			domains = domains_df(folder[i])
			domains_num = sum(list(domains.domain_count))
			filename = title_list[i]
			file_domains.append([filename, domains_num])
	
	elif isinstance(folder, list):
		for i in range(len(folder)):
			if folder[i].endswith(".txt"):
				domains = domains_df(make_table(f"{folder[i]}"))
				domains_num = sum(list(domains.domain_count))
				if title_list is not None:
					filename = title_list[i]
				else:
					filename = folder[i].replace(".txt","").split("/")[len(folder[i].split("/"))-1]
				file_domains.append([filename, domains_num])
	else:
		for file in listdir(folder):
			if file.endswith(".txt"):
				domains = domains_df(make_table(f"{folder}/{file}"))
				domains_num = sum(list(domains.domain_count))
				filename = file.replace(".txt","")
				file_domains.append([filename, domains_num])
	
	df = DataFrame(file_domains)
	df.rename(columns = {0:"title",1:"domains_count"}, inplace = True)
	
	if destination is not None:
		df.to_csv(f"{destination}")	
		
	return df

# Group chats by common domains
# domain, chats

def group_chats_domains_dir(folder, destination=None, title_list=None):
	
	chat_domain = []
	
	if isinstance(folder[0], DataFrame):
		for i in range(len(folder)):
			domains = domains_df(folder[i])
			filename = title_list[i]
			for j in range(len(domains)):
				chat_domain.append([domains.domain[j], filename])
	else:
		if isinstance(folder, list):
			for i in range(len(folder)):
				if folder[i].endswith(".txt"):
					domains = domains_df(make_table(f"{folder[i]}"))
					if title_list is not None:
						filename = title_list[i]
					else:
						filename = folder[i].replace(".txt", "").split("/")[len(folder[i].split("/"))-1]
				
					for j in range(len(domains)):
						chat_domain.append([domains.domain[j], filename])
		else:
			for file in listdir(folder):
				if file.endswith(".txt"):
					domains = domains_df(make_table(f"{folder}/{file}"))
					filename = file.replace(".txt","")
			
					for i in range(len(domains)):
						chat_domain.append([domains.domain[i], filename])#, domains.domain_count[i])
			
	chat_domain_lists = chat_domain

	dd = defaultdict(list)
	
	for key, value in chat_domain_lists:
		dd[key].append(value)
		
	domain = []
	chats = []
	
	for i in dd.items():
		domain.append(i[0])
		chats.append(i[1])
		
	df = DataFrame(data = 
	{"domain":domain,
	"chat":chats})
	
	if destination is not None:
		df.to_csv(f"{destination}")
	
	return df

if __name__ == "__main__":

	#input_txt = "en_tests/en_chat.txt"
	#df = make_table(input_txt)
	
	#print(count_links(input_txt))
	#print(make_links_table(df))
	#print(domains_df(df))
	
	#print(user_links_df(make_table("tests/chat_biscuits.txt")))
	#print(make_domains_count_table("tests", "output_csv/domains_count_table.csv"))
	
	#print(domains_df(make_table("tests/chat_papà.txt")))
	#print(domains_df(make_table("tests/chat_mamma.txt")))
	
	#domain_chat = group_chats_domains_dir("tests")
	
	#for i in range(len(domain_chat)): print(domain_chat.domain[i], domain_chat.chat[i])

	#print(make_domains_count_dir(["tests/chat_family.txt", "tests/chat_mamma.txt"]))
	#print(group_chats_domains_dir(["tests/chat_family.txt", "tests/chat_mamma.txt"]))
	
	#print(group_chats_domains_dir([make_table("tests/chat_family.txt")], title_list = ["test"]))
	
	print(make_domains_count_dir([make_table("tests/test_chat.txt")], title_list=["test"]))