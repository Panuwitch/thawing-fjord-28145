#Personal Information
#Serverside

from flask import Flask
from flask_restful import Api,Resource,abort,reqparse,marshal_with,fields
from flask_sqlalchemy import SQLAlchemy,Model
app=Flask(__name__)

#database
db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///flaskherokudatabase.db"
api=Api(app)

class PersonModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(100),nullable=False)
    Nickname=db.Column(db.String(100),nullable=False)   
    Instagram=db.Column(db.String(100),nullable=False)
    Age=db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"Person(Name={Name},Nickname={Nickname},Instagram={Instagram},Age={Age})"

db.create_all()

#Request Parser
data_add_args=reqparse.RequestParser()
data_add_args.add_argument("Name",type=str,required=True,help="Please enter the name with capital letters in the first part of name.")
data_add_args.add_argument("Nickname",type=str,required=True,help="Please enter nickname with capital letters in the first part of nickname.")
data_add_args.add_argument("Instagram",type=str,required=True,help="Please enter Instagram's name ")
data_add_args.add_argument("Age",type=str,required=True,help="Please enter age with letters")

#Update Request Parser
data_update_args=reqparse.RequestParser()
data_update_args.add_argument("Name",type=str,help="Please enter the name to be edit.")
data_update_args.add_argument("Nickname",type=str,help="Please enter the nickname to be edit.")
data_update_args.add_argument("Instagram",type=str,help="Please enter the Instagram's name to be edit.")
data_update_args.add_argument("Age",type=str,help="Please enter the age to be edit.")


resource_field={
    "id":fields.Integer,
    "Name":fields.String,
    "Nickname":fields.String,
    "Instagram":fields.String,
    "Age":fields.String
}


#design
class Information(Resource):

    @marshal_with(resource_field)
    def get(self,person_id):
        result=PersonModel.query.filter_by(id=person_id).first()
        if not result:
            abort(404,message="Not found the person's information.")
        return result
    
    @marshal_with(resource_field)
    def post(self,person_id):
        result=PersonModel.query.filter_by(id=person_id).first()
        if result:
            abort(409,message="This ID have been saved.")
        args=data_add_args.parse_args()
        person=PersonModel(id=person_id,Name=args["Name"],Nickname=args["Nickname"],Instagram=args["Instagram"],Age=args["Age"])
        db.session.add(person)
        db.session.commit()
        return person,201
    
    @marshal_with(resource_field)
    def patch(self,person_id):
        args=data_update_args.parse_args()
        result=PersonModel.query.filter_by(id=city_id).first()
        if not result:
           abort(404,message="Not found person's information.")
        if args["Name"]:
            result.Name=args["Name"] 
        if args["Nickname"]:
            result.Nickname=args["Nickname"]
        if args["Instagram"]:
            result.Instagram=args["Instagram"]
        if args["Age"]:
            result.Age=args["Age"]

        db.session.commit()
        return result
#call
api.add_resource(Information,"/Name/<int:person_id>")

if __name__ == "__main__":
    app.run(debug=True)
