""" This is the app"""
from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import requests
import urllib

from taxes import Taxes
from roadwork import RoadWork
from query import Query
from queryFactory import QueryFactory
from openState import OpenState
from closedState import ClosedState
from client import Client
from advisorservice import AdvisorService

mysql = MySQL()

# initializing a variable of Flask
app = Flask(__name__, template_folder="templates")

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'council_query'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/addQuery')
def new_query():
    return render_template('newQuery.html')


@app.route('/updateQuery/<username>')
def update_query(username):
    # get query of the user and display the question.
    # display text area to allow for answer.
    user = username
    print('the query belongs to user:', user)
    try:
        con = mysql.connect()  # set up database connection
        cur = con.cursor()
    except:
        con.rollback()
    finally:
        sql_select_query = """SELECT query.username, query.type,query.state,query.question, query.answer,query.address FROM query WHERE  
        query.username = %s """
        cur.execute(sql_select_query, (user,))
        data = cur.fetchall()
        address = data[0][5]
        # API to find location details --------------------------------------------------------------------
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'
        response = requests.get(url).json()
        print("" + str(response[0]))  # response details
        retrieved_address = response[0]["display_name"]  # retrieve response details form the attribute, display_name
        # -------------------------------------------------------------------------------------------------
        for d in data:
            print(d)
        con.commit()
    return render_template('update.html', data=data, address=retrieved_address)


@app.route('/removeQuery/<username>')
def remove_query(username):
    user = username
    print('the query belongs to user:', user)
    try:
        con = mysql.connect()  # set up database connection
        cur = con.cursor()
    except:
        con.rollback()
    finally:
        state = 'Query Closed'
        cur.execute('UPDATE query SET state=%s WHERE username=%s', (state, username))
        sql_select_query2 = """SELECT query.username, query.type,query.state,query.question, query.answer FROM query WHERE  
           query.username = %s """

        cur.execute(sql_select_query2, (user,))
        data = cur.fetchall()
        for d in data:
            print(d)
        con.commit()
    return render_template('remove.html', data=data)


@app.route("/dashboard", methods=['GET'])
def dashboard():
    names = ""
    try:
        con = mysql.connect()  # set up database connection
        cur = con.cursor()
    except:
        con.rollback()
    finally:
        cur.execute('SELECT client.username, client.email,  '
                    'query.type,query.state, query.question, query.answer '
                    'FROM client, query '
                    'WHERE client.username = query.username ')
        rows = cur.fetchall()
        con.commit()
        # ClientAPI to find clients details --------------------------------------------------------------------
        advisors = AdvisorService.get_advisors()
        for advisor in advisors:
            name = advisor['advisor']
            names = names + "; " + name
        print("get a list of advisors via API ")
        # ------------------------------------------------------------------------------------------------------
        return render_template("index.html", rows=rows, names=names)

        con.close()


@app.route('/register_query', methods=['POST', 'GET'])
def register_query():
    if request.method == 'POST':
        rows = []
        names = ""
        try:
            print("--------------------------Registering Query----------------------------------------")
            con = mysql.connect()  # set up database connection
            cur = con.cursor()
            username = request.form['username']  # retrieve form data
            email = request.form['email']
            the_address = request.form['address']
            query_type = request.form['query_type']
            question = request.form['question']
            social_number = request.form['socialNo']

            print("to register a user")
            user = Client()
            user.setName(username)
            user.setEmail(email)
            #  GoF composite pattern (demo only)------------
            user.addUsers(user)
            print("users names: " + user.getUsersNames())
            #  ---------------------------------------------

            user.setQuery()  # GoF factory method pattern

            # insert data to the database
            cur.execute('INSERT INTO client (username, email)'
                        'VALUES( %s, %s)',
                        (username, email))

            con.commit()
            print("write to the user table")

            #  GoF factory method pattern----------------
            user_factory = user.getQuery()
            query_obj = user_factory.getQuery(query_type)
            if query_obj is not None:
                query_obj.set_username(username)
                query_obj.set_type(query_type)
                query_obj.setQuestion(question)
                # GoF state pattern
                start_state = OpenState()  # new query will have an open state
                start_state.querState(query_obj)
                state = query_obj.get_state()
                print('the set state is: ', state)
                # -----------------------------
            #  ---------------------------------------

            state = query_obj.get_state()
            print('the set state globaly is: ', state)
            print('query type:', query_obj.get_type().lower())

            if query_obj.get_type().lower() == "road_work":
                query_obj.setAddress(the_address)
                address = query_obj.getAddress()
                cur.execute('INSERT INTO query (username, type, state, question,address )VALUES( %s, %s, %s, %s, %s)',
                            (username, query_type, state, question, address))
                print("The query is road work related.")
            elif query_obj.get_type().lower() == "taxes":
                query_obj.setSocialNumber(social_number)
                social_no = query_obj.getSocialNumber()
                cur.execute('INSERT INTO query (username, type, state, question, socialNumber)VALUES( %s, %s, %s, '
                            '%s, %s)',
                            (username, query_type, state, question, social_no))
                print("The query is taxes related.")
            #  ---------------------------------------------
            con.commit()
            print("write to the query table")

            # ClientAPI to find clients details --------------------------------------------------------------------
            advisors = AdvisorService.get_advisors()
            for advisor in advisors:
                name = advisor['advisor']
                names = names + "; " + name
            print("get a list of advisors via API ")
            # ------------------------------------------------------------------------------------------------------

            # testing - retrieve data from the database
            cur.execute('SELECT client.username, client.email,  '
                        'query.type,query.state, query.question, query.answer '
                        'FROM client, query '
                        'WHERE client.username = query.username ')

            rows = cur.fetchall()
            row_num = len(rows)
            print("user:  ", row_num)
            for row in rows:
                print("username: ", row[0])
                print("email: ", row[1])

            con.commit()
            rows = rows
            return render_template("index.html", rows=rows, names = names)
        except:
            con.rollback()
            print('Hit exception')
        finally:
            rows = rows
            names = names
            return render_template("index.html", rows=rows, names = names)
            con.close()


@app.route('/update', methods=['POST', 'GET'])
def update():
    names = ""
    if request.method == 'POST':
        try:
            username = request.form['username']
            answer = request.form['answer']
            con = mysql.connect()
            cur = con.cursor()
            cur.execute('UPDATE query SET answer=%s WHERE username=%s', (answer, username))
            con.commit()
            print("update the query table")

            # ClientAPI to find clients details --------------------------------------------------------------------
            advisors = AdvisorService.get_advisors()
            for advisor in advisors:
                name = advisor['advisor']
                names = names + "; " + name
            print("get a list of advisors via API ")
            # ------------------------------------------------------------------------------------------------------
            # testing - retrieve data from the database
            cur.execute('SELECT client.username, client.email,  '
                        'query.type,query.state, query.question, query.answer '
                        'FROM client, query '
                        'WHERE client.username = query.username ')
            rows = cur.fetchall()
            con.commit()

        except:
            con.rollback()
        finally:
            rows = rows
            return render_template("index.html", rows=rows, names= names)
            con.close()


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    names = ""
    if request.method == 'POST':
        try:
            username = request.form['username']
            con = mysql.connect()
            cur = con.cursor()

            cur.execute('DELETE FROM client WHERE username=%s', username)
            con.commit()
            print("delete the staff from the staff table")

            cur.execute('DELETE FROM query WHERE username=%s', username)
            con.commit()

        except:
            con.rollback()

        finally:
            cur.execute('SELECT client.username, client.email,  '
                        'query.type,query.state, query.question, query.answer '
                        'FROM client, query '
                        'WHERE client.username = query.username ')
            rows = cur.fetchall()
            con.commit()

            # ClientAPI to find clients details --------------------------------------------------------------------
            advisors = AdvisorService.get_advisors()
            for advisor in advisors:
                name = advisor['advisor']
                names = names + "; " + name
            print("get a list of advisors via API ")
            # ------------------------------------------------------------------------------------------------------

            return render_template("index.html", rows=rows, names = names)
            con.close()


if __name__ == "__main__":
    app.run()
