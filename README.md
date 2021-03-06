<h1 align="center">The Cleissinator</h1>

The Cleissinator is a command line program that uses selenium. It was created to automate the tedious task of logging on and downloading files off of our client's platform. It is the first part of a two-part program that creates projects using folders located in the Cleissinator's `DOWNLOAD_DIR`. The two parts are connected through a SFTP.

*This page documents the use of the first part only.*

## Packages
Package requirements can be found in the requirement.txt file. First make sure that pip is installed, and then simply call the command `pip install -r requirements.txt`. 

The Cleissinator uses geckodriver as its default driver. The location of geckodriver.exe is specified in the project's main.py file when defining the driver's `executable_path` parameter:

```python
driver = webdriver.Firefox(firefox_profile=profile, options=options, executable_path=r'./driver/geckodriver.exe')
```

The .exe file is already located within the project's root directory under driver/geckodriver.exe. This may be moved to another location so long as you specify the new location of the .exe file in the driver's `executable_path` parameter.

*.exe is only to be used for Windows systems. For other OSs, please download from the [latest releases](https://github.com/mozilla/geckodriver/releases). In fact, it's best to download directly from this link even if you're currently operating windows, as the .exe file included in this project may be out of date.* 

## Settings
In order to keep all of your environment variables in one, secure place, it's best to create a settings.py file in the projects root directory.

Your settings.py file should include the following variables to get the Cleissinator up and running:

* HOMEPATH
* DOWNLOAD_DIR
* FOLDERNAME_DICT
* TEST
* LOGIN_CREDS

#### HOMEPATH / DOWNLOAD_DIR
`HOMEPATH` sets the base directory on top of which `DOWNLOAD_DIR` is built. It is not necessary, but you must specify the location where geckodriver will direct your downloaded files. Therefore, if you do not include it, you must make sure that `DOWNLOAD_DIR` represents the complete path to the folder on your computer where downloads will go.

#### FOLDERNAME_DICT
This should be a python dictionary where the keys are languages and values are folder names.

Prior to running geckodriver, the Cleissinator will populate the `DOWNLOAD_DIR` with empty folders specified by the values of the `FOLDERNAME_DICT`

For example, a FOLDERNAME_DICT such as...

```python
FOLDERNAME_DICT = {
	'latin': ['LATIN-Trans', 'LATIN-Rev'],
	'sumerian': ['SUMERIAN-Trans', 'SUMERIAN-Rev'],
}
``` 

...will create the following folder structure:

```bash
├───DOWNLOAD_DIR
│   ├───LATIN-Trans
│   ├───LATIN-Rev
│   ├───SUMERIAN-Trans
│   ├───SUMERIAN-Rev
```

#### TEST
`TEST` is used to determine whether or not the browser will be displayed while the Cleissinator is running. If `TEST` is set to true, the browser will be displayed. This is to help see what exactly the program is doing to better understand where something went wrong in the event something does go wrong.

#### LOGIN_CREDS
This is another python dictionary that should include three keys: username, password, and url. The `LOGIN_CREDS` are used to access the client portal.

## Running the Cleissinator

To run the Cleissinator make sure that all requirements are included in your virtual environment and that you are running python 3.7 or later.

To check whether you are running the correct version of python, run `python --version` in your command shell.

Check your settings.py file to make sure your environment variables match the necessary information. **It is very important that your `DOWNLOAD_DIR` is in a location that you can access**. As well, check your `LOGIN_CREDS` to be sure they are correct. Geckodriver will not be able to open the portal if any of the credentials are misspelled or missing. 

Once the above criteria are checked and met, direct your command tool to the root directory of the project and run `python main.py`.

And congratulations! You've successfully run the Cleissinator :)
