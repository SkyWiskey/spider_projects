from selenium import webdriver

driver_path = r'D:\\ChromeDriver\chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)
driver.get('https://www.mafengwo.cn/poi/7346.html')