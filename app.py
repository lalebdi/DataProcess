from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

post_args = reqparse.RequestParser()
post_args.add_argument("value", type=str, help="Value is required to proceed", required=True)
post_args.add_argument("mode", type=str, help="Choose between phone || name || amount", required=True)
post_args.add_argument("replace_with", type=str, help="Choose either --blank-- || --original--", required=True)


class DataProcess(Resource):
    def get(self):
        return {"message": 'This URL that will accept a POST call with the following payload : '
                           '{value: "<value goes here>", mode: "phone || name || amount", "replace_with": "--blank-- || --original--"}'}

    def post(self):
        args = post_args.parse_args()
        return args, 201


api.add_resource(DataProcess, "/")


if __name__ == '__main__':
    app.run(debug=True)
