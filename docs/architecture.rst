Architecture
============

In this Section we are going to explain architectural decisions for NetPlanner

Before explaining architecture and related technologies for components lets review some of
initial specifications for backend (stated by product owners):


#.  The user must be able to run algorithms **asynchronously**, meaning user starts algorithms
    at time ``x`` and then after completion of algorithm at time ``x+t`` user be able to fetch
    results from database.

#. The user must be able to store inputs and outputs in database

#. The initial design can be monolith (but modular) and in future versions become micro service

.. note:: Complete list of backend features will be discussed in later chapters


With knowing some backend specifications let's explore components.

Web Service
-----------

As stated before we are using **FastAPI** for this purpose because:

#. Its' Fast even faster than flask and djando
#. It's based on a ASGI (Asynchronous Server Gateway Interface) framework which brings a lot into the table
#. Supports python asyncIO library (for coding fast single-threaded async codes)
#. Automatic document generation (using OpenAPI 3 specifications)
#. Supports (and uses) modern python features (like type annotation for type checking)
#. Advanced support for dependency injection

And many more...

Proxy Server
------------

The specifications said backend must be high performance and fast, so without any thinking
**Nginx** came into mind and there is no need for listing it's features.


Database
--------

Unlike most of systems that you can choose whether a relational database meets your need or
a NoSQL database, in this project we are dealing with some complicated and big data like algorithms
outputs and some relational data like users, projects, inputs,... .

At the end we decided to choose both, meaning saving complicated data in NoSQL manner and storing
relations data in relational manner.

After some research turned out **Postgres** is best for such actions.


ORM
---

As developers we didn't want to keep our heads busy with SQL commands in the entire backend