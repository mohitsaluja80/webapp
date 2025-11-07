import unittest
from unittest.mock import Mock, call
from techblog.views import tagdata

class TagDataTestCase(unittest.TestCase):
    def setUp(self):
        # Create mock objects for TaggedItem and Tag models
        self.tagged_items = [
            Mock(tag=Mock(name='Terraform')),
            Mock(tag=Mock(name='IaC')),
            Mock(tag=Mock(name='CICD')),
            Mock(tag=Mock(name='CICD')),
            Mock(tag=Mock(name='Jenkins')),
            Mock(tag=Mock(name='SRE')),

        ]
        
    def test_tagdata(self):
        # Mock the TaggedItem.objects.all() method
        TaggedItem = Mock()
        TaggedItem.objects.all.return_value = self.tagged_items
        
        expected_result = {
            'Terraform': 1,
            'IaC': 1,
            'CICD': 2,
            'SRE':2,
            'Jenkins': 1,
            'SRE': 1,
        }
        
        # Call the tagdata() function
        result = tagdata()
        
        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)
        
        # Assert that TaggedItem.objects.all() was called
        # TaggedItem.objects.all.assert_called_once()

        print(TaggedItem.mock_calls)


if __name__ == '__main__':
    unittest.main()
