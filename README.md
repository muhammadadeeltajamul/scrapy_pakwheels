# Scrap PakWheels

The program should be able to get the data of new and used cars from pakwheels

# Virtual Environment
### Install virtualenv and virtualenvwrapper
_pip install virtualenv_

_pip install virtualenvwrapper_
### Add variables to path (Recommended)

export WORKON_HOME=$HOME/.virtualenv

export PROJECT_HOME=$HOME/projects
### Find virtualenvwrapper and run it
_which virtualenvwrapper.sh_

_The command will output a path similar to this "/usr/local/bin/virtualenvwrapper.sh"_

Enter the following command to run this file

_source /usr/local/bin/virtualenvwrapper.sh_

### Reload startup file ".bashrc"
_source ~/.bashrc_

### Create a new virtual environment
_mkvirtualenv env-name_

This environment will be loaded automatically after successful creation, if it is not loaded use 

_workon env-name_

### Installing requirements
Run the following command in the environment to install the requirements

_pip install -r requirements.txt_

# Scrapy Project
### Creating scrapy project
Run the following command in the environment to create scrapy project

_scrapy startproject project-name_

### Setting up scrapy spider
Copy the file _"pak_wheels.py"_ from repository to location

_project-name/project-name/spiders/_

# Usage
### Saving data as json
To save data in .json file, first change terminal directory to the directory where you pasted the file then run the following command

_scrapy crawl pak_wheels -L WARNING -o output.json_



