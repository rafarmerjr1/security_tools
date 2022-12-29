# Micro API (Python)

### What it does
Micro-API for recieving and taking action on GET and POST requests.  Current configuration is capable of responding to GET
requests with a malicious file, and accepting POST requests.  POST requests integrate with a Python-generated SQLite database to store extracted information.

Useful for offensive operations - specifically XSS or any other attack path that can induce HTTP requests from a victim web server. The database and POST request routing are configured to accept usernames and user tokens/cookies, and store them locally in a database for future use.  

With some slight changes, can also be used to conduct various kinds of webscraping.  

Malicious JS files not included in repo currently.  

### Usage
```
usage: microAPI.py [-h] [--new] [--dbname DBNAME] [--existing]

options:
  -h, --help       show this help message and exit
  --new            Make new Database
  --dbname DBNAME  Name for Database
  --existing       Use an existing database
```

### Steps to use
Run `python3 microAPI.py --new` to start the API for the first time. This will create a new SQLite object recording data into 'user_data_store.db'. At this point, a simple request like `curl http://{URL}:{PORT}/tokens -X POST -d "user=Foo&token=Bar"` should be enough to confirm that the API is accepting POST traffic and logging to the database.  

### Viewing Results
Results can be viewed at the '/results' endpoint in a browser.  

### Use an existing or new .db file
`python3 microAPI.py --existing --dbname name_of__existing_db_file.db` can be used to specifically select a database file for use.

`python3 microAPI.py --new name_of_NEW_db_file.db` can be used to specify the name of a new database file. Without any name specified with the `--dbname` flag, the default name will be used.

### Using the database locally (without the MicroAPI)
`python3 database.py --make` can be used to initialize and interact with a new database locally.  

Data can be manually added to the database with '--add' accompanied by '--user' and '--token'.  To confirm that the database is recording input, `python3 database.py --query` should return all table entries.
