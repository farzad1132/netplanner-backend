Restful API with OpenAPI 3 and Routing
======================================

In this section we are going deep to our Restful API.

specification link: `OpenAPI 3 <http://spec.openapis.org/oas/v3.0.3>`_

We strongly suggest that after reading this documentation (which its purpose isn't covering all of specification aspects) visit above web page
and learn more about OpenAPI 3

In order to simplify above specification, we can say our API is consist of several **paths**
and each path has several **verbs**.

An example of path:
    ``/PhysicalTopology/read_all``

by verbs, we mean **HTTP method**.

After specifying path we have to define verbs of the path.
An example of **get** method for above path:

.. code-block:: 

    /PhysicalTopology/read_all/{user_id}:
      summary: Reading all PT's
      get:
        tags:
          - Physical Topology
        summary: Reading all PT's stored in Database
        security:
          - jwt: []
        operationId: PhysicalTopology.read_all_PT
        parameters:
          - $ref: '#/components/parameters/user_id'
        responses:
          200:
            description: Returning back all PT's
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      name:
                        type: string
                      id:
                        type: integer
                        format: int64
                      create_date:
                        type: string
                        format: date-time
                    required:
                      - name
                      - id
                      - create_date
          default:
            description: error handling
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error_msg:
                      type: string
                  required:
                    - error_msg

Usage of different components in our example code
-------------------------------------------------

    * **tags**
        Tags used for grouping different paths that are related in some manner

    * **security**
        This one will be discussed in its own section ( see Security section )

    * **operationId**
        This one tells that which function in which module is responsible of handling this **(path, verb) pair**.
        from above code we can tell that function with name *read_all_PT* and module *PhysicalTopology* is responsible
        for this (path, verb).

        example of (path, verb) pair: 
          `(/PhysicalTopology/read_all/{user_id}, GET)`
    
    * **parameters**
        As its name speaks, this component defines this (path, verb) parameters.
        As you can see in this code we have used *Reference* to prevent copying same exact code in multiple places.

        References are defined at the top of specification file.
        In this case definition is:
        
        .. code-block:: 

          user_id:
            name: user_id
            in: path
            required: true
            schema:
              type: integer
        
        As you can guess *name* is name of this parameter and we will use this in our handler function.
        after that we have **in** keyword which specifies where is the place of this parameter
        in HTTP request, *in* can be **query**, **path** or **header**.
        After that we have *schema* section which defines parameter structure, in this example *Id* is simple integer type and
        there is no need for advanced schema.
    
    * **responses**
        In this section we define different possible respond status codes ( HTTP status codes )
        and for each one them we have to describe respond body structure( schema ).
        In our example code we can see that for status code 200 this (path, verb) will return 
        an array of *JSON* object and each JSON object has three mandatory properties with the name of name, ida and create_date.

        Also there is an **default** responses. its usage in our application - *NOT IN GENERAL* -
        is that we can return any status code other than 200 ( in this (path, verb) ) with an **error_msg**.

Brief look at handling function
-------------------------------

This handling function corresponds to above api specification:

.. code-block::

  def read_all_PT(user_id):
    PTs = PhysicalTopologyModel.query.filter_by(user_id= user_id).all()
    if not PTs:
        return {"error_msg": "no Physical Topology found"}, 404
    else:
        schema = PhysicalTopologySchema(only=("id", "name", "create_date"), many= True)
        return schema.dump(PTs), 200

First thing is that we can simply receive our parameter in function.
Then we can see application of default responses here as we returned an *error_msg* with 404 status code
and at the last line you can see that we are returning a JSON object with status code of 200 ( its not clear how `schema.dump(PTs)`
is a JSON object but leave it for now we will explain this later in **Models** section).


request body in POST and PUT method
-----------------------------------

we started with GET method because its the easiest method to explain also its doesn't require
request body.

Request Body is much like a responses body but its sent from user of the API to server

An example of request body definition:

.. code-block::

  requestBody:
    description: providing information for creating new Physical Topology
    content:
      application/json:
      schema:
        $ref: '#/components/schemas/PhysicalTopology'

First of all this example proves our claim that request body is so much like response body,
Second we have used another Reference here for **PhysicalTopology** object.

PhysicalTopology and **TrafficMatrix** objects will be discussed in their own section

An example of extracting request body in handler function is as follow:

.. code-block::

  def create_PhysicalTopology(name, user_id):
    PT = json.loads(request.get_data())
    PT_object = PhysicalTopologyModel(name= name, data= PT)
    db.session.add(PT_object)
    db.session.commit()
    
    return {"Id": PT_object.id}, 201

with `json.loads(request.get_data())` we can extract request body. ( you have to import **json** library ).


Connection between Flask and OpenAPI
------------------------------------

This is though if don't use **connexion** library.
In connexion this can be done with this line of code:

.. code-block::

  connex_app = connexion.App(__name__,
                            specification_dir=os.path.join(basedir, "openapi"))


In above code we simple gave **openapi.yaml** file path to app initializer.

We will explore more about this in **Modules** section.