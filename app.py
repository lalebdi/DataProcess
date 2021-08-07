from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from nameparser import HumanName

app = Flask(__name__)
api = Api(app)

post_args = reqparse.RequestParser()
post_args.add_argument("value", type=str, help="Value is required to proceed", required=True)
post_args.add_argument("mode", type=str, help="Choose between phone || name || amount", required=True)
post_args.add_argument("replace_with", type=str, help="Choose either --blank-- || --original--", required=True)


def processing_data(data):
    new_data = {}
    new_data["original_value"] = data["value"]
    if data["replace_with"] == "--blank--":
        if data["mode"] == "name":
            name = HumanName(data["value"])
            cleaned_name = name_output_cleanup(name.as_dict())
            new_data["output"] = cleaned_name
        elif data["mode"] == "phone":
            phone_num = extract_phone_number(data["value"])
            new_data["output"] = phone_num
        elif data["mode"] == "amount":
            print("its amount")
    elif data["replace_with"] == "--original--":
        print("Its original")
    return new_data


def extract_phone_number(num):
    phone_num = ""
    for i in num:
        if i.isdigit():
            phone_num += i
    return phone_num


def name_output_cleanup(data):
    name = dict()
    for key, value in data.items():
        if value != "":
            name[key] = value
    return name


class DataProcess(Resource):
    def get(self):
        return {"message": 'This URL that will accept a POST call with the following payload : '
                           '{value: "<value goes here>", mode: "phone || name || amount", "replace_with": "--blank-- || --original--"}'}

    def post(self):
        args = post_args.parse_args()
        output_data = processing_data(args)
        return output_data, 201


api.add_resource(DataProcess, "/")


if __name__ == '__main__':
    app.run(debug=True)
