from flask import Flask
from flask_restful import Api, Resource, reqparse
from nameparser import HumanName

app = Flask(__name__)
api = Api(app)

post_args = reqparse.RequestParser()
post_args.add_argument("value", type=str, help="Value is required to proceed", required=True)
post_args.add_argument("mode", type=str, help="Choose between phone || name || amount", required=True)
post_args.add_argument("replace_with", type=str, help="Choose either --blank-- || --original--", required=True)


def processing_data(data):
    """Takes in a dict data from the post request, returns a new dict with the data processed"""
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

    else:
        return {'message': {'mode': "phone || name || amount"}}

    return new_data


def name_output_cleanup(name_data, replacement):
    """Takes in the name value as string and replace_with arg as replacement, returns a dict with mapped name"""
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
    """Takes in the phone number as string and replace_with arg as replacement, returns processed phone num or None"""
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


def process_amount(input_string, replacement):
    """Takes in input_string (amount) as a string and replace_with arg as replacement, returns the eval or input_str"""
    try:
        value = eval(input_string)
        if isinstance(value, int):
            return str(value)

        elif isinstance(value, float):
            amount = float(value)
            return "{:.2f}".format(amount)

        if replacement == "--original--":
            return input_string
        else:
            return "--blank--"

    except NameError:
        return input_string


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
