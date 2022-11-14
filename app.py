try:
    from flask import app,Flask
    from flask_restful import Resource, Api
    from apispec import APISpec
    from marshmallow import Schema, fields
    from apispec.ext.marshmallow import MarshmallowPlugin
    from flask_apispec.extension import FlaskApiSpec
    from flask_apispec.views import MethodResource
    from flask_apispec import marshal_with, doc, use_kwargs
    import datetime

    from MyRestApi.ClusterHealth.views import HeathController
    from MyRestApi.Authorization.views import AuthorizationController
    from MyRestApi.StkPush.views import TransactionstkController

except Exception as e:
    print("__init Modules are Missing {}".format(e))

app = Flask(__name__)  # Flask app instance initiated
api = Api(app)  # Flask restful wraps Flask app around it.
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Mpesa Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
           ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access MyRestApi Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/' , # URI to access UI of MyRestApi Doc,
    # 'APISPEC_AUTH': {
    #             'ENABLED': True,
    #             'USERNAME': 'admin',
    #             'PASSWORD': 'admin'
    #         }


})

docs = FlaskApiSpec(app)

SECRET_KEY = '8ee2923d3cd2b2833d3b747173f6c0da'
app.config['JWT_SECRET_KEY'] = SECRET_KEY  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=60)

api.add_resource(HeathController, '/health_check')
docs.register(HeathController)
api.add_resource(AuthorizationController, '/Authorize')
docs.register(AuthorizationController)
api.add_resource(TransactionstkController, '/stk')
docs.register(TransactionstkController)

if __name__ == "__main__":
    app.run()
