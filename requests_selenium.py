from selenium import webdriver
import time


class Render(webdriver.PhantomJS):
    def get(self, url):
        super().get(url)
        time.sleep(5)
        return self.page_source
    
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
