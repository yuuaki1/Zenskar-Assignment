# Zenskar Assignment
This zenskar code assignment entails the setup needed to be performed to run the Python Script.

## Prerequisites
- Python 3.7 or higher in your system.
- A working and stable internet connection

## Steps:
### 1. Set up virutal environment
- Set up virtual environment using the ```venv``` module.
  
  ```bash
  python -m venv [virtual environment name]
- Activate the venv by going to ```[virtual environment name]/Scripts/activate``` on Windows and ```source venv/bin/activate``` on Mac and Linux.

### 2. Install required modules
- Run the followiing command to install necessary modules.

  ```python
  pip install python-dotenv requests json

### 3. Create a ```.env``` file
- In the project directory, create a ```.env``` file.
- Add the following variables:

  ```env
  API = [YOUR API KEY]
  ORGANISATION = [YOUR ORGANISATION ID]

### 4. Run the python script
- Run the python script using

  ```bash
  python [script_name].py
