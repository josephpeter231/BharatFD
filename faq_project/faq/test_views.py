from django.urls import reverse
from rest_framework.test import APITestCase
from .models import FAQ

class FAQListViewTests(APITestCase):
    def setUp(self):
        self.faq1 = FAQ.objects.create(
            question_en="What is Python?",
            answer="<p>Python is a programming language.</p>"
        )
        self.faq2 = FAQ.objects.create(
            question_en="What is Django?",
            answer="<p>Django is a web framework.</p>"
        )
        self.url = reverse('faq-list') 

    def test_empty_faq_list(self):
        """
        Test that an empty list is returned when no FAQs exist.
        """
        FAQ.objects.all().delete() 
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_single_faq_retrieval(self):
        """
        Test that a single FAQ is retrieved correctly.
        """
        FAQ.objects.all().delete()  
        faq = FAQ.objects.create(
            question_en="Single FAQ",
            answer="<p>Single Answer</p>"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question'], faq.question_en)

    def test_multiple_faqs_retrieval(self):
        """
        Test that multiple FAQs are retrieved correctly.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_faq_list_ordering(self):
        """
        Test that FAQs are ordered by creation time (oldest first).
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], self.faq1.question_en)
        self.assertEqual(response.data[1]['question'], self.faq2.question_en)

    def test_translation_functionality(self):
        """
        Test that the translation functionality works for a specific language.
        """
        # Test Hindi translation
        response = self.client.get(self.url, {'lang': 'hi'})
        self.assertEqual(response.status_code, 200)
        
        # Check if the translated text contains expected keywords
        self.assertIn("क्या है", response.data[0]['question']) 
        self.assertIn("क्या है", response.data[1]['question'])  

    def test_fallback_to_english(self):
        """
        Test that the API falls back to English if translation fails.
        """
        # Test with an invalid language code
        response = self.client.get(self.url, {'lang': 'xyz'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], self.faq1.question_en)
        self.assertEqual(response.data[1]['question'], self.faq2.question_en)

    def test_html_stripping_in_answers(self):
        """
        Test that HTML tags are stripped from the answer field.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['answer'], "Python is a programming language.")
        self.assertEqual(response.data[1]['answer'], "Django is a web framework.")