## Start with `Docker`

> **Step 1** - Start the APP in `Docker`

```bash
$ docker-compose up --build 
```

Visit `http://localhost:5085` in your browser. The app should be up & running.

<br />

### 👉 Set Up for `Unix`, `MacOS` 

> Install modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />

### 👉 Set Up for `Windows` 

> Install modules via `VENV` (windows) 

```
$ virtualenv env
$ .\env\Scripts\activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> Create Superuser

```bash
$ python manage.py createsuperuser
```

<br />

> Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />

## Create Users

By default, the app redirects guest users to authenticate. In order to access the private pages, follow this set up: 

- Start the app via `flask run`
- Access the `registration` page and create a new user:
  - `http://127.0.0.1:8000/register/`
- Access the `sign in` page and authenticate
  - `http://127.0.0.1:8000/login/`

<br />

## Codebase Structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |-- core/                            
   |    |-- settings.py                   # Project Configuration  
   |    |-- urls.py                       # Project Routing
   |
   |-- home/
   |    |-- views.py         # APP Views 
   |    |-- urls.py          # APP Routing
   |    |-- models.py        # APP Models 
   |    |-- tests.py         # Tests  
   |  
   |-- templates/
   |    |-- includes/        # HTML chunks and components   
   |
   |-- static/
   |    |-- CSS, JS, Images  # CSS files, Javascripts files   
   |
   |-- requirements.txt      # Project Dependencies
   |
   |-- env.sample            # ENV Configuration (default values)
   |-- manage.py             # Start the app - Django default start script
   |
   |-- ************************************************************************
```

<br />

## Customize CSS

- Edit the `static/assets/scss/styles.css`
- Regenerate the CSS using `NPM` or `Yarn`

```bash
$ npm i            # Install modules
$ npm run build    # Recompile SCSS to CSS
$ npm run min-css  # Minify CSS
$ // OR 
$ yarn             # (via Yarn) Install modules
$ yarn build       # (via Yarn) Recompile SCSS to CSS
$ yarn min-css     # (via Yarn) Minify CSS
```
