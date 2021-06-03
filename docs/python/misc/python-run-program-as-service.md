---
reference:
  - https://websofttechs.com/tutorials/how-to-setup-python-script-autorun-in-ubuntu-18-04/
  - https://tecadmin.net/setup-autorun-python-script-using-systemd/
  - https://realpython.com/python-logging/
---

# How to run a Python program as Linux Service

## Create Python program

```bash
$ sudo vi /usr/bin/test_service.py
```



```python
import time
import logging

logging.basicConfig(level=logging.INFO, filename='/var/log/test-py.log', 
    filemode='a', format='%(asctime)s:%(name)s:%(levelname)s:%(message)s', 
    datefmt='%d-%b-%y %H:%M:%S')

step = 0
while True:
  step += 1
  logging.info(f"Processing step {step}.")
  time.sleep(2)
```



## Create Service Definition

```bash
$ sudo vi /lib/systemd/system/test-py.service
```



```
[Unit]
Description=Test Service
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=python3 /home/root/test_service.py >> /var/log/test-py.log
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
```

## Enable and Start the Service

First you need to reload the systemctl daemon to read the new service definition.

```bash
$ sudo systemctl daemon-reload
```

In case you update the service definition, you need to reload the systemctl daemon for updates to take effect.

Now you can enable and start the service:

```bash
$ sudo systemctl enable test-py.service
$ sudo systemctl start test-py.service
```

You can monitor the log:

```bash
$ sudo tail -f /var/log/test-py.log
03-Jun-21 16:43:52:root:INFO:Processing step 1.
03-Jun-21 16:43:54:root:INFO:Processing step 2.
03-Jun-21 16:43:56:root:INFO:Processing step 3.
03-Jun-21 16:43:58:root:INFO:Processing step 4.
...
```

## Managing the Service

You can start, stop, restart the service or get the service status:

```bash
$ sudo systemctl start test-py.service
$ sudo systemctl status test-py.service
$ sudo systemctl restart test-py.service
$ sudo systemctl stop test-py.service
```

