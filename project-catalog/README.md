# Udacity Project - Item Catalog

This is the second project of the [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004). In this project we'll build an event website with *Flask*, *SQLALchemy*, *Google OAuth* and *API endpoint*.

## Getting Started 

In order to run the programm, we'll need some dependencies. 

**Install dependencies:**
Here are the third-party dependencies you'll need to install to get it running:
* Flask: A lightweight web-framewrok
* Flask-Login: A tool for managing user session  
* OAuthLib: A battle-hardened OIDC library
* pyOpenSSL: An easy way to enable running securely with *https*
* pycopg2: A database to store some information 

We'll create a *requirements.txt* file with the following contents:

```
Flask==1.1.1
Flask-Login==0.4.1
oauthlib==3.1.0
pyOpenSSL==19.0.0
pycopg2==2.8.4
```

To install all those dependenciesn from the **requirements.txt**, run the following command: 

```
pip install -r requirements.txt
```

## Running the program
Open the terminal. Then, run the following commands:

```
python app.py
```