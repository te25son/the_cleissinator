<h1 align="center">The Cleissinator</h1>

The Cleissinator was created to automate the tedious task of logging on and downloading files off of our client's platform. It is the first part of a two-part program that creates projects using folders located in the Cleissinator's `DOWNLOAD_DIR`. The two parts are connected through a SFTP.

*This page documents the use of the first part only.*

### Packages
Package requirements can be found in the requirement.txt file. First make sure that pip is installed, and then simply call the command `pip install -r requirements.txt`. 

The Cleissinator uses geckodriver as its default driver. The location of geckodriver.exe is specified in the project's main.py file when defining the driver's `executable_path` parameter:

```python
driver = webdriver.Firefox(firefox_profile=profile, options=options, executable_path=r'./driver/geckodriver.exe')
```

The .exe file is already located within the project's root directory under driver/geckodriver.exe. This may be moved to another location so long as you specify the new location of the .exe file in the driver's `executable_path` parameter.

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
