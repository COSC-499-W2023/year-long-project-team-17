[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=12113659&assignment_repo_type=AssignmentRepo)
# Project-Starter

## Step 1: Download the required software
- python
- libreoffice
- mySQL (Workbench)
- Memcashed

## Step 2: Clone the repository

```commandline
git clone https://github.com/COSC-499-W2023/year-long-project-team-17.git
```
or 
```commandline
git clone git@github.com:COSC-499-W2023/year-long-project-team-17.git
```

## Step 3: setup environment variables
```commandline
cp .env.example .env
```

Fill in the values of the variables in .env file


## Step 4: Create a Virtual Environment
```commandline
python -m venv virt
```

For Windows
```commandline
source virt/Scripts/activate
```

For Linux or MacOS
```commandline
source virt/bin/activate
```

## Step 5: Install the required dependencies
```commandline
pip install -r app/requirements.txt
```

## Step 6: Create the database
```commandline
python mydb.py
```

## Step 7: Make the necessary migrations to the database

```commandline
python app/manage.py make migrations
```

```commandline
python app/manage.py migrate
```

## Step 8: Start the system

```commandline
python app/manage.py runserver
```

## Run automated tests
```commandline
python app/manage.py test
```

Please use the provided folder structure for your docs (project plan, design documentation, communications log, weekly logs, and final documentation), source code, testing, etc.    You are free to organize any additional internal folder structure as required by the project.  Please use a branching workflow and once an item is ready, do remember to issue a PR, code review, and merge it into the develop branch and then the master branch.
```
.
├── year-long-project-team-17 # Documentation files (alternatively `doc`)
│   ├── app
        ├──dcrm
        ├──media
            ├──presentation_templates
            ├──presentations
            ├──profile_pictures
        ├──staticfiles
            ├──admin
            ├──django_extensions
            ├──icon_cache  
        ├──util
        ├──website
            ├──migrations
            ├──templates
                ├──images
                ├──partials
                ├──static
                    ├──images
            ├──tests
        ├──.env.example
        ├──gitignore
        ├──__init__.py
        ├──manage.py
        ├──mydb.py
        ├──requirements.txt
│   ├── docs              
│       ├──  weekly logs              
├── app                     
├── tests 
├── utils
└── README.md
```
