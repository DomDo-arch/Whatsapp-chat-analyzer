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
	from src.year_stats import year_messages_df
	from src.gini_index import gini
	from src.gini_user_table import gini_user_df

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
	from year_stats import year_messages_df
	from gini_index import gini
	from gini_user_table import gini_user_df
	
import streamlit as st

import datetime as dt

import seaborn as sns
import matplotlib.pyplot as plt

import numpy as np

from re import findall

from pandas import DataFrame
from datetime import date

def read_input(input_txt: str, ios_checkbox: bool, am_pm_checkbox: bool, date_selectbox: str) -> DataFrame:
		
	dates = []
	hours = []
	message_contents = []
	users = []
	weekday_num = []
		
	date_pattern = r'\d{2}/\d{2}/\d{2}'
	hours_pattern = r'\d{2}:\d{2}'

	if len(input_txt) != 0:
		file = input_txt[0].readlines()

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
	
	if len(input_txt) != 0:
		return df
	else:
		return None

def Message_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox):
	
	df = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	period = st.menu_button("Period", options = ["7d","30d","90d","150d","365d"])
		
	days_interval = 0

	if period == "7d":
		days_interval = 7
	elif period == "30d":
		days_interval = 30
	elif period == "90d":
		days_interval = 90
	elif period == "150d":
		days_interval = 150
	elif period == "365d":
		days_interval = 365
	
	if df is not None:
		if period is not None:
			st.write(period)
		
		option_user = st.selectbox("User", [i for i in list(set(df.user_event)) if len(i)<25])
			
		df = filter_user_df(df, option_user)
		
		df = filter_messages_days_interval(df, df.date[len(df.date)-1], days_interval=days_interval, date_format=date_selectbox)
			
		st.header("Chat table user filter")
		st.write(df)
	
		# Words stats
		st.header("User messages count")
		st.write(count_messages_df(df))
	
		# Messages bar charts
		st.header("User messages bar chart")
		st.bar_chart(count_messages_df(df), x="user", y="messages_count")
	
		st.header("Words stats")
		st.write(gini(list(count_words_df(df).word_count)))
		st.write(count_words_df(df))
	
		st.header("First message each day table")
		st.write(first_message_each_day_user(df))
			
		#st.header("First message each day words stats")
	#st.write(gini(list(count_words_df(first_message_each_day_user(df)).word_count)))
		#st.write(count_words_df(first_message_each_day_user(df)))
	
		# First message
		first_message_df = first_message_each_day_df(df)
		st.header("First message each day stats")
		st.write(gini(list(first_message_df.messages_count)))
		st.write(first_message_df)
	
		st.header("First message each day bar chart")
		st.bar_chart(first_message_df, x="user", y="messages_count")
	
def Links_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox):
	
	df = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	period = st.menu_button("Period", options = ["7d","30d","90d","150d","365d"])
		
	days_interval = 7

	if period == "7d":
		days_interval = 7
	elif period == "30d":
		days_interval = 30
	elif period == "90d":
		days_interval = 90
	elif period == "150d":
		days_interval = 150
	elif period == "365d":
		days_interval = 365
	
	if df is not None:
		if period is not None:
			st.write(period)
			
		option_user = st.selectbox("User", [i for i in list(set(df.user_event)) if len(i)<25])
			
		df = filter_user_df(df, option_user)
			
		df = filter_messages_days_interval(df, df.date[len(df.date)-1], days_interval=days_interval, date_format=date_selectbox)
			
		st.header("Links table")
		st.write(make_links_table(df))
		
		# Month stats
		links = count_links_df(df, date_format=date_selectbox)
		if len(links) != 0:
			st.header("Links for each month")
			st.write(links)
		
		st.header("Links for each user table")
		links_user = user_links_df(df)
		st.write(links_user)
		
		st.header("Domains table")
		st.write(gini(list(domains_df(df).domain_count)))
		st.write(domains_df(df))
		
		if len(links) != 0:
			st.header("Links month count bar chart")
			st.bar_chart(links, x="month", y="month_count",sort=False)
		
			st.header("Links for each user bar chart")
			st.bar_chart(links_user, x="user", y="link", sort=False)
		
def Hours_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox):
	
	df = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	period = st.menu_button("Period", options = ["7d","30d","90d","150d","365d"])
		
	days_interval = 7

	if period == "7d":
		days_interval = 7
	elif period == "30d":
		days_interval = 30
	elif period == "90d":
		days_interval = 90
	elif period == "150d":
		days_interval = 150
	elif period == "365d":
		days_interval = 365
	
	if df is not None:
		if period is not None:
			st.write(period)
			
		option_user = st.selectbox("User", [i for i in list(set(df.user_event)) if len(i)<25])
			
		df = filter_user_df(df, option_user)
			
		df = filter_messages_days_interval(df, df.date[len(df.date)-1], days_interval=days_interval, date_format=date_selectbox)
	
		if am_pm_format(df) == True:
			if len(hour_am_pm_df(df)[0]) != 0:
				st.header("AM hour stats")
				st.bar_chart(hour_am_pm_df(df)[0], x="hour", y="hour_count")
			
			if len(hour_am_pm_df(df)[1]) != 0:
				st.header("PM hour stats")
				st.bar_chart(hour_am_pm_df(df)[1], x="hour", y="hour_count")
		
		else:
			st.header("Hour stats")
			st.write(gini(list(hour_df(df).hour_count)))
			st.bar_chart(hour_df(df), x="hour", y="hour_count")

def Day_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox):
	
	df = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	period = st.menu_button("Period", options = ["7d","30d","90d","150d","365d"])
		
	days_interval = 7

	if period == "7d":
		days_interval = 7
	elif period == "30d":
		days_interval = 30
	elif period == "90d":
		days_interval = 90
	elif period == "150d":
		days_interval = 150
	elif period == "365d":
		days_interval = 365
		
	if df is not None:
		if period is not None:
			st.write(period)
			
		option_user = st.selectbox("User", [i for i in list(set(df.user_event)) if len(i)<25])
			
		df = filter_user_df(df, option_user)
			
		df = filter_messages_days_interval(df, df.date[len(df.date)-1], days_interval=days_interval, date_format=date_selectbox)
			
		try:
			st.header("Day stats")
			st.write("a) Chat days:", days_without_sending_message(df, date_format=date_selectbox)[0])
			st.write("b) Days sending at least a message:", days_without_sending_message(df, date_format=date_selectbox)[1])
			st.write("c) Percent b/a:", days_without_sending_message(df, date_format=date_selectbox)[2])
		except ZeroDivisionError:
			pass
		
		if am_pm_format(df) == True:
			if len(hour_am_pm_df(df)[0]) != 0:
				st.header("AM hour stats")
				st.bar_chart(hour_am_pm_df(df)[0], x="hour", y="hour_count")
			
			if len(hour_am_pm_df(df)[1]) != 0:
				st.header("PM hour stats")
				st.bar_chart(hour_am_pm_df(df)[1], x="hour", y="hour_count")

		else:
			st.header("Day part")
			st.write(gini(list(day_part_df(df).messages_count)))
			st.bar_chart(day_part_df(df), x="day_part", y="messages_count", sort=False)
		
			st.header("Day hour stats")
			st.write(week_day_hour_df(df))
			
		try:
			st.header("Day hour heatmap")
			plt.figure(figsize=(23,6))
			title_labels = "mon tue wed thu fri sat sun".split()
			sns.heatmap(week_day_hour_df(df), annot=True, yticklabels=title_labels, cmap="coolwarm")
			st.pyplot(plt)
		except ValueError:
			st.write("Select a user")
			
def Weekday_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox):
	
	df = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	period = st.menu_button("Period", options = ["7d","30d","90d","150d","365d"])
		
	days_interval = 7

	if period == "7d":
		days_interval = 7
	elif period == "30d":
		days_interval = 30
	elif period == "90d":
		days_interval = 90
	elif period == "150d":
		days_interval = 150
	elif period == "365d":
		days_interval = 365
		
	if df is not None:
		if period is not None:
			st.write(period)
			
		option_user = st.selectbox("User", [i for i in list(set(df.user_event)) if len(i)<25])
			
		df = filter_user_df(df, option_user)
			
		df = filter_messages_days_interval(df, df.date[len(df.date)-1], days_interval=days_interval, date_format=date_selectbox)
		
		# Weekday stats
		st.header("Weekday stats")
		st.bar_chart(weekday_df(df), x="weekday", y="messages_count", sort=False)

def Months_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox):
	
	df = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	period = st.menu_button("Period", options = ["7d","30d","90d","150d","365d"])
		
	days_interval = 7

	if period == "7d":
		days_interval = 7
	elif period == "30d":
		days_interval = 30
	elif period == "90d":
		days_interval = 90
	elif period == "150d":
		days_interval = 150
	elif period == "365d":
		days_interval = 365
		
	if df is not None:
		if period is not None:
			st.write(period)
			
		option_user = st.selectbox("User", [i for i in list(set(df.user_event)) if len(i)<25])
			
		df = filter_user_df(df, option_user)
			
		df = filter_messages_days_interval(df, df.date[len(df.date)-1], days_interval=days_interval, date_format=date_selectbox)
	
		month_messages = month_count_df(df, date_format=date_selectbox)
		st.header("Month messages count bar chart")
		st.bar_chart(month_messages, x="month", y="messages_count", sort=False)
		
def Year_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox):
	
	df = read_input(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	period = st.menu_button("Period", options = ["7d","30d","90d","150d","365d"])
		
	days_interval = 7

	if period == "7d":
		days_interval = 7
	elif period == "30d":
		days_interval = 30
	elif period == "90d":
		days_interval = 90
	elif period == "150d":
		days_interval = 150
	elif period == "365d":
		days_interval = 365
		
	if df is not None:
		if period is not None:
			st.write(period)
			
		option_user = st.selectbox("User", [i for i in list(set(df.user_event)) if len(i)<25])
			
		df = filter_user_df(df, option_user)
			
		df = filter_messages_days_interval(df, df.date[len(df.date)-1], days_interval=days_interval, date_format=date_selectbox)
		st.header("Year stats")
		st.bar_chart(year_messages_df(df), x="year", y="messages_count")
		
		# Season stats
		st.header("Season stats")
		st.write(gini(list(season_df(df).messages_count)))
		st.bar_chart(season_df(df), x="season", y="messages_count", sort=False)
			
if __name__ == "__main__":
	
	# Import chat
	input_txt = st.file_uploader(label="upload", type=["txt"])

	ios_checkbox = st.sidebar.checkbox("ios", key="ios_cookie")
	am_pm_checkbox = st.sidebar.checkbox("am_pm", key="am_pm_cookie")
	date_selectbox = st.sidebar.selectbox("Date", ["%d/%m/%y", "%m/%d/%y", "%y/%m/%d"], key="date_cookie")
	
	#st.write(ios_checkbox, am_pm_checkbox, date_selectbox)
	
	def Messages():
		Message_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	def Links():
		Links_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	def Hours():
		Hours_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	def Days():
		Day_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	def Weekdays():
		Weekday_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	def Months():
		Months_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
	def Years():
		Year_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
		
	pg = st.navigation([Messages, Links, Hours, Days, Weekdays, Months, Years])
	pg.run()
