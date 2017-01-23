from sys import argv
import time
try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QUrl
    from PyQt5.QtWebKitWidgets import QWebPage
except ImportError:
    from PyQt4.QtGui import QApplication
    from PyQt4.QtCore import QUrl
    from PyQt4.QtWebKit import QWebPage


class Render(QWebPage):
    def __init__(self):
        self.app = QApplication(argv)
        super(QWebPage, self).__init__()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        time.sleep(5)
        self.app.quit()

    def get(self, url):
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()
        return self.frame.toHtml()
