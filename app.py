#here I have built app using python, Flask, Pandas and API
#First I imported the modules required
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)
#here the entry point for data is the user for an API
class Users(Resource):
    def get(self): #Here I defined the get method to Retrieve information
        data = pd.read_csv('data/users.csv')  # read CSV
        data = data.to_dict()  # convert dataframe to dictionary
        return {'data': data}, 200  # return data and 200 OK code
    
    def post(self): #here I used post method to Create a REST API resource
        parser = reqparse.RequestParser()  # initialize
        
        parser.add_argument('userId', required=True)  # add args
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)
        
        args = parser.parse_args()  # parse arguments to dictionary
        data = pd.read_csv('data/users.csv')

        if args['userId'] in list(data['userId']): #if already userId exists then display exist
            return {
                'message': f"'{args['userId']}' already exists."
            }, 401
        else:
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'userId': args['userId'],
                'name': args['name'],
                'city': args['city']
            },index=[0])
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('data/users.csv', index=False)  # save back to CSV
            return {'data': data.to_dict()}, 200  # return data with 200 OK
        

    def delete(self): #Here I defined the DELETE method to Delete a REST API resource 
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)  # add args
        args = parser.parse_args()  # parse arguments to dictionary
        data = pd.read_csv('data/users.csv') 
        if args['userId'] in list(data['userId']):
            data = data[data['userId'] != args['userId']] #if the userId is match then seperate all the remaining rows
            data.to_csv('data/users.csv', index=False) #append to new data to csv file.
            return {'data': data.to_dict()}, 200  # return data with 200 OK
        else:
            return{
                'message': f"{args['userId']}does not exist!"},404

    
api.add_resource(Users, '/users')  # '/users' is our entry point for Users

if __name__ == '__main__':
    app.run()
