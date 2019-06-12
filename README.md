  ____ _      _         _             _             
 / ___| | ___(_)___ ___(_)_ __   __ _| |_ ___  _ __ 
| |   | |/ _ \ / __/ __| | '_ \ / _` | __/ _ \| '__|
| |___| |  __/ \__ \__ \ | | | | (_| | || (_) | |   
 \____|_|\___|_|___/___/_|_| |_|\__,_|\__\___/|_| 


The following is a list (in order) of the steps the Cleissinator takes to do its job.

1. Removes all files/folders from download directory
2. Repopulates download directory with empty folders
3. Opens Cleiss platform
4. Logs in to home portal
5. Navigates to page with downloads
6. Downloads documents from page

	6.1. Checks if it is on the translation or certification page
	6.2. Gets the filename and checks if the file has been downloaded before using a text file
	
    if the filename doesn't match a filename in the json file:
	6.3. Downloads the file to the downloads folder
	6.4. Moves the downloaded file to it's corresponding language folder
	6.5. Writes the filename to the json file.
	
    else:
	6.3. Skips to the next file and repeats process starting at step 6.1.

