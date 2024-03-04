from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class LoginTestCase(APITestCase):

    def setUp(self):
        # Set up data for the whole TestCase
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.user.save()

    def test_double_login(self):
        # Perform the first login
        login_url = reverse('login_employee')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue('token' in response.data)

        # Attempt to log in again with the same credentials
        second_response = self.client.post(login_url, data, format='json')

        # Check the response to ensure it's behaving as expected, which in this case is another 200 OK status
        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        self.assertEqual(second_response.data['status'], 'success')
        self.assertTrue('token' in second_response.data)
        
    def test_logout(self):
        # Log the user in
        login_url = reverse('login_employee')
        login_data = {'username': 'testuser', 'password': 'testpassword123'}
        login_response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in login_response.data)

        # Logout the user
        logout_url = reverse('logout_employee')
        # Using the token from login response for authorization in the logout request
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        logout_response = self.client.post(logout_url, format='json')

        # Verify the logout was successful
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertEqual(logout_response.data['status'], 'success')

        # Verify the token has been removed
        self.assertFalse(Token.objects.filter(user=self.user).exists())

        # Attempt to use the token after logout should fail
        post_logout_response = self.client.get(login_url, format='json')
        self.assertNotEqual(post_logout_response.status_code, status.HTTP_200_OK)
