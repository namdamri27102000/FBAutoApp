from crawler import Account, GroupCrawler, UserCrawler
from time import sleep
import random

username = input('Type your username of Facebook: ')
password = input('type your password of Facebook: ')
fb_link = 'https://www.facebook.com/'
group_link = 'https://www.facebook.com/groups/649228858868758'
friend_link = 'https://www.facebook.com/friends/list'
user_test_link = "https://www.facebook.com/lukhach113"

# group_crawler = GroupCrawler(username=username, password=password, link=fb_link)
# group_crawler.LogIn()
# sleep(10)
# group_crawler.link = group_link
# user_list = group_crawler.GetMemberList(save=True, scroll_num=30)

user_crawler = UserCrawler(username=username, password=password, link=fb_link)
user_crawler.LogIn()
sleep(10)


user_crawler.link = friend_link
friends = user_crawler.GetFriendList(scroll_num=30)
random.shuffle(friends)
child_friends = random.sample(friends, 50)

number_frs = 0
for fr in child_friends:
    user_crawler.link = fr
    try:
        user_crawler.AutoLike()
        number_frs+=1
    except:
        pass
print("number of friend liked", number_frs)
sleep(10)
user_crawler.Logout()

# for li in user_list:
#     user_crawler.link = li
#     user_crawler.SendFriendRequest()

# user_crawler.link = user_test_link
# user_crawler.AutoLike()
    
# sleep(10)
# group_crawler.Logout()
# user_crawler.Logout()

# account = Account(username=username, password=password, link=fb_link)
# account.LogIn()
# sleep(10)
# account.link = friend_link

# friends = account.GetFriendList(scroll_num=2)
# print(friends)
# sleep(1200)
