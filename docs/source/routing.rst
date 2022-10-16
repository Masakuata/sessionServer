Routing
=======

Are you building a web server? Do you love flask? Great! This is a match made in heaven.

.. _enforce_payload:

Enforce payload on route
------------------------

With a little help you can make sure that a route will always receive the correct json payload.
If not, then we will handle the appropriate response.

.. code-block:: python3
   :linenos:

    @user.post("/user")
    @xfss.requires_payload({"email", "password", "name"})
    def register_user():
        # You can rest assured that the required values are in the json body
        pass

This is a flask example. Do you notice anything different?

The second line does all the magic! That one line ensures that the keys
indicated in the set are in the request body.

If the required values are in the request body, the function will execute as normal.
If not, we will send the client a 406 HTTP status code for you. We got you, pal.

.. _enforce_token:

Enforce token on route
----------------------

Do you remember the *token string* we talked about in the :ref:`basic usage <new_session>` section?
The client will need it to authenticate. In other words, to prove that he owns the session on the remote server.

Some routes in your web server should only be accessible by logged in users.
Guess what? We already got you covered.

.. code-block:: python3
   :linenos:

    @user.post("/pets")
    @RemoteSession.requires_token
    def register_pet():
        # This function is only accessible by logged in users!
        pass

Let's imagine that in your web app, your users can register their pets. How cute!
But it only makes sense to just let logged in users register pets.
Doesn't it?
If the user is not logged in, to whom we register the pet to?

The line 2 assures you that only logged in users will be able to use this route.
How do we know the user is logged in? Cause they will need to provide their session token.

We will check with the server if the token is valid and if the session is active,
and a bunch of other stuff in the background.

If you're building this web app, then I guess you'll need to build the front end too,
and store the token on the client device, and provide it everytime you want to...

Well, we tackle one, another one appears.

.. _enforce_role:

Enforce role on route
---------------------

Some operations on your server should not only require the user to be logged in,
they also require that the user has a specific role. Yeah, we got that too.

In your imaginary users and pets web app, some users are registered as sellers.
They have special privileges that enables them to perform some operations
and sell food, chains, emmm... pet stuff, you know.

.. code-block:: python3
   :linenos:

    @user.post("/sell")
    @xfss.requires_payload({"item", "price", "quantity"})
    @RemoteSession.requires_role("seller")
    def sell_stuff():
        # You know the deal
        pass

In this case, the 3rd line protects the route, so only users with the seller
role have access to it.
Did you notice the line 2? You can mix some of these to get a specific match
of rules.

.. note::

    Right now. The role protection just works with one role per route.

    We are currently working to improve this and make it so a route can be
    accessed by multiple roles. Don't worry, it will come sooner than you think.