try:
	from src.make_table_from_chat import make_table
	from src.weekday_stats import weekday, weekday_df, weekday_folder
	from src.words_stats import words_stats, count_messages_df, count_words_df, total_messages_dir, users_z_score
	from src.day_stats import filter_messages_by_date, filter_messages_date_interval, message_date_list, filter_messages_days_interval, days_without_sending_message
	from src.links_month import count_links, count_links_month, count_links_df, links_month_dir
	from src.make_links_table import make_links_table, count_links, make_table_count_links, user_links_df, domains_df, make_domains_count_dir, group_chats_domains_dir
	from src.month_stats import month_count, month_count_df, month_dir
	from src.hour_stats import hour_df, day_part_df, hour_dir
	from src.day_hour_stats import week_day_hour_df, hour_am_pm_df, week_day_hour_am_pm_df, am_pm_format, day_hour_dir
	from src.user_filter import filter_user_df
	from src.season_stats import season_df, season_dir
	from src.first_messages import first_message_each_day_df, first_message_each_day_user
	from src.year_stats import year_messages_df, year_dir
	from src.gini_index import gini
	from src.gini_user_table import gini_user_df
	from src.users_word_table import user_word_table

except ModuleNotFoundError:
	
	# File testing
	import sys
	import os
	
	sys_path = os.getcwd().split("/")
	sys_path.append("src")
	sys_path = "/".join(sys_path)
	sys.path.append(sys_path)
	
	#st.write(sys_path)
	
	from make_table_from_chat import make_table
	from weekday_stats import weekday, weekday_df, weekday_folder
	from words_stats import words_stats, count_messages_df, count_words_df, total_messages_dir, users_z_score
	from day_stats import filter_messages_by_date, filter_messages_date_interval, message_date_list, filter_messages_days_interval, days_without_sending_message
	from links_month import count_links, count_links_month, count_links_df, links_month_dir
	from make_links_table import make_links_table, count_links, make_table_count_links, user_links_df, domains_df, make_domains_count_dir, group_chats_domains_dir
	from month_stats import month_count, month_count_df, month_dir
	from hour_stats import hour_df, day_part_df, hour_dir
	from day_hour_stats import week_day_hour_df, hour_am_pm_df, week_day_hour_am_pm_df, am_pm_format, day_hour_dir
	from user_filter import filter_user_df
	from season_stats import season_df, season_dir
	from first_messages import first_message_each_day_df, first_message_each_day_user
	from year_stats import year_messages_df, year_dir
	from gini_index import gini
	from gini_user_table import gini_user_df
	from users_word_table import user_word_table

import streamlit as st

import datetime as dt

import seaborn as sns
import matplotlib.pyplot as plt

import numpy as np

from re import findall

from pandas import DataFrame
from datetime import date

def read_input(input_txt: str, ios_checkbox: bool, am_pm_checkbox: bool, date_selectbox: str) -> list:
		
	tables = []
	filenames = []

	def return_table(file) -> DataFrame:

		#file = input_txt[1].readlines()
		
		dates = []
		hours = []
		message_contents = []
		users = []
		weekday_num = []
		
		date_pattern = r'\d{2}/\d{2}/\d{2}'
		hours_pattern = r'\d{2}:\d{2}'
		
		for row in file:
			row = row.decode("utf-8")
			if len(findall(date_pattern, row)) != 0:
				if ios_checkbox == True:
					if am_pm_checkbox == True:
						hours.append(f"{row.split()[1]} {row.split()[2]}")
					else:
						hours.append(f"{row.split()[1].replace(']','')}")
				
					users.append((row.split("]")[1].split(":"))[0].strip())
					message_list = (row.split("]")[1].split(":")[1:])
					dates.append(' '.join(findall(date_pattern, row)).split()[0])
					
					if message_list[0].startswith(" http"):
						link = ':'.join(message_list).strip()
						message_contents.append(link)
					else:
						message_contents.append((':'.join((row.split("]")[1].split(":")[1:]))))
            		
				else:
					if am_pm_checkbox == True:
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
							
		date_list = date_selectbox.replace("%", "").split("/")
		
		day_index = date_list.index("d")
		month_index = date_list.index("m")
		year_index = date_list.index("y")
		
		for i in range(len(dates)):
			date_a = dates[i].split("/")
			
			day = int(date_a[day_index])
			month = int(date_a[month_index])
			year = 2000+int(date_a[year_index])
			
			weekday_num.append(date(year, month, day).weekday())
			
		#st.write(len(dates), len(hours), len(message_contents), len(users), len(weekday_num))
		
		df = DataFrame(data = 
		{"date":dates,
		"hours":hours,
		"weekday":weekday_num,
		"user_event":users,
		"message":message_contents}
		)
		
		return df
	
	if input_txt is not None:
		
		for i in range(len(input_txt)):
		
			file_list = input_txt[i].readlines()

			tables.append(return_table(file_list))
			filename = (input_txt[i].name).replace(".txt","")
			
			filenames.append(filename)

			
	return tables, filenames

def Message_page(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox):
	
	df = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)[0]
	filenames = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)[1]
	
	if df is not None:
		if len(df) == 1:
			df = df[0]
			st.header("Chat table")
			st.write(df)
			
			# Word stats
			st.header("Words stats")
			st.write(gini(list(count_words_df(df).word_count)))
			st.write(count_words_df(df))
		
			# User messages
			st.header("User messages count")
			st.write(gini(list(count_messages_df(df).messages_count)))
			st.write(count_messages_df(df))
				
			st.header("Users word table")
			word = st.selectbox("Word", list(set(count_words_df(df).word)))
			st.write(user_word_table(df, word))
				
			st.header("Z-score")
			values = gini([abs(i) for i in users_z_score(df).z_score])
			st.write(values)
			st.write(users_z_score(df))
		
			st.header("Gini for each user table")
			with st.spinner("Loading..."):
				st.write(gini(list(gini_user_df(df).user_gini)))
				st.write(gini_user_df(df))
			
			st.header("User messages bar chart")
			st.bar_chart(count_messages_df(df), x="user", y="messages_count")
			
			# First message
			first_message_df = first_message_each_day_df(df)
			st.header("First message each day stats")
			st.write(gini(list(first_message_df.messages_count)))
			st.write(first_message_df)
				
			st.header("First message each day bar chart")
			st.bar_chart(first_message_df, x="user", y="messages_count")

		elif len(df) != 0 and len(df)>1:
			st.header("Chat messages")
			st.write(total_messages_dir(df, title_list=filenames))	
			
def Links_page(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox):
	
	df = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)[0]
	filenames = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)[1]
	
	if df is not None:
		if len(df)== 1:
			df = df[0]
			st.header("Links table")
			st.write(make_links_table(df))
		
			st.header("Links for each month")
			#st.write("std:", np.std(list(count_links_df(df).month_count)))
			links = count_links_df(df)
			st.write(links)
		
			st.header("Links for each user table")
			links_user = user_links_df(df)
			st.write(links_user)
		
			st.header("Domains table")
			st.write(gini(list(domains_df(df).domain_count)))
			st.write(domains_df(df))

			if len(links) != 0:
				st.header("Links month count bar chart")
				st.write(gini(list(links.month_count)))
				st.bar_chart(links, x="month", y="month_count",sort=False)
		
			st.header("Links for each user bar chart")
			st.bar_chart(links_user, x="user", y="link", sort=False)
			
		elif len(df) > 1:
			st.header("Links for each month")
			st.write(links_month_dir(df, title_list = filenames))
			
			st.header("Domains count")
			st.write(make_domains_count_dir(df, title_list = filenames))
			
			st.header("Group chats by domain")
			st.write(group_chats_domains_dir(df, title_list = filenames))

def Hours_page(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox):
	
	df = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)[0]
	filenames = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)[1]
	
	if df is not None:
		if len(df)==1:
			df = df[0]
			if am_pm_format(df) == True:
				st.header("AM hour stats")
				st.bar_chart(hour_am_pm_df(df)[0], x="hour", y="hour_count")
				st.header("PM hour stats")
				st.bar_chart(hour_am_pm_df(df)[1], x="hour", y="hour_count")
			else:
				st.header("Hour stats")
				st.write(gini(list(hour_df(df).hour_count)))
				st.bar_chart(hour_df(df), x="hour", y="hour_count", sort=False)	
		elif len(df) > 1:
			st.header("Day part stats")
			#st.write(hour_dir(df, title_list=filenames))

def Day_page(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox):
	
	df = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)[0]
	filename = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)[1]

	title_label = "mon tue wed thu fri sat sun".split()
	
	if df is not None:
		if len(df) == 1:
			df = df[0]

			st.header("Day stats")
			st.write("a) Chat days:", days_without_sending_message(df)[0])
			st.write("b) Days sending at least a message:", days_without_sending_message(df)[1])
			st.write("c) Percent b/a:", days_without_sending_message(df)[2])
			
			st.header("Day part")
			st.write(gini(list(day_part_df(df).messages_count)))
			st.bar_chart(day_part_df(df), x="day_part", y="messages_count", sort=False)
				
			#st.write(am_pm_format(df))

			if am_pm_format(df) == True:
				df = df[0]
				st.header("AM day hour stats")
				st.write(week_day_hour_am_pm_df(df)[0])
		
				st.header("PM day hour stats")
				st.write(week_day_hour_am_pm_df(df)[1])
			
				st.header("AM day hour heatmap")
				plt.figure(figsize=(12,6))
					
				title_label = "mon tue wed thu fri sat sun".split()
					
				sns.heatmap(week_day_hour_am_pm_df(df)[0], annot=True, yticklabels=title_label, cmap="coolwarm")
				st.pyplot(plt)
			
				st.header("PM day hour heatmap")
				plt.figure(figsize=(12,6))
				sns.heatmap(week_day_hour_am_pm_df(df)[1], annot=True, yticklabels=title_label, cmap="coolwarm")
				st.pyplot(plt)
		
			else:
				st.header("Day hour stats")
		
				with st.spinner("Loading..."):
					st.write(week_day_hour_df(df))
			
				st.header("Day hour heatmap")
					
				title_label = "mon tue wed thu fri sat sun".split()

				with st.spinner("Loading..."):
					plt.figure(figsize=(23,6))
					sns.heatmap(week_day_hour_df(df), annot=True, cmap="coolwarm", yticklabels=title_label)
					st.pyplot(plt)

		elif len(df) > 1:
				
			dfs = []
			am_dfs, pm_dfs = [], []
				
			for i in range(len(df)):
				dfs.append(df[i])
				
			if am_pm_format(dfs[0]):
				for i in range(len(dfs)):
					am_dfs.append(week_day_hour_am_pm_df(dfs[i])[0])
					pm_dfs.append(week_day_hour_am_pm_df(dfs[i])[1])
						
				st.header("AM Day hour stats")
				am_dfs = sum(am_dfs)
				st.write(am_dfs)

				st.header("PM Day hour stats")	
				pm_dfs = sum(pm_dfs)
				st.write(pm_dfs)
					
				st.header("AM Day heatmap")
				with st.spinner("Loading..."):
					plt.figure(figsize=(len(am_dfs.columns), len(am_dfs)))
					sns.heatmap(am_dfs, annot=True, yticklabels=title_label, cmap="coolwarm")
					st.pyplot(plt)
					
				st.header("PM Day heatmap")
				with st.spinner("Loading..."):
					plt.figure(figsize=(len(pm_dfs.columns), len(pm_dfs)))
					sns.heatmap(pm_dfs, annot=True, yticklabels=title_label, cmap="coolwarm")
					st.pyplot(plt)
			else:
				st.header("Day hour stats")
				st.write(day_hour_dir(df, title_list = filename))
				
				st.header("Day hour heatmap")
				df = day_hour_dir(df, title_list = filename)
				title_label = list(df.title)
				
				df = df.drop(columns=["title"])

				with st.spinner("Loading..."):
					plt.figure(figsize=(len(df.columns),len(df)))
					sns.heatmap(df, annot=True, yticklabels=title_label, cmap="coolwarm")
					st.pyplot(plt)

def Weekday_page(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox):
	
	df = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)[0]
	filenames = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)[1]
	
	if df is not None:	
		if len(df) == 1:
			df = df[0]
			st.header("Weekday stats")
			st.bar_chart(weekday_df(df), x="weekday", y="messages_count", sort=False)

		elif len(df) > 1:
			st.header("Weekday stats")
			st.write(weekday_folder(df, title_list = filenames))
				
			st.header("Weekday heatmap")
				
			df = weekday_folder(df, title_list = filenames)
			title_label = list(df.title)
				
			df = df.drop(columns=["title"])

			with st.spinner("Loading..."):
				plt.figure(figsize=(len(df.columns), len(df)))
				sns.heatmap(df, annot=True, yticklabels=title_label, cmap="coolwarm")
				st.pyplot(plt)
			
def Months_page(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox):
	
	df = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)[0]
	filenames = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)[1]

	if df is not None:
		if len(df) == 1:
			df = df[0]
			month_messages = month_count_df(df)
			st.header("Month messages count bar chart")
			st.bar_chart(month_messages, x="month", y="messages_count", sort=False)
		elif len(df) > 1:
			st.header("Month messages")
			st.write(month_dir(df, title_list=filenames))
				
			st.header("Month heatmap")
				
			df = month_dir(df, title_list=filenames)
			title_label = list(df.title)
				
			df = df.drop(columns = ["title"])
				
			with st.spinner("Loading..."):
				plt.figure(figsize = (len(df.columns), len(df)))
				sns.heatmap(df, annot=True, yticklabels=title_label, cmap="coolwarm")
				st.pyplot(plt)
			
def Year_page(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox):
	
	df = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)[0]
	filenames = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)[1]

	if df is not None:
		if len(df) == 1:
			df = df[0]
			# Year stats
			st.header("Year stats")
			st.bar_chart(year_messages_df(df), x="year", y="messages_count")
			
			# Season stats
			st.header("Season stats")
			st.write(gini(list(season_df(df).messages_count)))
			st.bar_chart(season_df(df), x="season", y="messages_count", sort=False)

		elif len(df)>1:
			
			st.header("Year stats")
			
			dfs = []
			
			for i in range(len(df)):
				dfs.append(year_messages_df(df[i]))
			
			st.bar_chart(year_dir([dfs[i] for i in range(len(dfs))]), x="year", y="messages_count", sort=False)
			
			st.header("Season stats")
			st.write(season_dir(df, title_list=filenames))
			
			st.header("Season heatmap")
			
			df = season_dir(df, title_list=filenames)
			
			title_label = list(df.title)
			df = df.drop(columns=["title"])
			
			with st.spinner("Loading..."):
				plt.figure(figsize = (len(df.columns), len(df)))
				sns.heatmap(df, annot=True, yticklabels=title_label, cmap="coolwarm")
				st.pyplot(plt)

if __name__ == "__main__":
	
	# Import chat
	input_txt = st.file_uploader(label="upload", accept_multiple_files=True, type=["txt"])
	
	# Sidebar options
	#st.sidebar.subheader("Formats")
	ios_checkbox = st.sidebar.checkbox("ios", key="ios_cookie")
	am_pm_checkbox = st.sidebar.checkbox("am_pm", key="am_pm_cookie")
	date_selectbox = st.sidebar.selectbox("Date", ["%d/%m/%y", "%m/%d/%y", "%y/%m/%d"], key="date_cookie")
	
	#st.write(ios_checkbox, am_pm_checkbox, date_selectbox)
		
	#df = read_input2(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)

	def Messages():
		Message_page(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	def Links():
		Links_page(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	def Hours():
		Hours_page(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	def Days():
		Day_page(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	def Weekdays():
		Weekday_page(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	def Months():
		Months_page(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	def Years():
		Year_page(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
		
	pg = st.navigation([Messages, Links, Hours, Days, Weekdays, Months, Years])
	pg.run()
