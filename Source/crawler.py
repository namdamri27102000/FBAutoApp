import os
import time
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import json


class Account:
    def __init__(self, username, password, link):
        self.username = username
        self.password = password
        self.link = link
        option = Options()

        option.add_argument("--disable-infobars")

        option.add_argument("start-maximized")

        option.add_argument("--disable-extensions")

        option.add_experimental_option("prefs", 
        {"profile.default_content_setting_values.notifications": 2 
        }) 

        self.driver = webdriver.Chrome(options=option)   

    def LogIn(self):
        self.driver.get(self.link)
        sleep(5)
        txtUser = self.driver.find_element(By.XPATH, '//*[@id="email"]')
        txtUser.send_keys(self.username)
        txtPass = self.driver.find_element(By.XPATH, '//*[@id="pass"]')
        txtPass.send_keys(self.password)
        txtPass.send_keys(Keys.ENTER)

    def Logout(self):
        self.driver.close()

    def GetFriendList(self, scroll_num=1):
        #friend list link: https://www.facebook.com/friends/list
        self.driver.get(self.link)
        sleep(5)
        span_tags = self.driver.find_elements(By.TAG_NAME, value='span')
        for sp in span_tags:
            if "người bạn" in sp.text:
                sp.click()
                break
        for i in range(scroll_num):
            self.driver.find_element(By.TAG_NAME, value='body').send_keys(Keys.END)
            sleep(3)
        self.driver.find_element(By.TAG_NAME, value='body').send_keys(Keys.HOME)       
        a_tags = self.driver.find_elements(By.TAG_NAME, value='a')
        friend_links = []
        for tag in a_tags:
            fr_link = tag.get_attribute('href')
            if "https://www.facebook.com/" in fr_link:
                friend_links.append(fr_link)
                friend_links = list(set(friend_links))
        print("number of friend: ", len(friend_links))
        return friend_links


    def AutoPost(self, txt, imgs):
        pass

    def AutoComment(self, txt, imgs, post_id):
        pass


class GroupCrawler(Account):
    def __init__(self, username, password, link):
        super().__init__(username, password, link)
    
    def GetMemberList(self, save=False, scroll_num = 1):
        self.driver.get(os.path.join(self.link, 'members'))
        sleep(5)

        for i in range(scroll_num):
            scroll = self.driver.find_element(By.TAG_NAME, value='body').send_keys(Keys.END)
            sleep(3)
        scroll = self.driver.find_element(By.TAG_NAME, value='body').send_keys(Keys.HOME)
        sleep(10)
        users_link = []
        NewMember = self.driver.find_elements(By.TAG_NAME, 'span')
        for i in range(len(NewMember)):
            if NewMember[i].text == 'Mới vào nhóm':
                for j in range(i+1, len(NewMember)):
                    try:
                        a_tag = NewMember[j].find_element(By.TAG_NAME, 'a').get_attribute('href')
                        users_link.append(a_tag)
                        # print(a_tag)
                    except:
                        pass                
                
                break
        users_link = list(set(users_link))
        print('Number of users: ', len(users_link))
        if save:
            json_object = json.dumps(users_link)
            with open('Newmembers.json', 'w') as outputfile:
                outputfile.write(json_object)        
        return users_link
    
    def GetPostsIds(self):
        pass

    def AutoLike(self, post_id):
        pass
    
class UserCrawler(Account):
    def __init__(self, username, password, link):
        super().__init__(username, password, link)

    def SendFriendRequest(self):
        try:
            self.driver.get(self.link)
        except:
            print('Time Out..., Waiting 5s')
            sleep(5)
            pass
        sleep(3)
        AddFrBut = self.driver.find_elements(By.TAG_NAME, value='span')
        for span in AddFrBut:
            if span.text == 'Thêm bạn bè':
                span.click()
                break
            elif span.text == 'Hủy lời mời':
                span.click()
                sleep(5)
                span.click()            
                break
    def AutoAccess(self):
        try:
            self.driver.get(self.link)
        except:
            pass
    def GetPostsIds(self):
        pass
    def AutoLike(self, scroll_nums = 0):
        try:
            self.driver.get(self.link)
            sleep(3)
        except:
            pass

        if scroll_nums:
            for i in range(scroll_nums):
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                sleep(3)
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)

        like_tags = self.driver.find_elements(By.TAG_NAME, 'span')
        nums_of_like = 0
        for tag in like_tags:
            if (tag.text=="Thích") and (tag.get_attribute('outerHTML')=="<span>Thích</span>"):
            # and (tag.get_attribute('style') != 'color: rgb(8, 102, 255);'):
            # if tag.get_attribute('outerHTML')=="<span>Thích</span>":
                tag.click()
                nums_of_like+=1
                sleep(2)
        print(f'{self.link} -------- {nums_of_like} likes')

