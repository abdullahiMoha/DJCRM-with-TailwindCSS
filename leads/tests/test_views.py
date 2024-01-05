""" 
TEST MODULE
"""
from django.test import TestCase
from django.shortcuts import reverse

# Create your tests here.
class LandingPageTest(TestCase):
    """ LandingPage test class"""
    def test_status_code(self):
        """TESTING STATUS OF CODE"""
        response=self.client.get(reverse("landing-page"))
        #print(response.content)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, "landing.html")
        self.assertTemplateUsed(response, "landing.html")