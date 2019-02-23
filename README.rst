Build your own notification feed
============================================


What's a notification feed?
--------------------------------


Building a scalable notification system is almost entirely identical to building an activity feed.
From the user's perspective the functionality is pretty different.
A notification system commonly shows activity related to your account. 
Whereas an activity stream shows activity by the people you follow.
Examples of Fashiolista's notification system and Facebook's system are shown below.
Fashiolista's system is running on Stream Framework.


.. image:: https://raw.githubusercontent.com/tschellenbach/Stream-Framework/master/docs/_static/notification_system.png
.. image:: https://raw.githubusercontent.com/tschellenbach/Stream-Framework/master/docs/_static/fb_notification_system.png


Notification Feed Architecture
--------------------------------------


The main.py will start 2 process. One for notification watcher and the other for notification sender.
Here we watch issues change in github repo and send the issues changes to manager email.


You may construct your own topic in watcher.


Tutorial
----------------------

Use docker-compose

::

 docker-compose -f example.com up -d




