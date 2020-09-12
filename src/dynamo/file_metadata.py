import boto3


def put_file_metadata(data, dynamodb=None):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('nlp_file_metadata')
    response = table.put_item(
       Item=data
    )
    return response
