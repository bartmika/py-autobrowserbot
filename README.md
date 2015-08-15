# py-autobrowserbot
## Description
Python script which simulates browsing on a network for administrators to test out their firewalls filter setting / ruleset settings


## Features
* Supports HTTP / HTTPS GET requests
* Large list of safe wbsites to vist
* Large list of bad words to avoid in a URL


## System Requirements
* Python 3.4.x+
* pip 6.1.1+
* virtualenv 12.1.1+


## Dependencies
* urllib3 1.11
* certifi 2015.04.28
* beautifulsoup4 4.4.0

## Build Instructions
1. First clone the project locally and then go into the directory
```
$ git clone https://github.com/bartmika/py-autobrowserbot.git
$ cd py-autobrowserbot
```

2. Setup our environment:
```
(OSX)
$ python3 -m venv env

(Linux/FreeBSD)
$ virtualenv env
```

3. Activate "virtualenv" for this script:
```
$ source env/bin/activate
```

4. Confirm we are using Python3
```
(env) python --version  # Should return Python 3.x
```

5. Now let's install the required libraries:
```
(env) pip3 install -r requirements.txt
```

### Usage
To run the application, simply enter the following line:
```
(env) python autobrowserbot.py
```

## Extra
If you would like to have a dedicated Raspberry Pi running this script, read how to make such a setup here:  [raspberrypi_setup.md](raspberrypi_setup.md).

## License
MIT


## Donate
* Bitcoin: 17VEy2fps6nJCUhWsvhJ4h42omWMJZUjcm
