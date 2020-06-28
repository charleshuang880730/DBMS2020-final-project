from transaction import Handler
from flask import (Flask, render_template, url_for, redirect, request, jsonify)
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def query_page():
    h = Handler()
    condition = request.form.get('input1')
    D_NO = int(request.form.get('d_selector'))
    tmp = h.query_class(condition, D_NO)
    return render_template("show_result.html", result=tmp, mesg=1, user=None)

@app.route('/class', methods=['POST'])
def access_class():
    h = Handler()
    tmp = None
    
    try:
        operation = int(request.form.get('operation'))
        S_NO = int(request.form.get('input2'))
        user = h.query_user(S_NO)
        if(not user):
            raise Exception
        if(operation == 0):
            C_NO = int(request.form.get('input3'))
            h.insert(S_NO, C_NO)
            mesg = "insert table successfully!"
        elif (operation == 1):
            C_NO = int(request.form.get("input3"))
            h.delete(S_NO, C_NO)
            mesg = "delete table successfully!"
        else:
            tmp = h.query(S_NO)
            mesg = None

    except Exception as e:
        print(e)
        mesg = "Oop theres something wrong!"
        user = None

    finally: 
        return render_template("show_result.html", result=tmp, mesg=mesg, user=user)

@app.route('/back', methods=['GET'])
def back_index():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

