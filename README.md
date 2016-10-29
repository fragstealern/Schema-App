# School a' clock

## Installation


0. Requirements
    ```bash
    Python 3.4.4
    ```

1. Install requirements

    ```bash
    pip install -r requirements.txt
    ```
    1.1 LXML
    If you're using windows and get an error saying that microsoft visual c++ is required
    Go to https://pypi.python.org/pypi/lxml/3.4.0 and download and install for Python version 3.4

2. Install Google's API

    ```bash
    pip install --upgrade google-api-python-client
    Unpack the file
    python setup.py install
    ```

3. Start the python files

    ```bash
    Go into /api-app
    run: python setup.py install
    Go into /schema-app
    run: python setup.py install
    ```

4. If both python files succesfully:

    ```bash
      http://localhost:8081
    ```
