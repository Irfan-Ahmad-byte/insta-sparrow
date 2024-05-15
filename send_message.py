import instadm

import csv


file_name = 'followers_insta.csv'

u1 = ''
pass1= ''

u2 = ''
pass2 = ''

u3 = ''
pass3 = ''

u4 = ''
pass4 = ''

u5 = ''
pass5 = ''

session = f'session-{u4}'

target_users = []

with open(file_name, 'r') as fl:
    dm_list = csv.reader(fl)
    for row in dm_list:
        target_users.append(row[0])
    
user_name=''
password=''
target_user =''


def send_message(group=False):
	# Auto login
	insta = instadm.InstaDM(username=u4, password=pass4, headless=True)
	
	# Send message
	insta.sendMessage(user=u1, message='Hey! this is a test message sent by your developer.')
	
	if group:
	        # Send message
	        insta.sendGroupMessage(users=[u2, u1, u5], message='Hey! this is a test message sent to a group of users by your developer.')


if __name__ == '__main__':
	send_message(group=True)
	
	
	
