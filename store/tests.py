from django.test import TestCase
from django.contrib.auth import get_user_model


class SignoutTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test-user',
            password='test-password'
        )
        self.client.force_login(self.user)

    def test_post_signout_logs_out_and_redirects_home(self):
        response = self.client.post('/signout/')

        self.assertRedirects(response, '/')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_get_signout_does_not_log_out(self):
        response = self.client.get('/signout/')

        self.assertRedirects(response, '/')
        self.assertIn('_auth_user_id', self.client.session)


class SignupTests(TestCase):

    def test_signup_creates_user_and_logs_them_in(self):
        response = self.client.post('/signup/', {
            'username': 'new-user',
            'password1': 'Plantae!NewUser2026',
            'password2': 'Plantae!NewUser2026',
        })

        self.assertRedirects(response, '/')
        user = get_user_model().objects.get(username='new-user')
        self.assertTrue(user.check_password('Plantae!NewUser2026'))
        self.assertEqual(
            str(self.client.session['_auth_user_id']),
            str(user.pk)
        )

    def test_signup_rejects_duplicate_username(self):
        get_user_model().objects.create_user(
            username='existing-user',
            password='Existing!Password2026'
        )

        response = self.client.post('/signup/', {
            'username': 'existing-user',
            'password1': 'Plantae!NewUser2026',
            'password2': 'Plantae!NewUser2026',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            get_user_model().objects.filter(username='existing-user').count(),
            1
        )
