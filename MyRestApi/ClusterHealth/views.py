try:
    from flask import Flask, request
    from flask_restful import Resource, Api
    from apispec import APISpec
    from marshmallow import Schema, fields
    from apispec.ext.marshmallow import MarshmallowPlugin
    from flask_apispec.extension import FlaskApiSpec
    from flask_apispec.views import MethodResource
    from flask_apispec import marshal_with, doc, use_kwargs
    from functools import wraps
    import jwt

    print("All imports are ok............")
except Exception as e:
    print("Error: {} ".format(e))

SECRET_KEY = '8ee2923d3cd2b2833d3b747173f6c0da'



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


class HeathController(MethodResource, Resource):

    @verify_token
    @doc(description='This is health Endpoint', tags=['Health Endpoint'])
    def get(self):

        '''
        Get method represents a GET MyRestApi method
        '''
        return {'message': 'APi are working fine'}, 200