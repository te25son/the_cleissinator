from selenium import webdriver

import settings
from utils.make_directories import DirectoryMaster
from utils.cleissinator import Cleissinator as cnator


def main():

    # Directory
    d_master = DirectoryMaster(
        settings.HOMEPATH,
        settings.FOLDERNAME_DICT,
        settings.DOWNLOAD_DIR,
    )

    d_master.remove_download_directory()
    d_master.make_directories_if_they_dont_already_exist()

    # Cleissinator
    profile = webdriver.FirefoxProfile()
    profile.set_preference("pdfjs.disabled", True)
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("pdfjs.enabledCache.state", False)
    profile.set_preference("browser.download.dir", settings.DOWNLOAD_DIR)
    profile.set_preference("pref.downloads.disable_button.edit_actions", True)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.helperApps.neverAsk.openFile", "application/pdf")
    profile.set_preference("browser.helperApps.neverAsk.openFile", "application/octet-stream,application/pdf,application/x-pdf,application/vnd.pdf")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/pdf,application/x-pdf,application/vnd.pdf")
    options = webdriver.FirefoxOptions()

    # displays the browser while testing
    if settings.TEST == False:
        options.add_argument('-headless')

    driver = webdriver.Firefox(firefox_profile=profile, options=options, executable_path=r'./driver/geckodriver.exe')
    TheCleissinator = cnator(
        driver,
        60,
        settings.DOWNLOAD_DIR,
        settings.LOGIN_CREDS['url'],
        settings.LOGIN_CREDS['username'],
        settings.LOGIN_CREDS['password'],
        settings.FOLDERNAME_DICT,
    )

    TheCleissinator.open_url()
    TheCleissinator.login_to_home_portal()
    TheCleissinator.click_dropdown_link_to_translations_page()
    TheCleissinator.download_documents_from_page()


if __name__ == '__main__':
    try:
        main()
    except:
        # if error occurs force to run again
        main()
