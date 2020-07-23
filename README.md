![pypi](https://img.shields.io/pypi/v/tuxdrive.svg)
![python](https://img.shields.io/pypi/pyversions/tuxdrive.svg)
![license](https://img.shields.io/github/license/prahladyeri/tuxdrive.svg)
![last-commit](https://img.shields.io/github/last-commit/prahladyeri/tuxdrive.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)
[![donate](https://img.shields.io/badge/-Donate-blue.svg?logo=paypal)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JM8FUXNFUK6EU)
[![follow](https://img.shields.io/twitter/follow/prahladyeri.svg?style=social)](https://twitter.com/prahladyeri)

## Introduction

`tuxdrive` is a console based DIY google drive client.

![Logo](tuxdrive/logo_small.jpg)

## Installation

	pip install tuxdrive


Since this is a DIY (Do-it-yourself) app, you'll have to register your own app by going to the [Google Cloud Console](https://console.cloud.google.com) and then:

1. Enable Google Drive API.
2. Create credentials (make sure you choose "Desktop App").
3. Download the credentials json file and save it as `client_id.json` to your working folder. 

Only then the program will be able to work. For more information on registering a Google app, you may [refer to this article](https://prahladyeri.com/blog/2016/12/how-to-create-google-drive-app-python-flask.html).

Notes:

- If you are a new developer on Google, you might see a prompt saying "This app isn't verified", so you must add a [security exception](https://raw.githubusercontent.com/prahladyeri/prahladyeri.com/gh-pages/uploads/google_app_no_street_cred.png) to verify it successfully.
- As of version 2.0.0, `pip` is the only supported installation method, the old DEB/RPM method is depreciated.

## Usage

`tuxdrive` has a command line interface to the google drive interface similar to traditional unix tools like `ftp` and `sftp` (though not as extensive and comprehensive yet!).

Once you start `tuxdrive` program, it will give you a `tux_drive>` prompt from which you can run the above commands. When you run `tuxdrive` the first time, it will open up the browser window and ask for permissions to access your google drive on your behalf. After that, you can start running commands. You can list your drive files using `ls` or `dir` command for example:

![Screenshot](https://github.com/prahladyeri/tuxdrive/raw/master/screenshot.png)

Similarly, you can run `push some_local_file.txt` to upload it to your drive, or `rcd my_drive_folder` to change the remote drive. Here is the entire command list:

	help (or ?): Shows this help facility.
	dir (or ls): Lists all files and folders on drive.
	!dir (or !ls): Lists all files and folders in current directory.
	get (or pull) <item>: Pulls the named file/folder from drive to current working directory.
	put (or push) <item>: Pushes the named file/folder from current working directory to drive.
	rm <item>: Delete the named file/folder on remote path.
	pwd: Print working directory (remote/drive).
	cd: Change working directory (remote/drive).
	lpwd: Print working directory (local).
	lcd: Change working directory (local).
	mkdir: Create a directory on remote path.
	list permissions <item>: Lists the permissions on specific file/directory.
	clear permissions <item>: Clears permissions on specific file/directory.
	share <item>: Shares the specific file/directory in remote drive publicly.
	share <item> <email>: Shares the specific file/directory in remote drive to specified email.
	exit: Exits this program.
	rdcache: Show remote directory mapping of id and folder paths.
	rfcache: Show remote files mapping of id and folder paths.

## License

`tuxdrive` is free and open source software. It is [MIT](https://opensource.org/licenses/MIT) licensed.

## Donation

I'm a poor and humble coder from India and highly stressed for resources. Please consider donating if this tool has helped you in any way. You can also [hire me on fiverr](https://www.fiverr.com/prahladyeri) to get any coding task done.

- [Donate through PayPal](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JM8FUXNFUK6EU)
- [Donate through Patreon](https://www.patreon.com/prahladyeri)