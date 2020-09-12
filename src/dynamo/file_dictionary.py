import boto3


def put_file_dictionary(data, dynamodb=None):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('nlp_file_dictionary')
    response = table.put_item(
       Item=data
    )
    return response
