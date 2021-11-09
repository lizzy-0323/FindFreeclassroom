from numpy import iinfo
from selenium import webdriver
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from time import sleep
from sqlalchemy import create_engine, engine
import pandas as pd
class LoginEmulator(object):

    def __init__(self):
        #初始化url
        self.start_url='https://jw-xpaas-dlmu-edu-cn.webvpn.dlmu.edu.cn/eams/homeExt.action'
        #初始化浏览器对象
        self.driver=webdriver.Edge(executable_path='msedgedriver.exe')
        #当前页数
        self.page=1

    #启动浏览器对象并模拟登陆和进入爬取的页面
    def run(self):
        self.driver.get(self.start_url)
        self.username='2220193626'
        self.password='7139606Ww/'
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

    #获取内容
    def get_content(self):
        #保证所有的元素可以加载出来 
        sleep(2)
        #开始爬取
        df=pd.DataFrame()
        #设置查找条件循环爬取
        for i in range(5,21):
            self.driver.find_element_by_xpath('//*[@id="select3060839504"]/option['+str(i)+']').click()
            for j in range(2,9):
                self.driver.find_element_by_xpath('//*[@id="select3060839505"]/option['+str(j)+']').click()
                for k in range(2,12):
                    self.page=1
                    self.driver.find_element_by_xpath('//*[@id="select3060839506"]/option['+str(k)+']').click()
                    self.driver.find_element_by_xpath('/html/body/table/tbody/tr/td[1]/form/table/tbody/tr[11]/td/input[2]').click()
                    sleep(5)
                    #切换到1000个显示的模式
                    self.driver.find_element_by_xpath('//*[@id="grid1976372991_bar2_page"]/span[1]').click()
                    self.driver.find_element_by_xpath('//*[@id="grid1976372991_bar2_page_select"]').click()
                    self.driver.find_element_by_xpath('//*[@id="grid1976372991_bar2_page_select"]/option[9]').click()
                    self.driver.find_element_by_xpath('//*[@id="grid1976372991_bar2_page"]/span[2]/input[2]').click()
                    sleep(1)
                    df=self.process(i,j,k)
                    #删除多余的行
                    df=df.loc[ : , ~df.columns.str.contains("^Unnamed")]
                    #存入数据库中
                    df.to_sql('classData',con=self.save(),if_exists='append')
                    # print(df)
                    # tbody=self.driver.find_element_by_xpath('//*[@id="grid1976372991_data"]').find_elements_by_tag_name('tr') 
                    # #转化成字典
                    # for i in range(len(tbody)):
                    #     dict[i]=tbody[i]
                    #     df=pd.DataFrame([dict])    
                    #     print(df)
            
    #处理数据   
    def process(self,i,j,k):
        html=self.driver.execute_script("return document.documentElement.outerHTML")
        df=pd.read_html(html)[5]
        df=df.drop(labels=['教学楼','校区','教室类型','容量'],axis=1)
        #插入新列，作为id
        df.insert(0,'id',str(i-1)+str(j-1)+str(k-1))
        return df
    #将数据保存到数据库
    def save(self):
        engine=create_engine('sqlite:///class.db')
        return engine
if __name__=='__main__':
    loginer=LoginEmulator()
    loginer.run()
    loginer.get_content()