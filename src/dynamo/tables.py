import boto3

dynamodb = boto3.resource('dynamodb')


def put_file_dictionary(data):

    table = dynamodb.Table('nlp_file_dictionary')
    response = table.put_item(
       Item=data
    )
    return response


def put_file_metadata(data):
    table = dynamodb.Table('nlp_file_metadata')
    response = table.put_item(
       Item=data
    )
    return response