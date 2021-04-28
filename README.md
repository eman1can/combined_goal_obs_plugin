# Combined Goal OBS Plugin
A OBS Overlay that interfaces with Twitch to combine multiple goal widgets into one

Created by Ethan Wolfe
Please do not redistribute this freely. You CAN do that, but likely people will break it. It is a fragile baby, and if you do want to distribute it to people, please make sure that have a way to contact me (Issues on this repository works) to be able to resolve any installation or user errors they may encounter.

Currently has support for bits and donations

Requires:
  OBS-Studio
  Python 3.6.8 (https://www.python.org/downloads/release/python-368/)
    - Selenium (3.141.0)
    - pywin32 (300)
    - A streamlabs account
  
# Installation instructions
1. Find a safe place you want the files to be located. This needs to be outside the programs files folder. I reccommend an out of the way location that wont get in the way or be accidentally deleted such as 'C:/Users/user/OBS Plugins/' or similar
2. Download the code and unzip into your safe location. There should be seven files.
5. Navigate to '%LocalAppData%/Programs/Python/Python36`
6. Install Required Python Packages
7. Open a command terminal
  - run `cd C:\Users\User\AppData\Local\Programs\Python\Python36`
  - run `python -m pip install selenium`
  - run `python -m pip install pywin32`
  - Close the terminal Go back to windows explorer
8. From `Python36` Navigate to `Lib\site-packages\selenium\webdriver\common`
9. Copy the `service.py` file from your safe place into the foler, overwriting the current file
10. Go to your safe place and open `obs_plugin.py` in your favorite text editor
11. Find line 22 that says `WORKING_PATH = 'C:/Users/Zoe/Desktop/Custom Goal Bar'`
12. Change the Path to be your safe place, and make sure to have FORWARD (/) and NOT backward (\) slashes. Saves the file and exit.
13. Close the Explorer window and open OBS
14. Go to `Tools → Scripts → Python Settings`
15. Enter `C:/Users/User/AppData/Local/Programs/Python/Python36` into the bar
16. Go to `Scripts`
17. Click the plus at the bottom left. Navigate to your safe place. Select `obs_plugin.py` and load it.
18. Wait for the plugin to load, and then fill in the values for how you want the bar to be customized
19. Make sure to add a end date in the format (mm/dd/yy)
20. Go to `https://streamlabs.com/dashboard#/alertbox` and copy your url token into the Alert Url box
21. Go to the first scene that you want to have your goal bar on and create a browser source.
22. Set the Local File checkbox and open the `bar.html` file as your file. Your bar with all your customized options should be displayed. Have fun!

Please try to contact me if you get stuck anywhere or just have any questions!

WARNINGS
Due to the workaround that requires all this shitty importing and stuff, you need to be careful when clicking reload. When the script os loaded by OBS, it runs a web service (Selenium) in the background to listen for the alerts. Clicking reload SHOULD (untested) stop any running web services, but may just propagate and cause memory issues. If this happens, a quick restart of OBS is all that is needed. Of Course, if you stay away from that pesky reload button that will run the script again, you will never encoutner this issue.
