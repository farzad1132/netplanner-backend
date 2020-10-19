Welcome to NetPlanner-BackEnd's documentation!
==============================================

This documentation purpose is to explain NetPlanner BackEnd architecture and modules
and help future developers to contribute on this code more easily.

NetPlanner different parts are:

* Web Server
   This is front gate of backend and we are using **Nginx** here

* WSGI Server
   This one is a interface that connects *web server* to *Service*
   and here we are using **Gunicorn**.

* Service
   This is where our actual logic ( algorithms, API, .. ) implemented
   and here we are using **Flask**.

* Database
   This is where we are storing algorithms results, users information and etc.
   here we are using **Postgresql**.

We are going to discus all mentioned parts of backed in separate section

for **Service**:
 * Restful API and it's specification
 * Routing of API
 * User Management
 * Security in API

for **Database**:
 * ORM system
 * Models




.. toctree::
   :maxdepth: 2
   :caption: Table of Contents:
   
   /RestAPI
   /Routing
   /UserManagement
   /Security
   /ORM
   /Models



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
