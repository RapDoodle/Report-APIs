# Mangee Flask-RESTful
Mangee Flask-RESTful is a template/framework designed to simplify the process of building scalable RESTful Flask applications.

## Getting Started

- Clone the repository

  ```shell
  git clone https://github.com/RapDoodle/mangee-flask-restful.git
  ```

- Install required Python packages

  For Linux users
  ```bash
  $ pip3 install -r requirements.txt
  ```

  For Windows users
  ```bash
  $ pip install -r requirements.txt
  ```

  Please be noted that some dependencies may not be installed on Debian and Ubuntu. If an error occurred while installing `bcrypt`, run the following command

  ```bash
  sudo apt-get install build-essential libffi-dev python-dev
  ```

- Spinup a development server

  ```bash
  $ python3 run.py dev
  ```
  In the last argument, `dev` specifies the name of the configuration. Please visit the documents on configurations under the `docs` folder for more information about the configurations.

## Contributors
- Bowen WU (@RapDoodle)

## License
The project is licensed under the GNU General Public License v3.

## Copyright
Copyright (c) 2021.