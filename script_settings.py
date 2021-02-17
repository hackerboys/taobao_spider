#encoding:utf-8
from bs4 import BeautifulSoup
import requests
import json
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
import re
import os
import ast
import random
import pandas as pd
from selenium import webdriver
# from setting.loggin_deom import *
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from setting.program_tools import tools
from setting.program_tools import xsh_att_pro
import os

root_paths = os.path.dirname(__file__)


tool = tools() # 实例化工具对象


#########################################
#       本页代码不能随意改动和删除           #
#########################################

taobao_baby_path = r"D:\taobao_data" #淘宝宝贝保存位置

while True:
    if os.path.isdir(taobao_baby_path):
        break
    else:
        os.makedirs(taobao_baby_path)




