# Abby
This is my personal Discord bot. I doubt anyone would ever have the need to
install this. However, here are some basic directions to get started.

## Install Requirements
```
pip install -r requirements.txt
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
