# STHLM Bostad Vis
Visualize the stockholm housing queue

Currently supports parsing:

* SSSB

![Web scrapping SSSB](https://ashwinvis.github.io/sthlm-bostad-vis/doc/example_sssb.svg)

## Quick start

```bash
pipenv install
python run_sssb.py
```

If you have most of the non-Python dependencies pre-installed in your system,
this would work. Otherwise follow the installation instructions below.
Parameters can be modified in `main.py`.

## Installation

### Dependencies
* lxml
* pandas
* PyTables (to cache in HDF5 format)
* One of the following to execute JavaScript:
  - PyQt4 / PyQt5, Qt-Base and Qt-Webkit (option 1)
  - selenium, geckodriver and Firefox (option 2)
* matplotlib (for plotting)
* xorg-server-xvfb (optional, for running in a virtual X server)

### ArchLinux
```bash
sudo pacman -S python-lxml python-pandas python-pytables python-matplotlib
sudo pacman -S qt5-webkit python-pyqt5
sudo pacman -S python-selenium geckodriver firefox
sudo pacman -S xorg-server-xvfb
```

### Setup email
Requires a mail server:
```bash
export PYEMAIL_SERVER=smtp.mailserver.com
export PYEMAIL_USER=username
export PYEMAIL_PASSWD=password
```

### Schedule crontab
```bash
@hourly cd /path/to/sthlm-bostad-vis && /usr/bin/xvfb-run /usr/bin/python sssb.py
@daily cd /path/to/sthlm-bostad-vis && ./pyemail -d cache -s user@mailserver.com -r receiver@otherserver.com
```
