# Micro API (Python)

### What it does
Useful micro-API for recieving and taking action on GET and POST requests.  Current configuration is capable of responding to GET
requests with a malicious file, and accepting POST requests.  POST requests integrate with a Python-generated SQLite database to store extracted information.

Highly useful for offensive operations - specifically XSS or any other attack path that can induce HTTP requests from a victim web server. The database and POST request routing are configured to accept usernames and user tokens/cookies, and store them locally in a database for future use.  

With some slight tweaks, can also be used to conduct various kinds of webscraping.  

Malicious JS files not included in repo currently.  

### Steps to use

First, run `python3 database.py --make` to initialize the database locally.  Run `python3 microAPI.py` to start the API.  At this point, a simple request
like `curl http://{URL}:{PORT} -X POST -d "user=Foo&token=Bar"` should be enough to confirm that the API is accepting POST traffic and logging to the database.  

To confirm that the database is recording input, `python3 database.py --query` should return all table entries.
