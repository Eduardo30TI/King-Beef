import requests
from base64 import b64decode
import os
from glob import glob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
import pyautogui as gui
import time

link='https://ws.meudanfe.com/api/v1/get/nfe/xmltodanfepdf/API'
header={'Content-Type':'text/plain'}

class Danfe:

    def NFe(self,xml,nota):

        response=requests.post(link,data=xml,headers=header)
        b64=response.json()
        bytes=b64decode(b64,validate=True)

        path_base=os.path.join(os.getcwd(),'XML')
        os.makedirs(path_base,exist_ok=True)
        temp_path=os.path.join(path_base,f'{nota}.pdf')

        with open(temp_path,'wb') as file:

            file.write(bytes)

            pass


        return temp_path

        pass

    def downloadXML(self,chave):

        href='https://meudanfe.com.br/'

        service=Service()
        options=webdriver.ChromeOptions()

        prefs = {"download.default_directory" : os.getcwd(),"download.prompt_for_download": False, "download.directory_upgrade": True, "safebrowsing.enabled":True}
        options.add_experimental_option("prefs",prefs)
        options.add_argument("test-type")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument('--headless')

        with webdriver.Chrome(service=service,options=options) as driver:

            driver.get(href)
            driver.maximize_window()

            campo=WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.XPATH,'//*[@id="get-danfe"]/div/div/div[1]/div/div/div/input'))
            campo.send_keys(chave)
            time.sleep(1)

            for xpath in ['//*[@id="get-danfe"]/div/div/div[1]/div/div/div/button','/html/body/div[1]/div/div[1]/div/div[2]/button[1]']:

                btn=WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.XPATH,xpath))
                btn.click()
                time.sleep(3)

                pass

            temp_path=os.path.join(os.getcwd(),f'{chave}.xml')

            time.sleep(10)

            pass

        return temp_path

        pass

    pass