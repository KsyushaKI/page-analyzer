<div align="center">
<h1>Page Analyzer</h1>
<p>A page analyzer is a website that analyzes specified pages for SEO suitability</p>
<p>Follow the following link to try: <a href="https://page-analyzer-ot9i.onrender.com/">Page analyzer</a></p>

[![Actions Status](https://github.com/KsyushaKI/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/KsyushaKI/python-project-83/actions)
![Lint Check](https://github.com/KsyushaKI/python-project-83/actions/workflows/github_action.yml/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/103f5cdf5ae8928733b4/maintainability)](https://codeclimate.com/github/KsyushaKI/python-project-83/maintainability)

</div>


## About

Page Analyzer is a full-featured application based on the Flask framework that analyzes specified pages for SEO suitability. 

Here the basic principles of building modern websites on the MVC architecture are used: working with routing, query handlers and templating, interaction with the database.

In this project the Bootstrap 5 framework along with Jinja2 template engine are used. The frontend is rendered on the backend. This means that the page is built by the Jinja2 backend, which returns prepared HTML. And this HTML is rendered by the server.

PostgreSQL is used as the object-relational database system with Psycopg library to work with PostgreSQL directly from Python.

[Demo](https://page-analyzer-ot9i.onrender.com/)

### Features

* [X] Validate, normalize and add new URL to the database;
* [X] Check the site for its availability;
* [X] Query the desired site, collect information about it and add it to the database;
* [X] Display all added URLs;
* [X] Display the specific entered URL on a separate page with obtained information;

### Built With

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/2.2.x/)
* [Bootstrap 5](https://getbootstrap.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
* [Jinja 2](https://palletsprojects.com/p/jinja/)
* [Psycopg 2](https://www.psycopg.org/)
* [Gunicorn](https://gunicorn.org/)
* [Poetry](https://python-poetry.org/)
* [Flake8](https://flake8.pycqa.org/en/latest/)

This is the third training project of the ["Python Developer"](https://ru.hexlet.io/programs/python) course on [Hexlet.io](https://hexlet.io)

> GitHub [@KsyushaKI](https://github.com/KsyushaKI) &nbsp;&middot;&nbsp;
> LinkedIn [@Oksana Karshakevich](https://www.linkedin.com/in/oksana-karshakevich-097663243/)
