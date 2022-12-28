# Creating a database via Python to store XSS attack information.
import sqlite3
import argparse

####################################
# CREATING CONNECTION AND DATABASE #
####################################

def define_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_db(conn):
    makeScrapeTable="""CREATE TABLE IF NOT EXISTS webscrape (
        id integer PRIMARY KEY,
        users text NOT NULL,
        tokens text);"""
    try:
        c = conn.cursor()
        c.execute(makeScrapeTable)
    except sqlite3.Error as e:
        print(e)

############################################
# Database functions, insert, query, delete #
############################################

def insert_data(conn, users, tokens):
    Inserttokens = """INSERT INTO webscrape ( users, tokens )
        VALUES (?,?);""" 
    data = (users, tokens)
    try: 
        c = conn.cursor()
        c.execute(Inserttokens, data)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def get_table(conn):
    table_query = """SELECT * from webscrape;"""
    table_data = []
    try:
        c = conn.cursor()
        c.execute(table_query)
        rows = c.fetchall()
        for row in rows:
            table_data.append(row)
        return table_data
    except sqlite3.Error as e:
        print(e)

def get_users_specific(conn, users):
    table_query = """SELECT users,tokens from webscrape WHERE users = ?;"""
    users = str(users)
    tokens = []
    try:
        c = conn.cursor()
        c.execute(table_query, (users,))
        rows = c.fetchall()
        for row in rows:
            tokens.append(row)
        return tokens
    except sqlite3.Error as e:
        print(e)

def get_users(conn):
    table_query = """SELECT users from webscrape;"""
    users = []
    try:
        c = conn.cursor()
        c.execute(table_query)
        rows = c.fetchall()
        for row in rows:
            users.append(row[0])
        return users
    except sqlite3.Error as e:
        print(e)

def delete_row(conn, users):
    table_query = """DELETE FROM webscrape WHERE users=?;"""
    users = str(users)
    try:
        c = conn.cursor()
        c.execute(table_query, (users,))
        conn.commit()
        return True
    except:
        return False


##########################################
# Main function calls if called directly #
#      and not as an import              #
##########################################

if __name__ == "__main__":
    database = r"user_store.db"  
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--make', help='Make Database', action='store_true')
    group.add_argument('--add', help='Add User Information', action='store_true')
    group.add_argument('--query', help='Get Table Data', action='store_true')
    group.add_argument('--getUsers', help='Get all Users', action='store_true')
    group.add_argument('--delete', help='Delete a row by username', action='store_true')
    parser.add_argument('--users','-U')
    parser.add_argument('--tokens','-T')
    args = parser.parse_args()

    conn = define_connection(database) #Leave this here

    if (args.make):     # Create Database
        create_db(conn)
    elif (args.add):            # Insert user and token
        if (args.users is None and args.tokens is None):
            parser.error("Insert statement requires '--users' and '--tokens'")
        else:
            if insert_data(conn, args.users, args.tokens):
                print("Added to database info for: " + args.use)
            else:
                print("Error...")
    elif (args.query): 
        if (args.users is None): # if no users queried, provide all of table
            table = get_table(conn)
            if table:
                for data in table:
                        print(data)
            else:
                print("Error...")
        elif (args.users is not None): # query specific user
            tokens = get_users_specific(conn, args.users)
            if tokens:
                for token in tokens:
                    print(token)
            else:
                print("Error...")
    if (args.getUsers):     # list all users
        users = get_users(conn)
        if users:
            for user in users:
                print(user)
        else:
            print("Error...")
    if (args.delete):       # Delete a row by user name
        if (args.users is None):
            print("Cannot delete without specifying --users flag")
        if (args.users is not None):
            if delete_row(conn, args.users):
                print("Deleted %s" % args.users)
            else:
                print("Error.")
