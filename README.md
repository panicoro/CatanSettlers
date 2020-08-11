<p align="center">
  <img src="./src/images/catan_icon.png" hight= "150" width= "150" />
</p>

#  The settlers of Catan 

The following project implements a web application using [Django REST framework] (backend) and [React] (frontend) of a classic board game for a subset of rules.

[Django REST framework]: https://www.django-rest-framework.org/
[React]: https://es.reactjs.org/

For an introduction to the game it is recommended to read its [basic] rules in principle and then its [detailed] rules.

[basic]: https://drive.google.com/file/d/1xAtBKKUcGGNYGmStsaMez-lXh7LsySiM/view
[detailed]: https://drive.google.com/file/d/11sOYT_F_m4w6JRAGLTlwvNwMjfuMlXPN/view

## Requirements

### Frontend 

  * node ^ 12.13.0
  * npm ^ 6.12.0

To install them (in linux) do the following: 
In the directory `$HOME` run `wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.1/install.sh | bash`. This instals `nvm`, NodeJS's version control.
2. If the previus command was correct, then run `. .bashrc`. If there was an error, go to the page [página] nvm.
3. The command `nvm --version` should now return the version, in this case `0.35.1`.
4. Finally, to install `node` and `npm`, run `nvm install 12.13`. Now, it is possible run `node -v` and`npm -v`, and we should the current versions (in this case, `v12.13.0` y `6.12.0`, respectively)

To install in other operating systems refer to the [page] mentioned above.

[page]: https://github.com/nvm-sh/nvm#installation-and-update

### Backend

  * python ^ 3.7+
  * pip 


## Instalation

Download the repository with:

```bash
git clone https://github.com/panicoro/CattanSettlers.git
```

First install the dependencies for the backend, so go to the create and run the [virtualenv](https://virtualenv.pypa.io/en/stable/):

```bash
$ cd CattanSettlers/
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Then install all the dependecies for the frontend:

```bash
$ npm install
```

It is important **not** to run `npm update`, at least for the moment, since `react-scripts` does not support new versions of webpack.

## Usage

To run the server:

```bash
$ python manage.py makemigrations catan
$ python manage.py migrate
$ python manage.py runserver
```

The virtual environment must be activate.

For the frontend, run:

```bash
npm start
```
After the application completes its loading go to the browser at the following path: `http: // localhost: 3000`.

## Running the tests

### Unit tests

Inside the frontend directory, we must run:

```bash
$ npm run coverage
```

To run the tests inside the backend, with the virtual environment activated and
with migrations applied (makemigrations catan and migrate),
do:

```
pytest --cov=catan --cov-report term-missing
```

### Coding Style

We follow the code style [airbnb javascript].
To run the style violation test:

```bash
$ ./node_modules/.bin/eslint yourfile.js
```

[airbnb javascript]: https://github.com/airbnb/javascript

The python code follows the [PEP-8] convetions. You can test it with ```pycodestyle``` command.

[PEP-8]: https://www.python.org/dev/peps/pep-0008/
