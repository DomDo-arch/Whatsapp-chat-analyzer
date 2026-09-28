from streamlit import file_uploader, segmented_control, navigation, write, sidebar, checkbox, divider, text_input

# Import pages
from pages.entire_chat import Message_page, Links_page, Hours_page, Day_page, Weekday_page, Months_page, Year_page
from pages.chat_subset import Message_page_subset, Links_page_subset, Hours_page_subset, Day_page_subset, Weekday_page_subset, Months_page_subset, Year_page_subset
from pages.user_subset import Message_user_subset, Links_user_subset, Hours_user_subset, Day_user_subset, Weekday_user_subset, Months_user_subset, Year_user_subset

# Import chat
input_txt = file_uploader(label="Files", accept_multiple_files=True, type="txt")

# Chat mode
options = ["Entire chat","Chat subset","User subset"]
selection = segmented_control("Option page", options, selection_mode="single", default="Entire chat", required=True)

# Sidebar checkboxes
ios_checkbox = sidebar.checkbox("ios", key="ios_cookie")
am_pm_checkbox = sidebar.checkbox("am_pm", key="am_pm_cookie")
date_selectbox = sidebar.selectbox("Date", ["%d/%m/%y", "%m/%d/%y", "%y/%m/%d"], key="date_cookie")

# Entire page sections
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

try:
	if selection == "Entire chat":
		pg = navigation([Messages, Links, Hours, Days, Weekdays, Months, Years])
		pg.run()
except ValueError:
	write(date_format_error)

# Chat subset sections
def Messages():
	Message_page_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
def Links():
	Links_page_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
def Hours():
	Hours_page_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
def Days():
	Day_page_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
def Weekdays():
	Weekday_page_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
def Months():
	Months_page_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
def Years():
	Year_page_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)

try:
	if selection == "Chat subset":
		pg = navigation([Messages, Links, Hours, Days, Weekdays, Months, Years])
		pg.run()
except ValueError:
	write(date_format_error)
	
# User subset sections
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
	Month_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)
	
def Years():
	Year_user_subset(input_txt, ios_checkbox, am_pm_checkbox, date_selectbox)

try:
	if selection == "User subset":
		pg = navigation([Messages, Links, Hours, Days, Weekdays, Months, Years])
		pg.run()
except ValueError:
	write(date_format_error)
