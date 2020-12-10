from flask import request, json, Response, Blueprint, g
from ..processor import extract as ext
from ..processor import converter as con

extractor_api = Blueprint('extractor_api', __name__)


@extractor_api.route('/extract', methods=['POST'])
def extract():
    data = request.get_json()
    bucket = data['bucket']
    item = data['item']

    return process(bucket, item)


@extractor_api.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    bucket = data['bucket']
    item = data['item']

    return custom_response(con.converter_file(bucket, item),200)

@extractor_api.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    bucket = data['bucket']
    item = data['item']

    return custom_response(ext.process_2(bucket, item),200)


def process(bucket, item):
    return custom_response(ext.process(bucket,item), 200)


def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
