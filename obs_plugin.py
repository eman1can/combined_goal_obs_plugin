###
#
# Written by Ethan Wolfe 4/27/21
# Combine different donation types into one goal bar.
#
###

# Import stuff to run
import obspython as obs
import time
from datetime import datetime
from selenium import webdriver
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import subprocess
from selenium.webdriver.chrome.options import Options

# Variables
# CONSTANTS
WORKING_PATH = 'C:/Users/Zoe/Desktop/combined_goal_obs_plugin'
CHROME_DRIVER = WORKING_PATH + '/chromedriver.exe'
# Other Variables
bits_to_money = 0.0  # How much a single bit is worth
t1sub_to_money = 0.0  # How much a single bit is worth
t2sub_to_money = 0.0  # How much a single bit is worth
t3sub_to_money = 0.0  # How much a single bit is worth
psub_to_money = 0.0  # How much a single bit is worth
reload_interval = 0  # in ms; How often to refresh bar
font_name = ''  # What font to use
bar_thickness = 48  # in px, how tall the bar is
# -- colors --
text_color = '#FFFFFF'  # In Hex
bar_text_color = '#000000'
bar_color = '#46E65A'
bar_background_color = '#DDDDDD'

# Goal Options
alert_url = ''
pjonk_money = 0
goal_start = 0
goal_end = 1500
goal_title = 'New Gpu!'
goal_end_date = '07/31/2021'

print(os.getcwd())

# ------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------

# Strips HTML style tags to leave only the alert text
def remove_tag(string):
    if '<' not in string:
        return string
    string = string[:string.index('<')] + string[string.index('>') + 1:]
    if string != '':
        return remove_tag(string)
    return string

# Turns a Hex color into rgb
def get_rgb(hex_string):
    return tuple(int(hex_string.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

# ------------------------------------------------------------
# CODE BELOW
# ------------------------------------------------------------

# Starts the browser for updates and sets it to the alert url
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'browser':'ALL' }
driver = webdriver.Chrome(CHROME_DRIVER, desired_capabilities=d, options=chrome_options)
if alert_url != '':
    driver.get(alert_url)

# Update the bar.html file
def check_for_updates():
    global bits_to_money
    global t1sub_to_money
    global t2sub_to_money
    global t3sub_to_money
    global psub_to_money
    global goal_current
    global driver

    for entry in driver.get_log('browser'):
        # The Alert Volume is broadcast every alert and is how I detect alerts
        if 'Alert volume' in entry['message']:
            # Then, we scrape through the alert to get the alert message
            driver.switch_to.frame(driver.find_element(By.ID, "sl_frame"))
            wrapped_element=driver.find_element(By.ID, "wrap")
            html_string = wrapped_element.find_element(By.ID, "alert-message").get_attribute('innerHTML')
            alert_string = remove_tag(html_string).strip()
            driver.switch_to.default_content()
            
            # Output the Alert Message for debugging
            print(alert_string)
            
            # Change PJNOK Money based on Alert Items
            if 'cheered!' in alert_string:  # Ex. Eman1can cheered x1000
                # We have bits update
                print('Add', round(float(alert_string[alert_string.index('x') + 1:]) * bits_to_money, 2), 'to goal')
                goal_current += round(float(alert_string[alert_string.index('x') + 1:]) * bits_to_money, 2)
            elif 'donated' in alert_string: # Ex. Eman1can donated $1000
                # We have donation update
                print('Add', float(alert_string[alert_string.index('$') + 1:-1]), 'to goal')
                goal_current += float(alert_string[alert_string.index('$') + 1:-1])
            elif 'gifted' in alert_string: # Ex. Eman1can gifted a sub to firefox | Eman1can gifted 3 subs to community
                if 'monthly prime subscription' in alert_string:
                    goal_current += psub_to_money
                    print('Add', psub_to_money, 'to goal')
                else:
                    amount = alert_string[alert_string.index('gifted') + 7:]
                    amount = amount[:amount.index(' ')]
                    if amount == 'a':
                        amount = 1
                    else:
                        amount = int(amount)
                    if 'tier 3' in alert_string:
                        print('Add', amount * t3sub_to_money, 'to goal')
                        goal_current += amount * t3sub_to_money
                    elif 'tier 2' in alert_string:
                        print('Add', amount * t2sub_to_money, 'to goal')
                        goal_current += amount * t2sub_to_money
                    else:
                        print('Add', amount * t1sub_to_money, 'to goal')
                        goal_current += amount * t1sub_to_money
            elif 'resubbed' in alert_string or 'subscribed' in alert_string: # Ex. Eman1can resubbed at tier 3; Eman1can subscribed at tier 2
                if 'tier 3' in alert_string:
                    print('Add', t3sub_to_money, 'to goal')
                    goal_current += t3sub_to_money
                elif 'tier 2' in alert_string:
                    print('Add', t2sub_to_money, 'to goal')
                    goal_current += t2sub_to_money
                else:
                    print('Add', t1sub_to_money, 'to goal')
                    goal_current += t1sub_to_money

            update_bar()

def update_bar():
    global reload_interval
    global alert_url
    
    global goal_title
    global goal_start
    global goal_end
    global goal_current
    global goal_end_date
    
    global font_name
    global bar_thickness
    global text_color
    global bar_text_color
    global bar_color
    global bar_background_color

    current_percent = round((int(goal_current) - goal_start) / goal_end * 100, 2)

    current_day = datetime.now()
    goal_end_time = datetime.strptime(goal_end_date, '%m/%d/%y')
    time_left = f'{(goal_end_time - current_day).days} Days Left!'
    file = open(WORKING_PATH + '/bar.html', 'w')
    html_output = '''
    <head>
    <script>
    function reload(){
        location.href=location.href
    }''' + f'''
    setInterval('reload()', {int(reload_interval * 1000)})
    </script>
    <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    ''' + f'''
    <body>
    <div style="padding: 10px 20px;">
        <div class="standard__title" style="color: rgb{str(get_rgb(text_color))}; font: 800 22px / 1px &quot;{font_name}&quot;;">{goal_title}</div>
        <div class="standard__container" style="height: {bar_thickness}px; background: rgb{str(get_rgb(bar_background_color))};"><div class="standard__current__amount" style="color: rgb(0, 0, 0); font: 800 28px / {bar_thickness}px &quot;{font_name}&quot;;">{round(goal_current, 2)} PM ({current_percent}%)</div>
            <div style="height: 100%; width: 100%; position: absolute; top: 0px; left: 0px; z-index: 10; box-shadow: rgb(0, 0, 0) 0px 0px 2px inset;"></div>
            <div class="donation-bar standard__bar" style="background: linear-gradient(transparent, rgba(0, 0, 0, 0.15)) rgb{str(get_rgb(bar_color))}; width: {int(current_percent)}%;"></div>
        </div>
        <div class="standard__start" style="color: rgb{str(get_rgb(text_color))}; font: 800 18px / 32px &quot;{font_name}&quot;;">{time_left}
            <div style="color: rgb{str(get_rgb(text_color))}; font: 800 28px / 32px &quot;{font_name}&quot;; float: left;">{goal_start}</div>
            <div class="standard__amount">{goal_end}</div>
        </div>
    </div>
    </body>'''
    file.write(html_output)
    file.close()

# Get the description to display to users
def script_description():
	return "Add together different support types into one goal bar.\n\nBy Ethan Wolfe"

def reset_pressed(props, prop):
    global goal_current
    goal_current = 0
    update_bar()

def add_bit_to_goal(props, prop):
    global goal_current
    global bits_to_money
    goal_current += bits_to_money
    update_bar()

# Called to update the local variables on property changes
def script_update(settings):
    global bits_to_money
    global t1sub_to_money
    global t2sub_to_money
    global t3sub_to_money
    global psub_to_money
    global reload_interval
    global alert_url
    
    global goal_title
    global goal_start
    global goal_end
    #global goal_current
    global goal_end_date
    
    global font_name
    global bar_thickness
    global text_color
    global bar_text_color
    global bar_color
    global bar_background_color

    bits_to_money = obs.obs_data_get_double(settings, "bits_to_money")
    t1sub_to_money = obs.obs_data_get_double(settings, "t1sub_to_money")
    t2sub_to_money = obs.obs_data_get_double(settings, "t2sub_to_money")
    t3sub_to_money = obs.obs_data_get_double(settings, "t3sub_to_money")
    psub_to_money = obs.obs_data_get_double(settings, "psub_to_money")
    reload_interval = obs.obs_data_get_double(settings, "reload_interval")
    alert_url = obs.obs_data_get_string(settings, "alert_url")
    
    goal_title = obs.obs_data_get_string(settings, "goal_title")
    goal_start = obs.obs_data_get_int(settings, "goal_start")
    goal_end = obs.obs_data_get_int(settings, "goal_end")
    goal_end_date = obs.obs_data_get_string(settings, "goal_end_date")
    
    font_name = obs.obs_data_get_string(settings, "font_name")
    bar_thickness = obs.obs_data_get_int(settings, "bar_thickness")
    text_color = obs.obs_data_get_string(settings, "text_color")
    bar_text_color = obs.obs_data_get_string(settings, "bar_text_color")
    bar_color = obs.obs_data_get_string(settings, "bar_color")
    bar_background_color = obs.obs_data_get_string(settings, "bar_background_color")
    
    obs.timer_remove(check_for_updates)
    update_bar()

    if alert_url != "" and goal_end_date != "":
        driver.get(alert_url)
        obs.timer_add(check_for_updates, int(reload_interval * 1000))
    
# Called to set the defualt values of the options
def script_defaults(settings):
    obs.obs_data_set_default_double(settings, "bits_to_money", 0.01)
    obs.obs_data_set_default_double(settings, "t1sub_to_money", 3.99)
    obs.obs_data_set_default_double(settings, "t2sub_to_money", 5.99)
    obs.obs_data_set_default_double(settings, "t3sub_to_money", 9.99)
    obs.obs_data_set_default_double(settings, "psub_to_money", 2.99)
    obs.obs_data_set_default_double(settings, "reload_interval", 2.5)
    
    obs.obs_data_set_default_string(settings, "goal_title", 'My Sample Goal')
    obs.obs_data_set_default_int(settings, "goal_start", 0)
    obs.obs_data_set_default_int(settings, "goal_end", 100)

    obs.obs_data_set_default_string(settings, "font_name", 'Open Sans')
    obs.obs_data_set_default_int(settings, "bar_thickness", 48)
    
    obs.obs_data_set_default_string(settings, "text_color", 'FFFFFF')
    obs.obs_data_set_default_string(settings, "bar_text_color", '000000')
    obs.obs_data_set_default_string(settings, "bar_color", '46E65A')
    obs.obs_data_set_default_string(settings, "bar_background_color", 'DDDDDD')

# Creates the properties widget for customizing options
def script_properties():
    props = obs.obs_properties_create()
    # General Settings
    obs.obs_properties_add_float(props, "bits_to_money", "Bits to Currency", 0.01, 100.0, 0.01)
    obs.obs_properties_add_float(props, "t1sub_to_money", "T1 Subscription to Currency", 0.01, 100.0, 0.01)
    obs.obs_properties_add_float(props, "t2sub_to_money", "T2 Subscription to Currency", 0.01, 100.0, 0.01)
    obs.obs_properties_add_float(props, "t3sub_to_money", "T3 Subscription to Currency", 0.01, 100.0, 0.01)
    obs.obs_properties_add_float(props, "psub_to_money", "Prime Subscription to Currency", 0.01, 100.0, 0.01)
    obs.obs_properties_add_float(props, "reload_interval", "Reload Interval (Seconds)", 1, 1000, 1)
    obs.obs_properties_add_text(props, "alert_url", "Alert Url", obs.OBS_TEXT_DEFAULT)

    # Goal specific settings
    obs.obs_properties_add_text(props, "goal_title", "Title", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_int(props, "goal_start", "Start", 0, 1000000, 1)
    obs.obs_properties_add_int(props, "goal_end", "End", 0, 1000000, 1)
    obs.obs_properties_add_text(props, "goal_end_date", "End Date", obs.OBS_TEXT_DEFAULT)
    
    # Style Settings
    obs.obs_properties_add_text(props, "font_name", "Font Name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_int(props, "bar_thickness", "Bar Thickness", 10, 1000, 1)
    
    obs.obs_properties_add_text(props, "text_color", "Text Color", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "bar_text_color", "Bar Text Color", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "bar_color", "Bar Color", obs.OBS_TEXT_DEFAULT)  
    obs.obs_properties_add_text(props, "bar_background_color", "Bar Background Color", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_button(props, "button", "Reset Goal", reset_pressed)
    obs.obs_properties_add_button(props, "add_button", "Add current Bit exchange to goal", add_bit_to_goal)
    return props

def script_unload():
    global driver
    driver.quit()
    driver = None

def script_load(settings):
    global goal_current
    goal_current = obs.obs_data_get_double(settings, "goal_current")

def script_save(settings):
    global goal_current
    obs.obs_data_set_double(settings, 'goal_current', goal_current)