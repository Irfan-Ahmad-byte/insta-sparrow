from instagram_bot_dm import instadm

import csv


file_name = 'followers_insta.csv'

u1 = 'knightkingdelivery_dc'
pass1= 'AuCl3AR9(('

u2 = 'computertechservice1'
pass2 = '@Computer1122'

u3 = 'levajim928'
pass3 = 'levajim@928'

u4 = 'knightkingdeliverysw'
pass4 = 'AuCl3AR9(@'

u5 = 'devirfan.insta'
pass5 = 'IL@tmys@lf1@insta'

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
	
	
	
