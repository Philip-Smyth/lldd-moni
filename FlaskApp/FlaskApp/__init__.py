from flask import Flask as fl
from flask import render_template
import MySQLdb as msql

app = fl(__name__)

@app.route('/')
def homepage():
    node_data = display_node_data()
    return render_template("node_data.html", data=node_data)

#@app.route('/test')
#def test():
#    return render_template()

def display_node_data():
    con = msql.connect(host='localhost', user='root', passwd='password', db='discover')
    cur = con.cursor()
    check = "SHOW TABLES LIKE 'nodes'"
    cur.execute(check)
    result = cur.fetchone()
    if result:
        pass
    else:
        cur.execute('CREATE TABLE nodes (Id INTEGER NOT NULL AUTO_INCREMENT,Hostname VARCHAR(30), MAC_Addr VARCHAR(18),IP_Addr VARCHAR(15), OS VARCHAR(10),OS_Vrs VARCHAR(10), OS_Type VARCHAR(30),OS_Acc VARCHAR(3),PRIMARY KEY (Id))')
    cur.execute('SELECT * from nodes')
    node_data = cur.fetchall()
    return node_data



if __name__ == "__main__":
    app.debug = True
    app.run()
