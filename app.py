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
    template = [("original_value", data["value"]), ("mode", data["mode"])]
    new_data = dict(template)

    if data["mode"] == "name":
        name = name_output_cleanup(data["value"], data["replace_with"])
        new_data["output"] = name

    elif data["mode"] == "phone":
        phone_num = extract_phone_number(data["value"], data["replace_with"])
        new_data["output"] = phone_num

    elif data["mode"] == "amount":
        total_amount = process_amount(data["value"], data["replace_with"])
        new_data["output"] = total_amount

    return new_data


def name_output_cleanup(name_data, replacement):
    unprocessed_name = HumanName(name_data).as_dict()
    values = ['first', 'middle', 'last']
    new_name = dict()

    for key, value in unprocessed_name.items():
        if value != "":
            new_name[key] = value

    if all(key in new_name for key in values):
        return new_name
    else:
        if replacement == "--original--":
            new_name = name_data
        else:
            new_name = dict([(key, "--blank--") for key in values])

    return new_name


def extract_phone_number(num, replacement):
    phone_num = ""
    for i in num:
        if i.isdigit():
            phone_num += i

    if len(phone_num) != 10:
        if replacement == "--blank--":
            phone_num = replacement
        else:
            phone_num = num

    return phone_num


def process_amount(string, replacement):
    value = eval(string)
    if isinstance(value, int):
        return str(value)

    elif isinstance(value, float):
        amount = float(value)
        return "{:.2f}".format(amount)

    if replacement == "--original--":
        return string
    else:
        return "--blank--"


class DataProcess(Resource):
    def get(self):
        return {"message": 'This URL will accept a POST call with the following payload : '
                           '{value: "<value goes here>", mode: "phone || name || amount", "replace_with": "--blank-- || --original--"}'}

    def post(self):
        args = post_args.parse_args()
        output_data = processing_data(args)
        return output_data, 201


api.add_resource(DataProcess, "/")


if __name__ == '__main__':
    app.run(debug=True)
