from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest


keys = ('first_name', 'status', 'error')
passList = ['abc', 'Abc']
values = [(i, 1, '') for i in passList]
errDict = {
    'This field is required': ['', ' '],
    'Invalid first name': ['123', 'abc123', 'z'*41, '!@#$%', 'SELECT * FROM firstname'],
}
values += [(k, 0, i) for i, j in errDict.items() for k in j]
@pytest.mark.parametrize(keys, values)
class TestLogin:
    def setup(self):   
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get('https://acyhk.com/en/open-live-account')

    def teardown(self):
        self.driver.quit()

    def test_first_name(self, first_name, status, error):
        print(f'【{first_name}】')
        for _ in range(2):
            try:
                self.driver.find_element(By.CSS_SELECTOR, 'svg[fill="none"]').click()
                break
            except:
                self.driver.refresh()

        ele = self.driver.find_element(By.CSS_SELECTOR, 'input[data-testid="firstname"]')
        ele.clear()
        ele.send_keys(first_name)
        ele.submit()

        try:
            self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="undefined-btn"]').click()
        except:
            pass
        
        if status:
            sig = True
            try:
                self.driver.find_element(By.CSS_SELECTOR, 'span[class="jss159 jss160"]')   
                sig = False
            except:          
                pass
            assert sig == True
        else:
            assert error in self.driver.page_source

  
if __name__ == '__main__':
    pytest.main(['-s', 'test_main.py', '--disable-warnings', '--html=report.html'])         
