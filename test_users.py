
#Test users.py

import users
import datetime as dt

users.init()

print('users initiated...')

#users.add_user(83465873, 'kozebolda', 'O', dt.date(1901,1,1), "dummy")
#users.add_user(436564, 'hozebando', 'U', dt.date(1901,1,1), "huyammy")
#users.save_userz()

#print('saved. now loading...')

#users.load_userz()
print(users.userz)

print(users.list_userz())