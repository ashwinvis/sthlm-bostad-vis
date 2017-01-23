# STHLM Bostad Vis
Visualize the stockholm housing queue

## Dependencies
* lxml
* pandas
* PyTables (to cache in HDF5 format)
* PyQt4 / PyQt5 (for SSSB)

## Setup email
```bash
export PYEMAIL_SERVER=smtp.mailserver.com
export PYEMAIL_USER=username
export PYEMAIL_PASSWD=password
```

## Schedule crontab
```bash
@hourly cd /path/to/sthlm-bostad-vis && /usr/bin/xvfb-run /usr/bin/python sssb.py
@daily cd /path/to/sthlm-bostad-vis && ./pyemail -d cache -s user@mailserver.com -r receiver@otherserver.com
```
