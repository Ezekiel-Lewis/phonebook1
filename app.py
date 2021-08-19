from flask import Flask, render_template, request, redirect, url_for #looking for template directory
from flask_sqlalchemy import SQLAlchemy #saves contact items to library for handling database
#SQLAlchemy is a library that facilitates the communication between Python programs and databases.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #Name of path to DB, relative path, advs this was dict, used brackets
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True) #structuring DB, creating a unique value for each contact item
    title = db.Column(db.String(100)) #string must not exceed 100 char
    complete = db.Column(db.Boolean)


@app.route('/')
def index(): #prints contact list
    contact_list = Contact.query.all()
    print(contact_list)
    return render_template('index.html', contact_list=contact_list)
@app.route("/add", methods=["POST"]) #Queries db to get this item
def add():
    #adds new item
    title = request.form.get("title")
    contact_id = Contact(title=title, complete=False)
    db.session.add(contact_id) #add list item to DB
    db.session.commit()
    return redirect(url_for("index")) # redirects user to index
@app.route("/update/<int:id>", methods =['POST', 'GET'])
def update(id):
    contact = Contact.query.filter_by(id=id).first()
    print(request.method)
    if request.method == 'POST':
        print("inside if")

        contact.title = request.form['name']
        print(request.form)
        try: 
            db.session.commit()
            return redirect("/")
        except:
            return "Error"
    else:
        print("inside else")
        return render_template('update.html',contact=contact)

    #updates new item
    # contact_id = contact.query.filter_by(id=contact_id).first()
    # contact_id.complete = not contact_id.complete
    # db.session.commit()
    # return redirect(url_for("index"))
@app.route("/delete/<int:contact_id>")
def delete(contact_id):
    contact_id = Contact.query.filter_by(id=contact_id).first()
    db.session.delete(contact_id)
    db.session.commit()
    return redirect(url_for("index"))
if __name__ == "__main__":
    db.create_all() #creates database file
    app.run(host ='0.0.0.0', port = 5000, debug = True)