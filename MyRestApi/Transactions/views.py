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
    from functools import wraps
    import jwt

    print("All Modules are loaded ...")
except Exception as e:
    print("some modules are Missing ")

SECRET_KEY = '8ee2923d3cd2b2833d3b747173f6c0da'

class TransactionsPutSchema(Schema):
    phone = fields.String(required=True, description="mobile number")
    amount=fields.String(required=True, description="amount")


def verify_token(f):

    @wraps(f)
    def decorator(*args,**kwargs):
        token = request.headers.get('token', None)
        print(token)
        if token is None:
            return {"Message":"Your are missing Token"}
        else:
            try:
                data = jwt.decode(token, SECRET_KEY)
                if str(data['user']) =='admin':
                    return f(*args, **kwargs)
                else:
                    return {"Message": "Token is invalid"}
            except Exception as e:
                return {"Message":"Token is expired "+str(e)}
    return decorator


class TransactionsController(MethodResource, Resource):

    @verify_token
    @doc(description='Add Documentation ', tags=["Mpesa stk push"])
    @use_kwargs(TransactionsPutSchema, location=('json'))
    def post(self, **kwargs):
        try:
            'Developer writes the code here '
            return {'message': 'APi iko fine'}, 200
        except Exception as e:
            print(e)
            return {
                "status": -1,
                "error": {
                    "message": str(e)
                }
            }

