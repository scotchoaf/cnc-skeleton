# cnc-skeleton
Canned skeleton setup for pan-cnc. This repo can be used as a starting point to build a new CNC application. CNC is a 
library that makes it easy to build API driven web based applications. With this you can quickly build web-forms
to populate API payloads, generate XML fragments for PAN-OS API calls, or spin up infra using terraform. The operator
of the application only interacts with the simple menu system and is abstracted away from the underlying technology. 

For complete details, see the [PAN-CNC app.](https://github.com/PaloAltoNetworks/pan-cnc/blob/master/docs/Installation.md)
on [Github](www.github.com).

## Building a new App using the CNC library

#### Generic folder structure

```bash
cnc-skeleton/
└── src
    └── cnc-app-name
        ├── .pan-cnc.yaml
        ├── snippets
        │   └── README.md
        └── views.py
```


All folders in the 'src' directory are treated as cnc 'apps'. The CNC library will try to automatically load them 
as Django apps on startup. The two most important files are the `.pan-cnc.yaml` and the `views.py` files. 
All your code will live in `src/$APP_NAME/views.py`


#### Install CNC as a submodule to your repo

```bash

git submodule add -b master git@github.com:PaloAltoNetworks/pan-cnc.git cnc

```

You may have to do

```bash

git submodule update --init

```

inside the cnc directory to activate and pull the submodule content to cnc. First time user may also require a python
virtual environment and install of the cnc requirements

```bash

cd cnc
pip install -r requirements.txt

```

You should now have two top level directories: `src` and `cnc`. 

## Running Pan-CNC

#### 1. Build the database
```bash

./cnc/manage.py migrate

```

#### 2. Create a new user

NOTE: In the below command, change ***email address*** and ***passwd*** to your respective entries .Common practice 
is to have the password be the name of the app, unless specifically spelled out in your documentation.

```bash

./cnc/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('paloalto', 'admin@example.com', 'passwd')"

```

#### Local Development

You can launch this new app with the following commands:

```bash
cd cnc
celery -A pan_cnc worker --loglevel=info  & ./manage.py runserver 8080

```

This will start a background task worker and then start the application on port `8080`. You can login using the 
`username` and `password` specified above. 
