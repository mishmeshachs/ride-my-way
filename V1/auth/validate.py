from flask import make_response, jsonify
import re


def response(status, message, status_code):
    """
    Helper method to make an Http response
    :param status: Status
    :param message: Message
    :param status_code: Http status code
    :return:
    """
    return make_response(jsonify({
        'status': status,
        'message': message
    })), status_code


def empty(**data):
    '''method to validate username input'''
    messages = {}
    for key in data:
        newname = re.sub(r'\s+', '', data[key])
        if not newname:
            message = {'message': key + ' cannot be an empty string'}
            messages.update({key + '-Error:': message})
    return messages


def whitespace(data):
    '''method to validate white'''
    newname = re.sub(r'\s+', '', data)
    afterlength = len(newname)
    actuallength = len(data)
    if afterlength != actuallength:
        return True


def val_none(**data):
    '''method to check none'''
    messages = {}
    for key in data:
        if data[key] is None:
            message = {'message': key + ' cannot be missing'}
            messages.update({key + '-Error:': message})
    return messages


def pass_length(data):
    if len(data) < 8:
        return True


def email_prtn(data):
    pattern = re.match(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data)
    if not pattern:
        return True