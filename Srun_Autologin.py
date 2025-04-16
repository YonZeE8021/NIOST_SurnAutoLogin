import sys
import platform  
import subprocess  
import time  
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import Select  
import os

def ping_baidu(timeout=5):  # 默认超时时间为5秒
    # 调用ping命令，-c 1表示只发送一个数据包，根据操作系统不同，这个参数可能有所不同（Windows下用 -n 1）
    param = '-c' if 'linux' in platform.system().lower() or 'darwin' in platform.system().lower() else '-n'
    command = ['ping', param, '1', 'www.baidu.com']
    # 设置 STARTUPINFO 来隐藏窗口（仅在 Windows 上有效）
    startupinfo = None
    if sys.platform == "win32":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    try:
        # 使用subprocess.run，添加timeout参数，设置超时时间
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, startupinfo=startupinfo)
        if result.returncode == 0:
            print("www.baidu.com 可以ping通")
            return True
        else:
            print("www.baidu.com 无法ping通")
            return False
    except subprocess.TimeoutExpired:
        print(f"ping命令超时，超过 {timeout} 秒未响应")
        return False
    except Exception as e:
        print(f"发生错误: {e}")
        return False

def get_cooling():  
    filename = 'C:\\SurnAutoLoginYoz\\Config.txt'  # 确保路径分隔符正确  
    cooling = None 
    timeout = None 
    try:  
        with open(filename, 'r', encoding='utf-8') as file:  
            for current_line_number, line in enumerate(file, start=1):  
                if current_line_number == 11:  
                    cooling = line.strip()  
                elif current_line_number == 13:
                    timeout = line.strip()
                    break  
        print(f"Coolingtime: {cooling}")  
        return cooling, timeout
    except FileNotFoundError:  
        print(f"文件 {filename} 不存在。")  
        return None  
    except Exception as e:  
        print(f"读取文件时发生错误: {e}")  
        return None
    
def login_to_school_web():  
    """  
    The function to handle the login process.  
    """  
    filename = 'C:\\SurnAutoLoginYoz\Config.txt'  # 使用双反斜杠作为路径分隔符  
  
    # Initialize variables to store username, password, and domain  
    username = None  
    password = None  
    domain = None  
    schoolWebURL = None
    cooling = None
  
    # Open the file and read the necessary lines  
    try:  
        with open(filename, 'r', encoding='utf-8') as file:  
            for current_line_number, line in enumerate(file, start=1):  
                if current_line_number == 3:  
                    username = line.strip()  
                elif current_line_number == 5:  
                    password = line.strip()  
                elif current_line_number == 7:  
                    domain = line.strip()  
                elif current_line_number == 9:  
                    schoolWebURL = line.strip()
                    break
    except FileNotFoundError:  
        print(f"The file {filename} does not exist.")  
        return  
    except Exception as e:  
        print(f"An error occurred: {e}")  
        return  
  
    # Print the retrieved information  
    print(f"Username: {username}")  
    print(f"Password: {password}")  
    print(f"Domain: {domain}")  
    print(f"SchoolWebURL: {schoolWebURL}")   

    # 指定 chromedriver.exe 的路径  
    chromedriver_path = "C:/SurnAutoLoginYoz/chromedriver.exe"  
      
    # 设置 Chrome 浏览器选项  
    chrome_options = webdriver.ChromeOptions()  

    # Setup Chrome options  
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")  #无头模式
    chrome_options.add_argument("--ignore-certificate-errors")  
  
    # 初始化 WebDriver  
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)   
    driver.get(schoolWebURL)  
    time.sleep(3)  
  
    # Handle SSL certificate warnings if present  
    if driver.find_elements("id", "details-button"):  
        details_button = driver.find_element("id", "details-button")  
        details_button.click()  
        time.sleep(2)  
  
    if driver.find_elements("id", "proceed-link"):  
        proceed_link = driver.find_element("id", "proceed-link")  
        proceed_link.click()  
        time.sleep(2)  
  
    # Login if the login button is present  
    if driver.find_elements("id", "login-account"):  
        ele = driver.find_element("id", "login-account")  
        if ele.is_enabled():  
            print("当前状态：未登录，即将进行登录操作......")  
            ele_username = driver.find_element("id", "username")  
            ele_username.send_keys(username)  
            ele_password = driver.find_element("id", "password")  
            ele_password.send_keys(password)  
  
            domain_element = driver.find_element("id", "domain")  
            time.sleep(2)  
            if domain_element:  
                select = Select(domain_element)  
                select.select_by_visible_text(domain)  
                ele.click()  
                time.sleep(3)  
                print("当前状态：已登录")  
            else:  
                print("坏了，没找到你的运营商选择框在哪...")  
    elif driver.find_elements("id", "logout"):  
        ele = driver.find_element("id", "logout")  
        if ele.is_enabled():  
            print("当前状态：已登录")  
    else:  
        print("超时了...要不......再试试？")  
  
    driver.quit()  
  
if __name__ == "__main__":
    timeout = 5
    while True:  
        if not ping_baidu(timeout):  
            print("Ping to www.baidu.com failed. Attempting to login to school web.")  
            login_to_school_web()
        cooling_time, timeout = get_cooling()
        cooling_time = int(cooling_time)
        timeout = int(timeout)
        if cooling_time == 0:
            sys.exit()
        time.sleep(cooling_time)
