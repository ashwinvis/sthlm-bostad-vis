import time
import signal
import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class Render(webdriver.Firefox):
    def __init__(self):
        os.environ["MOZ_HEADLESS"] = "1"
        binary = FirefoxBinary()
        binary.add_command_line_options("-headless")
        super(Render, self).__init__(firefox_binary=binary)

    def get(self, url):
        super().get(url)
        time.sleep(5)
        return self.page_source

    def __enter__(self):
        print("Running Firefox headless...")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete_all_cookies()

        # kill the specific phantomjs child process
        self.service.process.send_signal(signal.SIGTERM)

        del os.environ["MOZ_HEADLESS"]

        print("Exiting Firefox.")
        # quit the node process
        self.quit()
