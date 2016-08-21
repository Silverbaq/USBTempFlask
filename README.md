# USBTempFlask

This is a small webapplication, build with Flask. The point is, to have a USB Termometer connected to a Raspberry Pi (Or what every you wish). It will then record the temperature, every 15 minuts.

# Image
![Image of running application](https://octodex.github.com/images/yaktocat.png)

# Dependencies

For now, this is using the temper-python: https://github.com/padelt/temper-python - The plan is to move away from it. But for now, it's needed.

# Installation

```
sudo apt-get update

sudo apt-get install python2.7 python-pip

sudo pip install flask flask_sqlalchemy flask_bootstrap 

```

# Run
```
cd USBTempFlask
sudo python USBTempFlask.py
```



