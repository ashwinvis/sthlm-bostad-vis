from selenium import webdriver
import time
import signal


class Render(webdriver.PhantomJS):
    def get(self, url):
        super().get(url)
        time.sleep(5)
        return self.page_source
    
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete_all_cookies()

        # kill the specific phantomjs child process
        self.service.process.send_signal(signal.SIGTERM)

        # quit the node process
        self.quit()
