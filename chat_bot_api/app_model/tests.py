import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser


class LLMEndpointConfidenceTest(APITestCase):
    ''''''

    def setUp(self):
        ''''''

        self.user = CustomUser.objects.create_user(
            email = 'test@example.com',
            password = 'strongPassword123-',
            first_name = 'Test',
            last_name = 'User'
        )

        response = self.client.post(reverse('app_auth:token_obtain_pair'), {
            'email': 'test@example.com',
            'password': 'strongPassword123-'
        })
        
        self.token = response.data['access']
        self.auth_headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.token}'
        }

    def test_prompts_with_varied_confidence_levels(self):
        ''''''

        test_cases = [
            {
                "prompt": "How do I iterate over rows in a Pandas DataFrame?", 
                "expected_confidence": "High"
            },
            {
                "prompt": "What is the difference between a list and a tuple in Python?", 
                "expected_confidence": "High"
            },
            {
                "prompt": "I got the error 'TypeError: 'NoneType' object is not iterable'. What does this mean?", 
                "expected_confidence": "High"
            },
            {
                "prompt": "How do I read from and write to a JSON file in Python?", 
                "expected_confidence": "High"
            },
            {
                "prompt": "What is the correct syntax for a list comprehension in Python?", 
                "expected_confidence": "High"
            },
            ####
            {
                "prompt": "What is the philosophy behind 'pythonic' code?", 
                "expected_confidence": "Medium"
            },
            {
                "prompt": "How should I structure a large Python project? What are the best practices?", 
                "expected_confidence": "Medium"
            },
            {
                "prompt": "When should I use object-oriented programming versus functional programming in my scripts?", 
                "expected_confidence": "Medium"
            },
            {
                "prompt": "How should a beginner start thinking about asynchronous programming in Python?", 
                "expected_confidence": "Medium"
            },
            {
                "prompt": "Is Python a good language for game development?", 
                "expected_confidence": "Medium"
            },
            ####
            {
                "prompt": "What is the best recipe for chocolate cake?", 
                "expected_confidence": "Low"
            },
            {
                "prompt": "Who was the first person to walk on the moon?", 
                "expected_confidence": "Low"
            },
            {   # TODO: problema
                "prompt": "How do I declare a constant in JavaScript?", 
                "expected_confidence": "Low"
            },
            {
                "prompt": "What is your favorite movie?", 
                "expected_confidence": "Low"
            },
            {
                "prompt": "asdfglkjh çpoiu zxcvb", 
                "expected_confidence": "Low"
            },
            {
                "prompt": "What is the meaning of life?", 
                "expected_confidence": "Low"
            }
        ]

        for case in test_cases:
            prompt = case["prompt"]
            expected_confidence = case["expected_confidence"]

            with self.subTest(prompt = prompt):
                url = reverse('app_model:search-information')
                payload = {"prompt": prompt}
                
                response = self.client.post(url, payload, format = 'json', **self.auth_headers)

                self.assertEqual(response.status_code, status.HTTP_200_OK, f"API falhou para o prompt: '{prompt}'")
                
                json_string_from_response = response.json()
                
                response_data = json.loads(json_string_from_response)
                
                self.assertIsInstance(response_data, list)
                self.assertEqual(len(response_data), 1)

                result_object = response_data[0]
                
                self.assertEqual(result_object['confidence'], expected_confidence)