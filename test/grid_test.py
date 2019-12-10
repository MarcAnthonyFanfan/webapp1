from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

win_ff_driver = webdriver.Remote(
   command_executor = "http://192.168.1.167:4444/wd/hub",
   desired_capabilities = {
        "browserName": "firefox",
        "platform": "Windows"
    }
)

lin_ff_driver = webdriver.Remote(
   command_executor = "http://192.168.1.167:4444/wd/hub",
   desired_capabilities = {
        "browserName": "firefox",
        "platform": "Linux"
    }
)

lin_ff_driver.get("http://www.python.org")
print("title: " + lin_ff_driver.title)
lin_ff_driver.quit()

win_ff_driver.get("http://www.google.com")
print("title: " + win_ff_driver.title)
win_ff_driver.quit()