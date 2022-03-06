# Abby
This is my personal Discord bot. I doubt anyone would ever have the need to
install this. However, here are some basic directions to get started.

## Set-up Environment
Create virtual environment:
```bash
git clone https://github.com/thetallguyyy/abby.git
cd abby
python3 -m venv ./venv
source venv/bin/activate
```

## Install Requirements
```bash
pip install -r requirements.txt
deactivate
```

## Configure
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

## Install
```
sudo chmod +x install.sh
sudo ./install.sh
sudo systemctl enable abby
```

Verify that everything went well
```
systemctl status abby
```
