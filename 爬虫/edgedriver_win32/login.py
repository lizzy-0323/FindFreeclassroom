from selenium import webdriver
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from time import sleep
class LoginEmulator(object):
    def __init__(self):
        #初始化url
        self.start_url='https://jw-xpaas-dlmu-edu-cn.webvpn.dlmu.edu.cn/eams/homeExt.action'
        #初始化浏览器对象
        self.driver=webdriver.Edge(executable_path='msedgedriver.exe')
    #启动浏览器对象并模拟登陆和进入爬取的页面
    def run(self):
        self.driver.get(self.start_url)
        self.username='2220193816'
        self.password='20010307Ck.'
        self.driver.find_element_by_name('username').clear()
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_xpath("/html/body/app-root/div/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/app-login-normal/div/form/div[2]/nz-input-group/input").clear()
        self.driver.find_element_by_xpath("/html/body/app-root/div/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/app-login-normal/div/form/div[2]/nz-input-group/input").send_keys(self.password)
        self.driver.find_element_by_xpath('/html/body/app-root/div/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/app-login-normal/div/form/div[6]/div/button').click()
        sleep(5)
        self.driver.find_element_by_xpath('//*[@id="main-nav"]/ul/li[9]/a').click()
        sleep(1)
        self.driver.find_element_by_xpath('//*[@id="main-nav"]/ul/li[9]/ul/li[1]/a').click()
        self.driver.switch_to_frame('iframeMain')
    #更改查找条件
    def change_page(self,i=2):
        self.driver.find_element_by_xpath('//*[@id="select3060839504"]/option['+i+']').click()
        self.driver.find_element_by_xpath('//*[@id="select3060839504"]/option['+i+']').click()
        self.driver.find_element_by_xpath('//*[@id="select3060839504"]/option['+i+']').click()
    #获取内容
    def get_content(self):
        #保证所有的元素可以加载出来 
        sleep(2)
        #开始爬取
        table_list=[]
        self.driver.find_element_by_xpath('/html/body/table/tbody/tr/td[1]/form/table/tbody/tr[11]/td/input[2]').click()
        sleep(1)
        tbody=self.driver.find_element_by_xpath('//*[@id="grid1976372991_data"]').find_elements_by_tag_name('tr')
        for tr in tbody:
            table_list.append(tr.text)
        sleep(1)
    #翻页函数
    def get_next_page(self):
        print('正在翻页\n')
        #判断是否可以点击
        try:
            #寻找下一页的标签(
            next_page=WebDriverWait(self.driver,10).until(lambda x:x.find_element_by_xpath('//*[@id="grid1976372991_bar2_page"]/a[1]'))
        except:
            next_page=None
        if next_page:
            #如果有下一页，点击
            next_page.click()
if __name__=='__main__':
    loginer=LoginEmulator()
    loginer.run()
    loginer.get_content()
    loginer.get_next_page()

        


