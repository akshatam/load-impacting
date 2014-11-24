## Requirements

This application library was designed on Windows 8, with Python 2.7, in a rather hasty manner.
However, we do have our own requirements, and those are,
The Awesome SDK with LoadImpact; pip install loadimpact

## Installation

This is a GIT based repository, and there is a Install script at the Root Level.: Install.py
Please run that before tweaking the application. The Install Script makes sure, all dependencies are met,
all required files to run the test are in place.

### JMETER Test file at {PROCJECT_ROOT}/resources/jmeter_test.xml
This is a sample file provided by the LoadImpact team and should not be altered, as the Test depend on values parsed
from this.
You can of-course use a different file, refer to pilot.py in "src/"
The config_mgr() Class can be instantiated with a file name (path), so feel free to change in pilot.



## Credential Management
my.token: is Author's token file, "amar.akshat@gmail.com".
This is initially zipped with a password in the root directory, and one needs to run the Install script with the option
--password <password> to be able to use it. If you do not pass the password option, the Install script will ask for the
same on the runtime, please be prepared to enter that.
The token file in resources/tokens/my.token is initially a placeholder with corrupt text, and will be replaced by the
Install script as a valid token file.

Ask, amar.akshat@gmail.com for the password to Zip File.
*Please Remember*, this is only for test, and if you want to use the Library as such, just put your own token file in
 ./resources/tokens/ as "yourname".token" and instantiate the Client with yourname
 client = client_manager.get_client('yourname')
 