# security_tools
A repository to store some custom tools I use from time-to-time

## MicroAPI_w_DB
Runs a Flask HTTP server that accepts POST requests and stores the content to a SQLite DB.  Contents of SQLite DB are viewable at the `/results` endpoint.  Used for XSS testing and other tasks requiring an HTTP server.

## AWS_Encryption_Scan
Small script that checks multiple resources (RDS, S3, etc.) for Encryption-at-rest via boto3.  Requires AWS credentials.  

## Secret_Scanning
Clones git repositories and scans them for secrets using Gitleaks.  Requires credentials, git, and (python) gitleaks.