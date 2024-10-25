import pytest
from hackathon_sts_token import lambda_handler, get_policies_for_user, create_or_check_iam_role, generate_sts_credentials

# lambda_handler.py

def lambda_handler(event, context):
    userid = event.get('userid')
    if not userid:
        return {"statusCode": 400, "body": "Missing userid"}
    
    # Simulate fetching policies
    policies = get_policies_for_user(userid)
    if not policies:
        return {"statusCode": 404, "body": "No policies found"}
    
    # Simulate creating/checking IAM role
    try:
        role = create_or_check_iam_role(userid)
    except Exception as e:
        def test_missing_userid():
            event = {}
            context = {}
            response = lambda_handler(event, context)
            assert response['statusCode'] == 400
            assert response['body'] == "Missing userid"

        def test_no_policies_found(monkeypatch):
            def mock_get_policies_for_user(userid):
                return []
            monkeypatch.setattr('lambda_handler.get_policies_for_user', mock_get_policies_for_user)
            
            event = {'userid': 'testuser'}
            context = {}
            response = lambda_handler(event, context)
            assert response['statusCode'] == 404
            assert response['body'] == "No policies found"

        def test_iam_role_error(monkeypatch):
            def mock_create_or_check_iam_role(userid):
                raise Exception("IAM role error")
            monkeypatch.setattr('lambda_handler.create_or_check_iam_role', mock_create_or_check_iam_role)
            
            event = {'userid': 'testuser'}
            context = {}
            response = lambda_handler(event, context)
            assert response['statusCode'] == 500
            assert response['body'] == "IAM role error"

        def test_sts_credentials_error(monkeypatch):
            def mock_generate_sts_credentials(role):
                raise Exception("STS credentials error")
            monkeypatch.setattr('lambda_handler.generate_sts_credentials', mock_generate_sts_credentials)
            
            event = {'userid': 'testuser'}
            context = {}
            response = lambda_handler(event, context)
            assert response['statusCode'] == 500
            assert response['body'] == "STS credentials error"

        def test_successful_execution(monkeypatch):
            def mock_get_policies_for_user(userid):
                return ["policy1", "policy2"]
            def mock_create_or_check_iam_role(userid):
                return "role"
            def mock_generate_sts_credentials(role):
                return {"AccessKeyId": "key", "SecretAccessKey": "secret", "SessionToken": "token"}
            
            monkeypatch.setattr('lambda_handler.get_policies_for_user', mock_get_policies_for_user)
            monkeypatch.setattr('lambda_handler.create_or_check_iam_role', mock_create_or_check_iam_role)
            monkeypatch.setattr('lambda_handler.generate_sts_credentials', mock_generate_sts_credentials)
            
            event = {'userid': 'testuser'}
            context = {}
            response = lambda_handler(event, context)
            assert response['statusCode'] == 200
            assert response['body'] == {"AccessKeyId": "key", "SecretAccessKey": "secret", "SessionToken": "token"}