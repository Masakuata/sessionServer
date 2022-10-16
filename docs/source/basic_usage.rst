Basic Usage
===========

.. warning::

    Before proceeding, be sure that you want to connect to a XFSessionServer
    type. This library just works with that kind of server.

.. _installation:

Installation
------------

You can install the required libraries to use a remote session server with pip:

.. code-block:: console

    $ pip install xf-auth

As simple as that!

.. note::

    Currently, the library is stored only on PyPi. Be sure to use that repository.

.. _initial_configuration:

Initial Configuration
---------------------

To get started, import the RemoteSession and Auth classes.

.. code-block:: python3
   :linenos:

    from xf_auth.Auth import Auth
    from xf_auth.RemoteSession import RemoteSession

Then, you have to indicate a couple of values, and you're off to the races!

Don't worry, we'll explain each line.

.. code-block:: python3
   :lineno-start: 3

    Auth.set_user_origin(User)
    Auth.set_user_keys(["email", "password"])
    Auth.set_role_attribute("role")

    RemoteSession.set_address("192.168.1.100")
    RemoteSession.set_port("42100")

On line 3, we indicate the user class that we want to create remote sessions for.
If you have multiple types of users, just set it to the user base class. You do
remember those *inheritance* and *polymorphisms* lectures, right?

On line 4, we supply a list with the names of the required user attributes to create a session.
At least two attributes are required, and there's no upper limit. The example
shows the recommended attributes.

The 5th line is optional. If your application has user roles, such as *admin*,
*moderator*, *seller*, *content creator* or anything else, you can set the attribute
name of the user class where you store that value.

For example, if the user class is something like this:

.. code-block:: python3

    class User:
        def __init__(self):
            self.email = None
            self.password = None
            self.role = "client"

Then we need to indicate the ``role`` attribute.
The role attribute can be of any primitive type.

In the 7th line, we supply the address for the remote session server.
It can be any type of URL or and IPv4 or IPv6 address.

Lastly, the 8th line is optional. If you need to specify a port, you set it here.
It can be a string or an integer.

The port number could be set in along with the address like this:

.. code-block:: python3

    RemoteSession.set_address("192.168.1.100:42100")

.. _new_session:

Creating a new session
----------------------

After the initial config, we are ready to go!

Create a new session in the remote server with the following code.

.. code-block:: python3

    payload = {
        "email": "user1@mail.com",
        "password": "aG00dP4sw00rD",
        "role": "client",
        "birthday": "07/19/1999",
        "is_admin": False
    }
    response = RemoteSession.init_session(payload)

The ``payload`` is the information that will be sent to the server.
The only required fields are the ones you set in the
:ref:`configuration <initial_configuration>` section.
Besides that, you can put anything you want to store in the remote server.

Keep in mind that all the info you send will only be stored while the session
is alive.

The ``response`` variable holds the server response (duh!).
It is a dictionary that holds two values, an HTTP ``STATUS`` and (possibly) a ``TOKEN``.

If the request was successful and a new session was created, the ``STATUS`` key
holds an HTTP status code of 201, and the ``TOKEN`` key a string.
This string is the *session token*. Keep it in a safe place, cause you will need
it for every future request regarding the session you just created.

This token is like a session ID of sorts. Yeah! That's it!

If the request was not successful, you can find the corresponding HTTP status
code in the first position of the tuple.

In code would look something like this:

.. code-block:: python3

    response = RemoteSession.init_session(payload)
    status_code = response[0]

    if status_code == 201:
        # Yay! We got a token
        token = response[1]
    else:
        # The request failed. Let's see why
        # Proceed to handle the HTTP status code as you see fit

.. note::

    This new session implementation will definitely change in the future.
    I hope to make it easier to handle.

.. _get_session:

Getting stored information
--------------------------

You created a remote session? Great! Now let's see how to check the information
we stored.

.. code-block:: python3

    data = RemoteSession.get_session_info(token)
    print(data["birthday"])

Remember the token? Now it's time to use it.
Pass it to the function shown above and it will take your information back.

Easy, right?

.. _update_data:

Update session data
-------------------

You have sent the wrong information?
Don't worry. We can change it easily.

.. code-block:: python3

    new_data = {
        "birthday": "10/19/1999",
        "is_admin": True
    }
    RemoteSession.update_data(token, new_data)

Just like that we can send the ``new_data`` to replace the old one in the server.

It's like magic!

.. _check_session:

Is the session alive?
---------------------

How much time have passed since you created the session? Surely it has
been destroyed.

To check if the session is alive in the remote server, do something like this:

.. code-block:: python3

    is_alive = RemoteSession.is_session_alive(token)
    if is_alive:
        print("Yay! It is still alive")
    else:
        print("Well, it was good while it lasted")

Just one line can tell you if the session is still alive on the other end.
You can thank me later. ; )

.. _delete_session:

Destroy the session
-------------------

Like everything in life, it must end.

It seems that the time to destroy the session has come.
Don't cry. It will be quick, and painless.

.. code-block:: python3

    RemoteSession.close_session(token)

Just like that, it's gone.

Be sure to retrieve all your data before destroying a session.
Once a session has been destroyed, the information cannot be recovered.
It's gone. Forever.

.. note::

    Even if you don't purposely destroy a session, it will be removed after
    some inactivity time.

    The default session lifetime is 10 minutes since the last operation.
    If you have not performed an operation in the las 10 minutes, you can
    say goodbye.

    To keep a session from being destroyed, you can use
    ``RemoteSession.is_session_alive`` to restart the 10 minute timer.