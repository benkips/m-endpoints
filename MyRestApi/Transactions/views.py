

try:
    from flask import app, Flask, request
    from flask_restful import Resource, Api, reqparse
    import json
    import os
    from marshmallow import Schema, fields
    from flask_apispec.views import MethodResource
    from flask_apispec import marshal_with, doc, use_kwargs
    import os
    from enum import Enum
    import jwt
    import requests
    import ast
    from functools import wraps
    print("All Modules are loaded ...")
except Exception as e:
    print("some modules are Missing ")

SECRET_KEY = '8ee2923d3cd2b2833d3b747173f6c0da'

def verify_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('token', None)
        if token is None:
            return {"Message": "Your are missing Token"}
        else:
            try:
                data = jwt.decode(token, SECRET_KEY)
                if str(data['user']) == 'admin':
                    return f(*args, **kwargs)
                else:
                    return {"Message": "Token is invalid"}
            except Exception as e:
                return {"Message": "Token is expired " + str(e)}

    return decorator

class TransactionPutSchema(Schema):
    mpesacode = fields.String(required=True, description="mpesacode from the order")





class TransactionController(MethodResource, Resource):

    @verify_token
    @doc(description='Add Documentation ', tags=["Get mpesa transaction from mpesacode"])
    @use_kwargs(TransactionPutSchema, location=('json'))
    def post(self, **kwargs):
        try:
            mpesacode = kwargs.get('mpesacode', 'default')

            if str(mpesacode) == 10 :
                return {'message': 'invalid amount or phone number'}, 200
            else:
                if len(mpesacode)==10:
                    jsndata = {'mpesacode': str(mpesacode)}
                    url = 'https://payments.ekarantechnologies.com/Getransaction'
                    myjson = jsndata

                    returnmsg = requests.post(url, json=myjson)
                    print(returnmsg.text)
                    returnmsga = ast.literal_eval(returnmsg.text)
                    if returnmsg.text.__contains__('fail'):
                        return {'message': returnmsga.get('fail')}, 200
                    else:
                        return {'message': returnmsga.get('data')}, 200
                else:
                    return {'message': 'invalid mpesacode'}, 200
        except Exception as e:
            print(e)
            return {
                "status": -1,
                "error": {
                    "message": str(e)
                }
            }

