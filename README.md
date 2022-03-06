# Abby
This is my personal Discord bot. I doubt anyone would ever have the need to
install this. However, here are some basic directions to get started.

### Set-up Environment
```
git clone https://github.com/thetallguyyy/abby.git
cd abby
python3 -m venv ./venv
```

### Install Requirements
```
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### Configure
Edit the following lines in default.config.py
```python
class Client(object):
    prefix = ''
    description = ''
    token = ''
```

Rename default.config.py to config.py
```
cp default.config.py to config.py
```

### Verify Configuration
```
sudo chmod +x ./abby.py
./abby.py
```

### Install
```
sudo chmod +x install.sh
sudo ./install.sh
sudo systemctl enable abby
```

### Verify systemd is Working
```
systemctl status abby
sudo journalctl -u abby
```
