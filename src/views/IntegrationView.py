from flask import request, json, Response, Blueprint, g
from ..processor import extract as ext

extractor_api = Blueprint('extractor_api', __name__)


@extractor_api.route('/extract', methods=['POST'])
def extract():

    data = request.get_json()
    resp = None
    bucket = data['bucket']
    item = data['item']

    return process(bucket, item)


def process(bucket, item):
    return custom_response(ext.process(bucket,item), 200)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
