# Import any WebDriver class that you would usually import from
# selenium.webdriver from the seleniumrequests module
from seleniumrequests import Chrome

# Simple usage with built-in WebDrivers:
webdriver = Chrome()
response = webdriver.request('GET', 'https://www.google.com/')
print(response)


# More complex usage, using a WebDriver from another Selenium-related module:
from seleniumrequests.request import RequestsSessionMixin
from someothermodule import CustomWebDriver


class MyCustomWebDriver(RequestsSessionMixin, CustomWebDriver):
    pass


custom_webdriver = MyCustomWebDriver()
response = custom_webdriver.request('GET', 'https://www.google.com/')
print(response)

driver = seleniumrequests.Remote(
    'http://192.168.101.1:4444/wd/hub',
    options=chrome_options,
    proxy_host='192.168.101.2')
