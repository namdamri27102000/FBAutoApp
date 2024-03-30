import os
import time
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
#####
# Working with the 'add_argument' Method to modify Driver Default Notification
options.add_argument('--disable-notifications')

# Passing Driver path alongside with Driver modified Options
browser = webdriver.Chrome(options=options)
browser.get('https://www.facebook.com/groups/649228858868758')
sleep(10)
# Log In

username = "yourusername"
password = "yourpass"

txtUser = browser.find_element(By.XPATH, '//*[@id=":r2:"]')
txtUser.send_keys(username)
txtPass = browser.find_element(By.XPATH, '//*[@id=":r5:"]')
txtPass.send_keys(password)
txtPass.send_keys(Keys.ENTER)
sleep(10)

browser.get('https://www.facebook.com/groups/649228858868758/members')
sleep(5)

for i in range(25):
    scroll = browser.find_element(By.TAG_NAME, value='body').send_keys(Keys.END)
    sleep(3)
scroll = browser.find_element(By.TAG_NAME, value='body').send_keys(Keys.HOME)
sleep(10)
users_link = []
NewMember = browser.find_elements(By.TAG_NAME, 'span')
for i in range(len(NewMember)):
    if NewMember[i].text == 'Mới vào nhóm':
        for j in range(i+1, len(NewMember)):
            try:
                a_tag = NewMember[j].find_element(By.TAG_NAME, 'a').get_attribute('href')
                if len(users_link)==0:
                    users_link.append(a_tag)
                else:
                    if a_tag!=users_link[-1]:
                        users_link.append(a_tag)
                # print(a_tag)
            except:
                pass                
        print('Number of users: ', len(users_link))
        break
for user_link in users_link:
    try:
        browser.get(user_link)
    except:
        print('Time Out..., Waiting 5s')
        sleep(5)
        pass
    sleep(5)
    AddFrBut = browser.find_elements(By.TAG_NAME, value='span')
    for span in AddFrBut:
        if span.text == 'Thêm bạn bè':
            try:
                span.click()
            except:
                print('Click Error, waiting 5s')
                sleep(5)
                pass
sleep(3600)




