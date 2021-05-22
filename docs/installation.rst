Installation And Running
========================

There are several ways for installing NetPlanner backend but the easiest way is to use docker

Installation process using docker:

#. Install docker
#. Install docker-compose
#. Install these images:
    #. Nginx
    #. RabbitMQ
    #. Postgres

    .. note:: you can install these images using bellow command:

        .. code-block:: bash
        
            docker pull [image name]

#. creating NetPlanner image by running command bellow in **project directory**:
    .. code-block:: bash

        docker build . -t service:v2

#. running project using docker compose using bellow command:
    .. code-block:: bash

        docker-compose up -d

    .. note:: this command runs NetPlanner backend in detach mode, if you want to see the 
              logs in live mode you can delete ``-d`` in command above

#. go to http://localhost:5020/docs to see the API documentation

#.  At this point you have NetPlanner backend fully functional but if you want some initial date
    in database to work with you can run commands bellow (in order):

    .. code-block:: bash

        1. docker exec -it service bash

        2. python init_database.py

        3. exit

#. Finally for stopping server run command below:
    .. code-block:: bash

        docker-compose down 
    