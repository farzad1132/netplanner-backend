Features
========

Tested REST API
---------------

All endpoints are following REST API architecture also we have ``Unit`` and ``Integration`` tests for
all endpoints using modern ``pytest`` library

Versioning inputs
-----------------

We have versioning systems like ``git`` for all of inputs including ``Traffic Matrix`` and ``Physical Topology``.

users can also manipulate this records for any reason.

.. note:: Deleted records remain in the database for situations that users accidentally delete records

Authorization
--------------

We have ``Oauth2`` authorization using ``Access`` and ``Refresh`` tokens for all sensitive API

User Registration
-----------------

We have implemented a procedure for new users registrations **without** any maintainer (including admins) interactions

Sign up procedure:

#. Entering account information
#. After submit a email will be sent
#. confirming email by clicking on link in the confirmation email

.. important:: Only emails with ``@sinacomsys.com`` domain is valid

User Management
---------------

In backend we have three user roles:

#. Admin
#. Manager
#. Designer

Manager can do almost anything, he/she can create projects, run algorithms, edit inputs (including deleting) and ...

Designers has lower access than managers, they can not do following things:

#. Create projects
#. delete records (by record we mean a specific version of inputs like Physical Topology)
#. add other designers to the projects
#. run algorithms
#. share inputs

Background Task Manager
-----------------------

user (frontend) can run all algorithms asynchronously in background and check on running states at any time

Sharing inputs and results between users
----------------------------------------

User with right authorization can share inputs like ``Traffic Matrix`` or ``Physical Topology`` and results like
``RWA`` or ``Grooming`` algorithm results with registered users.

Accepting multiple format for inputs
------------------------------------

Multiple inputs format are acceptable. for example for ``Traffic Matrix`` :

#. Excel format with right structure (there is a template that user can use)
#. Using previous inputs that exist in database
#. Entering required in available views in frontend