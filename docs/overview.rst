Overview
========

Structure of document:

First, we explain how to install and run the backend, then we have a small discussion on architecture and reasons for
choosing used technologies and after this, we have listed the main backend features. at the end, we have complete API documentation
of all modules

.. important:: REST API documentation isn't included in this documentation because it has it's own ``Interactive`` documentation
                on sina's server in http://localhost:5020/docs and http://localhost:5020/redoc

In REST API document you can insert your data as payload or parameters and send real request to backend and receive result in
beautiful Structured manner, also you can download responses as ``JSON`` file

The main components of NetPlanner backend are:

#. *FastAPI* as web service
#. *Nginx* as proxy server
#. *Postgres* as database
#. *SqlAlchemy* as ORM
#. *RabbitMQ* as message broker
#. *Celery* as background task manager
#. *Docker* as containerization tool
#. *kubernetes* as orchestrator (future releases)