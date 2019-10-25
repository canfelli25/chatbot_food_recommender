from flask import jsonify

def return_message(status_code, status, message):
    return jsonify(
        status_code=status_code,
        status=status,
        message=message
    )

def success_message(message):
    return return_message(200, "OK", message)
