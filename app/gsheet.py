import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name((os.environ['GOOGLE_CREDENTIALS'], scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("NLine1").sheet1

# Extract and print all of the values
# list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)



def create_user(uid,phone_num,referred_by):


    num_of_users = (sheet.col_values(1))[-1]
    row = [int(num_of_users) + 1, uid, phone_num, referred_by]

    index = (int(num_of_users) + 2)
    sheet.insert_row(row, index)

