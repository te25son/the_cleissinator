import os
import json
import shutil
import requests
import time as t
import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from .logger import setup_logger


class Cleissinator:

    def __init__(self, driver, wait_time, download_dir, url, username, password, folder_dict):
        self.url = url
        self.driver = driver
        self.username = username
        self.password = password
        self.download_dir = download_dir
        self.folder_dict = folder_dict
        self.wait = WebDriverWait(self.driver, wait_time)
        self.json_filename = 'files_database.json'

        setup_logger('daily_log', 'daily_log.log', mode='w')
        setup_logger('full_log', 'full_log.log')

        self.daily_log = logging.getLogger('daily_log')
        self.full_log = logging.getLogger('full_log')

    def open_url(self):
        self.driver.get(self.url)
        self.wait.until(
            EC.visibility_of_element_located((
                By.ID, 'element_1'
            ))
        )

    def login_to_home_portal(self):
        self.driver.find_element_by_id('element_1').send_keys(self.username)
        self.driver.find_element_by_id('element_2').send_keys(self.password)
        self.driver.find_element_by_id('element_2').submit()
        self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH, '//span[contains(text(), "Traductions")]'
            ))
        )

    def click_dropdown_link_to_translations_page(self):
        link_to_docs = self.driver.find_element_by_xpath(
            '//a[@href="suivi/table_doc_encours.php"]'
        )
        self.driver.execute_script('arguments[0].click()', link_to_docs)
        self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH, '//h1[contains(text(), "Liste des demandes en cours")]'
            ))
        )

    def click_dropdown_link_to_certifications_page(self):
        link_to_certs = self.driver.find_element_by_xpath(
            '//a[@href="suivi/table_cert_encours.php"]'
        )
        self.driver.execute_script('arguments[0].click()', link_to_certs)
        self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH, '//h1[contains(text(), "Liste des demandes en cours")]'
            ))
        )

    def check_if_trans_or_cert(self):
        status = ''
        if 'table_doc_encours' in self.driver.current_url:
            status = 'trans'
        elif 'table_cert_encours' in self.driver.current_url:
            status = 'certs'
        else:
            status = ''
        return status

    def get_most_recently_downloaded_file(self):
        time_counter = 0
        while not [file for file in os.listdir(self.download_dir) if '.pdf' in file]:
            time_counter += 1
            t.sleep(1)
            if time_counter > 120:
                raise "ABORT: File did not appear in download directory."
        return max(
            [file for file in os.listdir(self.download_dir) if '.pdf' in file],
            key=lambda file_name_only: os.path.getctime(
                os.path.join(self.download_dir, file_name_only)
            )
        )

    def most_recent_download_size_is_zero(self):
        most_recent_download = self.get_most_recently_downloaded_file()
        if os.stat(os.path.join(self.download_dir, most_recent_download)).st_size == 0:
            return True
        else:
            return False

    def move_and_rename_downloaded_file_as_translation(self, type, lang, local):
        time_counter = 0
        while self.most_recent_download_size_is_zero():
            time_counter += 1
            t.sleep(1)
            if time_counter > 120:
                raise "ABORT: Waited to long for file to download"

        most_recent_download = self.get_most_recently_downloaded_file()
        newfilename = type + lang + '_' + most_recent_download

        self.full_log.info(f"Downloaded file {most_recent_download}")

        if lang in self.folder_dict.keys():
            if local == 'trans':
                move_to_folder = os.path.join(self.download_dir, self.folder_dict[lang][0])
            else:
                move_to_folder = os.path.join(self.download_dir, self.folder_dict[lang][1])
        else:
            move_to_folder = os.path.join(self.download_dir, 'MISC_FILES')
        try:
            shutil.move(
                os.path.join(self.download_dir, most_recent_download),
                os.path.join(move_to_folder, newfilename)
            )
            self.full_log.info(f"Moved {most_recent_download} to {move_to_folder} and renamed as {newfilename}")

            return True

        except:
            self.full_log.error(f"Failed to move {most_recent_download} to {move_to_folder}")
            os.remove(os.path.join(self.download_dir, most_recent_download))

            return False

    def download_documents_from_page(self):
        rows = self.driver.find_elements_by_tag_name('tr')[1:]
        local = self.check_if_trans_or_cert()
        rename_dict = {'trans': 'TRAD_', 'certs': 'CERTS_'}
        if local == None:
            raise "Unable to determine the page location."
        else:
            for row in range(len(rows)):
                if self.driver.title == 'Demande de traduction':
                    self.login_to_home_portal()
                    if local == 'trans':
                        self.click_dropdown_link_to_translations_page()
                    else:
                        self.click_dropdown_link_to_certifications_page()
                    self.download_documents_from_page()
                else:
                    doc = rows[row].find_elements_by_xpath('.//td')[1].find_element_by_xpath('.//a')
                    lang = rows[row].find_elements_by_xpath('.//td')[2].text.lower()
                    type = rename_dict[local]
                    filename = rows[row].find_elements_by_xpath('.//td')[0].text

                    self.driver.execute_script('arguments[0].scrollIntoView()', doc)
                    if self.file_has_not_been_previously_downloaded(filename):

                        self.full_log.info(f"Clicking on file {filename}")

                        doc.click()
                        success = self.move_and_rename_downloaded_file_as_translation(type, lang, local)

                        if success:
                            # only write file to json if file successfully moved to correct folder
                            self.write_download_to_json_file(self.json_filename, filename)

                            self.daily_log.info(f"Successfully downloaded file {filename}")
                            self.full_log.info(f"Successfully downloaded file {filename}")
                        else:
                            self.daily_log.error(f"Unable to download file {filename}")
                            self.full_log.error(f"Unable to download file {filename}")

                    else:
                        pass
                    if (row + 1) == len(rows) and local != 'certs':
                        self.driver.execute_script("window.history.go(-1)")
                        self.wait.until(
                            EC.visibility_of_element_located((
                                By.XPATH, '//span[contains(text(), "Certifications")]'
                            ))
                        )
                        self.click_dropdown_link_to_certifications_page()
                        self.download_documents_from_page()
                    if (row + 1) == len(rows) and local == 'certs':
                        self.driver.quit()


    def get_data_from_json(self, jsonfile):
        with open(jsonfile) as file:
            return json.load(file)

    def write_download_to_json_file(self, jsonfile, filename):

        def write_data_to_json(data):
            with open(jsonfile, 'w') as file:
                json.dump(data, file, indent=4)

        def append_to_data_set(*args):
            datastore = self.get_data_from_json(jsonfile)
            if len(datastore['filename']) >= 1000:
                datastore['filename'] = datastore['filename'][500:]
            for arg in args:
                if arg in datastore['filename']:
                    pass
                else:
                    datastore['filename'].append(arg)
                    write_data_to_json(datastore)

                    self.full_log.info(f"{arg} appended to database")

        append_to_data_set(filename)

    def file_has_not_been_previously_downloaded(self, filename):
        try:
            datastore = self.get_data_from_json(self.json_filename)
            if filename in datastore['filename']:
                return False
            else:
                return True
        except:
            # creates new file if file doesn't exist and returns True
            data = {'filename': []}
            with open(self.json_filename, 'w') as file:
                json.dump(data, file, indent=4)
            return True
