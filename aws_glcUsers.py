import boto3,json


aws_key = "your AWS key"
aws_secret = "your AWS secret"

import datetime

# Amazon Cognito User Pool Configs
LIMIT = 60
REGION = 'us-east-2'
USER_POOL_ID = 'us-east-2_sDm0qFJ4T'

client = boto3.client('cognito-idp',aws_access_key_id=aws_key,
         aws_secret_access_key= aws_secret,region_name=REGION)
pagination_token = ""


def get_all_users():
    cognito = boto3.client('cognito-idp',aws_access_key_id=aws_key,
         aws_secret_access_key= aws_secret,region_name=REGION)

    users = []
    next_page = None
    kwargs = {
        'UserPoolId': USER_POOL_ID
    }

    users_remain = True
    while users_remain:
        if next_page:
            kwargs['PaginationToken'] = next_page
        response = cognito.list_users(**kwargs)
        users.extend(response['Users'])
        next_page = response.get('PaginationToken', None)
        users_remain = next_page is not None

    return users


#allUsers = get_all_users()


#marketing items

###get marketing items too
def getMarketingList():
    your_table = "GLCoverage_Marketing"
    ###get story data starts
    dynamodb = boto3.client('dynamodb',aws_access_key_id=aws_key,
             aws_secret_access_key= aws_secret,region_name="us-east-2")
    response = dynamodb.scan(
        TableName=your_table,
        Select='ALL_ATTRIBUTES')
    email_list_data = response['Items']
    return email_list_data

##get projects
def getAllProjects():
    your_table = "GLCoverage_Project"
    ###get story data starts
    dynamodb = boto3.client('dynamodb',aws_access_key_id=aws_key,
             aws_secret_access_key= aws_secret,region_name="us-east-2")

    # Initialize an empty list to store all project data
    all_project_data = []

    # Initial call to scan the table
    scan_kwargs = {
        "TableName": your_table,
        "Select": "SPECIFIC_ATTRIBUTES",
        "FilterExpression": "attribute_exists(userId) AND userId <> :empty",
        "ProjectionExpression": "title, userId, uploadTime",
        "ExpressionAttributeValues": {":empty": {"S": ""}}
    }

    done = False
    start_key = None

    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = dynamodb.scan(**scan_kwargs)
        all_project_data.extend(response['Items'])
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None

    return all_project_data

    #return email_list_data