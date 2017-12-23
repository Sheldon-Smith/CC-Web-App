# CC-Web-App

You can use the requirements.txt piped to pip to install dependencies. You will need to create a .env file with a secret key in it. The easiest way to
get one is to create a new project in Django and then just copy that key. Lastly, you will need to set up postgres. You can either edit the settings/base.py file to match your own configuration or match your configuration to my setup.
If you edit this file it will make version control a bit weird, make sure if you change it you add it as another entry so it doesn't break someone else's database connection
