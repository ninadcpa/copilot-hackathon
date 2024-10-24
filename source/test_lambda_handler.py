import json
import boto3
from moto import mock_dynamodb2, mock_iam, mock_sts
from unittest.mock import patch
import pytest
from source.lambda_handler import lambda_handler

# Fixtures for mocking AWS services
@pytest.fixture
def dynamodb_setup():@pytest.fixture@pytest.fixture
    with mock_dynamodb2():tup():tup():
        dynamodb = boto3.resource('dynamodb')b2():b2():
        table = dynamodb.create_table(esource('dynamodb')esource('dynamodb')
            TableName='hackathon-user-table',
            KeySchema=[{'AttributeName': 'userid', 'KeyType': 'HASH'}],table',table',
            AttributeDefinitions=[{'AttributeName': 'userid', 'AttributeType': 'S'}],rid', 'KeyType': 'HASH'}],rid', 'KeyType': 'HASH'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}eType': 'S'}],eType': 'S'}],
        )
        yield table
ield tableield table
@pytest.fixture
def iam_setup():@pytest.fixture@pytest.fixture
    with mock_iam():::
        yield boto3.client('iam')m():m():
client('iam')client('iam')
@pytest.fixture
def sts_setup():@pytest.fixture@pytest.fixture
    with mock_sts():::
        yield boto3.client('sts')s():s():
client('sts')client('sts')
# Test cases
def test_lambda_handler_missing_userid():def test_lambda_handler_missing_userid():def test_lambda_handler_missing_userid():
    event = {}
    context = {}{}{}
    response = lambda_handler(event, context)ambda_handler(event, context)ambda_handler(event, context)
    assert response['statusCode'] == 400
    assert json.loads(response['body']) == 'userid is required in the event'== 'userid is required in the event'== 'userid is required in the event'

def test_lambda_handler_no_policies(dynamodb_setup):def test_lambda_handler_no_policies(dynamodb_setup):def test_lambda_handler_no_policies(dynamodb_setup):
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)ambda_handler(event, context)ambda_handler(event, context)
    assert response['statusCode'] == 404
    assert json.loads(response['body']) == 'No policies found for the given userid'

@patch('source.lambda_handler.create_iam_role_if_not_exists', return_value=None)
def test_lambda_handler_error_creating_role(mock_create_role, dynamodb_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error creating or checking IAM role'

@patch('source.lambda_handler.generate_sts_token', return_value=None)
def test_lambda_handler_error_generating_sts(mock_generate_sts, dynamodb_setup, iam_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error generating STS credentials'

def test_lambda_handler_success(dynamodb_setup, iam_setup, sts_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'AccessKeyId' in body
    assert 'SecretAccessKey' in body
    assert 'SessionToken' in body
    assert 'Expiration' in body

@patch('source.lambda_handler.attach_iam_policies', side_effect=Exception('Error attaching IAM policy'))
def test_lambda_handler_error_attaching_policies(mock_attach_policies, dynamodb_setup, iam_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error attaching IAM policy arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'== 'No policies found for the given userid'== 'No policies found for the given userid'

@patch('source.lambda_handler.create_iam_role_if_not_exists', return_value=None)
def test_lambda_handler_error_creating_role(mock_create_role, dynamodb_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error creating or checking IAM role'

@patch('source.lambda_handler.generate_sts_token', return_value=None)
def test_lambda_handler_error_generating_sts(mock_generate_sts, dynamodb_setup, iam_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error generating STS credentials'

def test_lambda_handler_success(dynamodb_setup, iam_setup, sts_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'AccessKeyId' in body
    assert 'SecretAccessKey' in body
    assert 'SessionToken' in body
    assert 'Expiration' in body

@patch('source.lambda_handler.attach_iam_policies', side_effect=Exception('Error attaching policy'))
def test_lambda_handler_error_attaching_policies(mock_attach_policies, dynamodb_setup, iam_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error attaching IAM policy arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
@patch('source.lambda_handler.create_iam_role_if_not_exists', return_value=None)
def test_lambda_handler_error_creating_role(mock_create_role, dynamodb_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error creating or checking IAM role'

@patch('source.lambda_handler.generate_sts_token', return_value=None)
def test_lambda_handler_error_generating_sts(mock_generate_sts, dynamodb_setup, iam_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error generating STS credentials'

@patch('source.lambda_handler.attach_iam_policies', side_effect=Exception('Error attaching IAM policy'))
def test_lambda_handler_error_attaching_policies(mock_attach_policies, dynamodb_setup, iam_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error attaching IAM policy arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'

def test_lambda_handler_success(dynamodb_setup, iam_setup, sts_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'AccessKeyId' in body
    assert 'SecretAccessKey' in body
    assert 'SessionToken' in body
    assert 'Expiration' in body
@patch('source.lambda_handler.create_iam_role_if_not_exists', return_value=None)
def test_lambda_handler_error_creating_role(mock_create_role, dynamodb_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error creating or checking IAM role'

@patch('source.lambda_handler.generate_sts_token', return_value=None)
def test_lambda_handler_error_generating_sts(mock_generate_sts, dynamodb_setup, iam_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error generating STS credentials'

def test_lambda_handler_success(dynamodb_setup, iam_setup, sts_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'AccessKeyId' in body
    assert 'SecretAccessKey' in body
    assert 'SessionToken' in body
    assert 'Expiration' in body

@patch('source.lambda_handler.attach_iam_policies', side_effect=Exception('Error attaching policy'))
def test_lambda_handler_error_attaching_policy(mock_attach_policies, dynamodb_setup, iam_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error attaching IAM policy arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
@patch('source.lambda_handler.create_iam_role_if_not_exists', return_value=None)
def test_lambda_handler_error_creating_role(mock_create_role, dynamodb_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error creating or checking IAM role'

@patch('source.lambda_handler.generate_sts_token', return_value=None)
def test_lambda_handler_error_generating_sts(mock_generate_sts, dynamodb_setup, iam_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error generating STS credentials'

def test_lambda_handler_success(dynamodb_setup, iam_setup, sts_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'AccessKeyId' in body
    assert 'SecretAccessKey' in body
    assert 'SessionToken' in body
    assert 'Expiration' in body

@patch('source.lambda_handler.attach_iam_policies', side_effect=Exception('Error attaching policy'))
def test_lambda_handler_error_attaching_policies(mock_attach_policies, dynamodb_setup, iam_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error attaching IAM policy arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
@patch('source.lambda_handler.create_iam_role_if_not_exists', return_value=None)
def test_lambda_handler_error_creating_role(mock_create_role, dynamodb_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error creating or checking IAM role'

@patch('source.lambda_handler.generate_sts_token', return_value=None)
def test_lambda_handler_error_generating_sts(mock_generate_sts, dynamodb_setup, iam_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error generating STS credentials'

@patch('source.lambda_handler.attach_iam_policies', side_effect=Exception('Error attaching IAM policy'))
def test_lambda_handler_error_attaching_policies(mock_attach_policies, dynamodb_setup, iam_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error attaching IAM policy arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'

def test_lambda_handler_success(dynamodb_setup, iam_setup, sts_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'AccessKeyId' in body
    assert 'SecretAccessKey' in body
    assert 'SessionToken' in body
    assert 'Expiration' in body

@patch('source.lambda_handler.create_iam_role_if_not_exists', return_value=None)
def test_lambda_handler_error_creating_role(mock_create_role, dynamodb_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error creating or checking IAM role'

@patch('source.lambda_handler.generate_sts_token', return_value=None)
def test_lambda_handler_error_generating_sts(mock_generate_sts, dynamodb_setup, iam_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error generating STS credentials'

def test_lambda_handler_success(dynamodb_setup, iam_setup, sts_setup):
    dynamodb_setup.put_item(Item={'userid': 'test-user', 'policies': ['arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']})
    event = {'userid': 'test-user'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'AccessKeyId' in body
    assert 'SecretAccessKey' in body
    assert 'SessionToken' in body
    assert 'Expiration' in body