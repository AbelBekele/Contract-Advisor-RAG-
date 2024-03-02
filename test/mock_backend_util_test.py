import unittest
from unittest.mock import patch, MagicMock

class TestContractAdvisor(unittest.TestCase):
    @patch('main.ContractAdvisor', autospec=True)
    def test_answer_question(self, mock_contract_advisor):
        # Arrange
        mock_contract_advisor.answer_question.return_value = "This is a test answer"
        advisor = mock_contract_advisor("file_path", "milvus_host", "milvus_port")
        
        # Act
        result = advisor.answer_question("What is contract law?")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")
        mock_contract_advisor.answer_question.assert_called_once_with("What is contract law?")

if __name__ == '__main__':
    unittest.main()