#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys, time, traceback
    
class WFinalException(Exception):
    pass
    
class WWrapper:
    __error         = 0

    @staticmethod
    def error       ():
        return WWrapper.__error

    def __init__    (self, title="default", continue_on_error=True, onError=None, onQuit=None):
        self.__continue_on_error = continue_on_error
        self.__on_error          = onError
        self.__on_quit           = onQuit
        self.__title             = title
        self.__text              = ""
        self.__start             = time.time()
        self.__already_on_exit   = False
        
    @property
    def title       (self):
        return self.__title

    @property
    def text        (self):
        return self.__text

    @text.setter
    def text        (self, value):
        self.__text = value
        
    def __enter__   (self):
        self.__start= time.time()
        return self
    
    def __exit__    (self, type, value, trace):
        elapsed = (float)(time.time() - self.__start)
        if self.__already_on_exit:
            pass
        elif type is None:
            self.__already_on_exit          = True
            print ("%-10s - %-50s - %06.2fs" % (self.title, self.text, elapsed))
            return   True
        elif isinstance (value, KeyboardInterrupt):
            self.__already_on_exit          = True
            print ("%-10s - %-50s - %06.2fs" % (self.title, "INTERRUPT",   elapsed))
            if  self.__on_quit:
                self.__on_quit()
            raise  value
        elif isinstance (value, WFinalException):
            self.__already_on_exit          = True
            WWrapper.__error                = WWrapper.__error + 1 
            print ("%-10s - %-50s - %06.2fs" % (self.title, "FATAL",   elapsed))
            if  self.__on_quit:
                self.__on_quit()
            return False
        else: 
            self.__already_on_exit          = True
            WWrapper.__error                = WWrapper.__error + 1 
            print ("%-10s - %-50s - %06.2fs" % (self.title, "ERROR",   elapsed))
            traceback.print_exception       (type, value, trace, None, sys.stdout)
            
            if self.__on_error: 
                self.__on_error   (self.title)
            
            if not self.__continue_on_error and self.__on_quit:
                self.__on_quit    ()
                        
            return self.__continue_on_error


# In[ ]:


import os
from   selenium                                import webdriver
from   selenium.webdriver.common.action_chains import ActionChains
from   selenium.webdriver.common.keys          import Keys
from   selenium.webdriver.remote.command       import Command
from   selenium.webdriver.chrome.options       import Options
from   selenium.webdriver.support              import expected_conditions
from   selenium.webdriver.common.by            import By
from   selenium.webdriver.support.ui           import WebDriverWait
from   selenium.common.exceptions              import TimeoutException
from   selenium.common.exceptions              import WebDriverException
from   selenium.common.exceptions              import NoSuchElementException
from   selenium.common.exceptions              import StaleElementReferenceException

class  element_to_be_clickable(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = expected_conditions.visibility_of_element_located(self.locator)(driver)
        try:
            if element and element.is_enabled():
                return element
            else:
                return False
        except WebDriverException:
            return False

class  element_to_be_stale    (object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = expected_conditions.presence_of_element_located(self.locator)(driver)
        try:
            if element and element.is_enabled():
                return element
            else:
                return False
        except WebDriverException:
            return False
        
def    findElement            (search, by = By.ID, timeout = 10):
    return     WebDriverWait  (driver, timeout).until (element_to_be_stale                                  ((by, search)))

def    findElements           (search, by = By.ID, timeout = 10):
    try:    
        return WebDriverWait  (driver, timeout).until (expected_conditions.presence_of_all_elements_located ((by, search)))
    except WebDriverException:
        return []


# In[ ]:


import datetime, sys

try:
    __file__
    if len(sys.argv) < 2:
        print        ("missing parameter, remote chromedriver url must be defined")
        sys.exit     (1)
    remote_url       = sys.argv[1]
    driver_args      = sys.argv[2:]
except NameError:
    remote_url       = "http://127.0.0.1:4444"
    driver_args      = [ "--no-sandbox", "--disable-gpu", "--disable-extensions", "--window-size=1600,900" ]

with WWrapper("INIT", False)        as ww:
    try:
        current_folder      = os.path.dirname (os.path.realpath(__file__))
    except NameError:
        current_folder      = os.path.realpath('.')

    #set web driver
    options                 = Options()
    for arg in driver_args:
        options.add_argument(arg)
    driver                  = webdriver.Remote (command_executor = remote_url, options = options)
    driver.execute          (Command.SET_TIMEOUTS, { 'ms' : float(60 * 1000), 'type' : 'page load' } )
    
    ww.text                 = "Init  web driver"
    
    def onError     (title):
        src_page        = driver.page_source.encode('utf-8')
        if src_page and src_page.strip():
            src_file    = os.path.join (current_folder, u"debug-" + title + "-" + time.strftime("%Y%m%d-%H%M%S") + ".html")
            with open   (src_file, "wb") as f:
                f.write (src_page)
            
        print ("%-8s - DEBUG html file: %s" % (title, src_file))
        
    def onQuit      ():
        try:
            driver.stop_client ()
        except WebDriverException:
            pass
        try:
            driver.close       ()
        except WebDriverException:
            pass
        try:
            driver.quit        ()
        except WebDriverException:
            pass


# In[ ]:


with WWrapper("LOGIN", False, onError, onQuit)        as ww:
    driver.get           ("https://github.com/login")
    
    login                = findElement ("login_field",  By.ID)
    login.clear          ()
    login.send_keys      ("my@email.com")
    
    password             = findElement ("password",     By.ID)
    password.clear       ()
    password.send_keys   ("1234")
    
    login                = findElement ("commit",       By.NAME)
    login.click          ()
    
    ww.text              = "Go to page and login"

# In[ ]:


with WWrapper("CLEAN", False, onError)         as ww:
    onQuit  ()
    ww.text = "Close web driver"


# In[ ]:


try:
    __file__
    sys.exit (WWrapper.error())
except NameError:
    pass
