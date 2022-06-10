import time
import os

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class DouyinCommentSpider(object):

    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach',True)
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver_path = r'D://ChromeDriver/chromedriver.exe'
    path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(path, 'db')
    def __init__(self,video_id):
        self.driver = webdriver.Chrome(executable_path=self.driver_path,options=self.options)
        self.url = f'https://www.douyin.com/video/{video_id}?previous_page=app_code_link'

    def run(self):
        self.driver.get(self.url)
        time.sleep(5)

        for i in range(1,1000):
            WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div[2]/div/div/div[1]/div[3]/div/div/div[4]/div["+str(i)+"]/div/div[2]/p/span/span/span/span/span/span"))
            )
            comment = self.driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div/div/div[1]/div[3]/div/div/div[4]/div["+str(i)+"]/div/div[2]/p/span/span/span/span/span/span")
            try:
                time.sleep(0.5)
                self.storage_data(comment)
                self.driver.execute_script('window.scrollBy(0,150)')
            except:
                self.driver.execute_script('window.scrollBy(0,100)')
                time.sleep(0.5)
                self.storage_data(comment)

    def storage_data(self,comment):
        if comment.text:
            with open(f'{self.file_path}/comments.txt', 'a', encoding='utf8') as f:
                f.write(comment.text + '\n')
            print(comment.text)
        else:
            pass

def main():
    video_id = input('请输入视频id号>>>')
    spider = DouyinCommentSpider(video_id)
    spider.run()

if __name__ == '__main__':
    main()