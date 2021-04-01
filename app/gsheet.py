import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], scope)
client = gspread.authorize(creds)


sheet = client.open("NLine1").sheet1

# Extract and print all of the values
# list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)

#hi

def create_user(uid,phone_num,referred_by,username):


    num_of_users = (sheet.col_values(1))[-1]
    row = [int(num_of_users) + 1, uid, phone_num, referred_by, username]

    index = (int(num_of_users) + 2)
    sheet.insert_row(row, index)

def update(x):
    values_list = sheet.col_values(4)
    score = values_list.count(x)

    uuid_list = sheet.col_values(2)
    uuid_index = uuid_list.index(x)
    sheet.update((str('F' + str(uuid_index + 1))), score)

    return score