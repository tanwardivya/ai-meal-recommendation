import unittest
from recipe_assistant.token_service import issue_token

class TestIssueToken(unittest.TestCase):
    
    def test_issue_token(self):
        user_id = "jane_doe"
        email = "janedoe@email.com"
        token = issue_token(user_id=user_id, email=email)
        print(token)
        self.assertIsNotNone(token) 