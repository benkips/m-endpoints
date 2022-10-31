try:
    from flask import Flask, Request, request, app, jsonify
    from flask_restful import Resource, Api, reqparse
    from apispec import APISpec
    from marshmallow import Schema, fields
    from apispec.ext.marshmallow import MarshmallowPlugin
    from flask_apispec.extension import FlaskApiSpec
    from flask_apispec.views import MethodResource
    from flask_apispec import marshal_with, doc, use_kwargs
    import json
    import datetime
    import jwt

    print("All imports are ok............")
except Exception as e:
    print("Error: {} ".format(e))


class AuthorizationPutSchema(Schema):
    Username = fields.String(required=True, description="Username to authorize")
    Password = fields.String(required=True, description="Password to authorize")


USER_DATA = {
    "admin": "admin"
}
SECRET_KEY = '8ee2923d3cd2b2833d3b747173f6c0da'

class AuthorizationController(MethodResource, Resource):

    @doc(description='Basic Auth  ', tags=["Authorization"])
    @use_kwargs(AuthorizationPutSchema, location='json')
    def post(self, **kwargs):
        json_data = request.get_json(force=True)
        try:
            username = kwargs.get('Username','default')
            password = kwargs.get('Password','default')
            if not (username, password):
                return False
            else:
                if USER_DATA.get(username) == password:
                    token = jwt.encode(
                        {
                            'user': username,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                        }
                        , SECRET_KEY)

                    return jsonify({
                        'token': token.decode('UTF-8')
                    })

        except Exception as e:
            print(e)
            return {
                "status": -1,
                "error": {
                    "message": str(e)
                }
            }
