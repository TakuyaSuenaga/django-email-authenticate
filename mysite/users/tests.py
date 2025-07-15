# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.messages import get_messages

from .models import User, UserManager
from .forms import SigninForm, SignupForm, ChangePasswordForm, ResetPasswordForm, PasswordSetForm, ProfileForm

User = get_user_model()


class UserModelTestCase(TestCase):
    """ユーザーモデルのテスト"""
    
    def test_user_creation(self):
        """通常のユーザー作成テスト"""
        user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpassword123'
        )
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.name, 'Test User')
        self.assertTrue(user.check_password('testpassword123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        
    def test_superuser_creation(self):
        """スーパーユーザー作成テスト"""
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            name='Admin User',
            password='adminpassword123'
        )
        
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertEqual(admin_user.name, 'Admin User')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_admin)
        self.assertTrue(admin_user.is_staff)
        
    def test_user_creation_without_email(self):
        """メールアドレスなしでのユーザー作成テスト（エラーケース）"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                name='Test User',
                password='testpassword123'
            )
            
    def test_user_string_representation(self):
        """ユーザーの文字列表現テスト"""
        user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpassword123'
        )
        
        self.assertEqual(str(user), 'test@example.com')
        
    def test_email_normalization(self):
        """メールアドレスの正規化テスト"""
        user = User.objects.create_user(
            email='Test@EXAMPLE.COM',
            name='Test User',
            password='testpassword123'
        )
        
        self.assertEqual(user.email, 'Test@example.com')
        
    def test_user_permissions(self):
        """ユーザー権限のテスト"""
        user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpassword123'
        )
        
        # 通常ユーザーでも全権限を持つ（現在の実装）
        self.assertTrue(user.has_perm('any_permission'))
        self.assertTrue(user.has_module_perms('any_app'))
        
    def test_get_absolute_url(self):
        """get_absolute_urlメソッドのテスト"""
        user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpassword123'
        )
        
        expected_url = reverse('users:profile', kwargs={'pk': user.pk})
        self.assertEqual(user.get_absolute_url(), expected_url)


class SigninViewTestCase(TestCase):
    """サインインビューのテスト"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpassword123'
        )
        
    def test_signin_view_get(self):
        """サインインページの表示テスト"""
        response = self.client.get(reverse('users:signin'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertIsInstance(response.context['form'], SigninForm)
        
    def test_valid_signin(self):
        """有効なサインインテスト"""
        response = self.client.post(reverse('users:signin'), {
            'username': 'test@example.com',
            'password': 'testpassword123'
        })
        
        self.assertEqual(response.status_code, 302)  # リダイレクト
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)
        
    def test_invalid_signin(self):
        """無効なサインインテスト"""
        response = self.client.post(reverse('users:signin'), {
            'username': 'test@example.com',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')
        
    def test_authenticated_user_redirect(self):
        """認証済みユーザーのリダイレクトテスト"""
        self.client.login(username='test@example.com', password='testpassword123')
        response = self.client.get(reverse('users:signin'))
        
        self.assertEqual(response.status_code, 302)  # リダイレクト


class SignupViewTestCase(TestCase):
    """サインアップビューのテスト"""
    
    def setUp(self):
        self.client = Client()
        self.valid_data = {
            'email': 'newuser@example.com',
            'name': 'New User',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        
    def test_signup_view_get(self):
        """サインアップページの表示テスト"""
        response = self.client.get(reverse('users:signup'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertIsInstance(response.context['form'], SignupForm)
        
    def test_valid_signup(self):
        """有効なサインアップテスト"""
        response = self.client.post(reverse('users:signup'), self.valid_data)
        
        # ユーザーが作成されたかチェック
        self.assertTrue(User.objects.filter(email=self.valid_data['email']).exists())
        
        # リダイレクトをチェック
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:welcome'))
        
        # 自動ログインされているかチェック
        user = User.objects.get(email=self.valid_data['email'])
        self.assertEqual(int(self.client.session['_auth_user_id']), user.id)
        
    def test_invalid_signup_password_mismatch(self):
        """パスワード不一致のサインアップテスト"""
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'differentpassword'
        
        response = self.client.post(reverse('users:signup'), invalid_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email=self.valid_data['email']).exists())
        
    def test_duplicate_email_signup(self):
        """重複メールアドレスでのサインアップテスト"""
        # 既存ユーザーを作成
        User.objects.create_user(
            email=self.valid_data['email'],
            name='Existing User',
            password='existingpassword123'
        )
        
        response = self.client.post(reverse('users:signup'), self.valid_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')
        
    def test_authenticated_user_cannot_signup(self):
        """認証済みユーザーはサインアップできないテスト"""
        # ユーザーを作成してログイン
        user = User.objects.create_user(
            email='existing@example.com',
            name='Existing User',
            password='existingpassword123'
        )
        self.client.login(username='existing@example.com', password='existingpassword123')
        
        response = self.client.get(reverse('users:signup'))
        
        # LogoutRequiredMixinによりリダイレクトされる
        self.assertEqual(response.status_code, 302)


class SignoutViewTestCase(TestCase):
    """サインアウトビューのテスト"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpassword123'
        )
        
    def test_signout(self):
        """サインアウトテスト"""
        # ログイン
        self.client.login(username='test@example.com', password='testpassword123')
        
        # ログアウト
        response = self.client.post(reverse('users:signout'))
        
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)


class WelcomeViewTestCase(TestCase):
    """ウェルカムビューのテスト"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpassword123'
        )
        
    def test_welcome_view_authenticated(self):
        """認証済みユーザーのウェルカムページテスト"""
        self.client.login(username='test@example.com', password='testpassword123')
        response = self.client.get(reverse('users:welcome'))
        
        self.assertEqual(response.status_code, 200)
        
    def test_welcome_view_unauthenticated(self):
        """未認証ユーザーのウェルカムページテスト"""
        response = self.client.get(reverse('users:welcome'))
        
        self.assertEqual(response.status_code, 302)  # ログインページにリダイレクト


class ChangePasswordViewTestCase(TestCase):
    """パスワード変更ビューのテスト"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='oldpassword123'
        )
        self.client.login(username='test@example.com', password='oldpassword123')
        
    def test_change_password_view_get(self):
        """パスワード変更ページの表示テスト"""
        response = self.client.get(reverse('users:change_password'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChangePasswordForm)
        
    def test_valid_password_change(self):
        """有効なパスワード変更テスト"""
        response = self.client.post(reverse('users:change_password'), {
            'old_password': 'oldpassword123',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:change_password_done'))
        
        # パスワードが変更されたかチェック
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))
        
    def test_invalid_old_password(self):
        """無効な古いパスワードテスト"""
        response = self.client.post(reverse('users:change_password'), {
            'old_password': 'wrongpassword',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')
        
    def test_unauthenticated_change_password(self):
        """未認証ユーザーのパスワード変更テスト"""
        self.client.logout()
        response = self.client.get(reverse('users:change_password'))
        
        self.assertEqual(response.status_code, 302)  # ログインページにリダイレクト


class PasswordResetViewTestCase(TestCase):
    """パスワードリセットビューのテスト"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpassword123'
        )
        
    def test_password_reset_view_get(self):
        """パスワードリセットページの表示テスト"""
        response = self.client.get(reverse('users:password_reset'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ResetPasswordForm)
        
    def test_valid_password_reset_request(self):
        """有効なパスワードリセット要求テスト"""
        response = self.client.post(reverse('users:password_reset'), {
            'email': 'test@example.com'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:password_reset_done'))
        
        # メールが送信されたかチェック
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['test@example.com'])
        
    def test_invalid_email_reset_request(self):
        """無効なメールアドレスでのリセット要求テスト"""
        response = self.client.post(reverse('users:password_reset'), {
            'email': 'nonexistent@example.com'
        })
        
        # Djangoはセキュリティ上、存在しないメールアドレスでも成功レスポンスを返す
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)
        
    def test_password_reset_confirm_valid(self):
        """有効なパスワードリセット確認テスト"""
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        
        response = self.client.post(reverse('users:password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        }), {
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:password_reset_complete'))
        
        # パスワードが変更されたかチェック
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))
        
    def test_password_reset_confirm_invalid_token(self):
        """無効なトークンでのパスワードリセット確認テスト"""
        response = self.client.post(reverse('users:password_reset_confirm', kwargs={
            'uidb64': 'invalid',
            'token': 'invalid'
        }), {
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'invalid')


class ProfileViewTestCase(TestCase):
    """プロフィールビューのテスト"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpassword123'
        )
        self.client.login(username='test@example.com', password='testpassword123')
        
    def test_profile_view_get(self):
        """プロフィールページの表示テスト"""
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.user.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ProfileForm)
        
    def test_profile_update(self):
        """プロフィール更新テスト"""
        response = self.client.post(reverse('users:profile', kwargs={'pk': self.user.pk}), {
            'email': 'updated@example.com',
            'name': 'Updated User'
        })
        
        self.assertEqual(response.status_code, 302)
        
        # ユーザー情報が更新されたかチェック
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.name, 'Updated User')
        
        # 成功メッセージが表示されるかチェック
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('successfully saved' in str(message) for message in messages))
        
    def test_profile_view_unauthenticated(self):
        """未認証ユーザーのプロフィールページテスト"""
        self.client.logout()
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.user.pk}))
        
        self.assertEqual(response.status_code, 302)  # ログインページにリダイレクト
        
    def test_profile_view_wrong_user(self):
        """他のユーザーのプロフィールページテスト"""
        other_user = User.objects.create_user(
            email='other@example.com',
            name='Other User',
            password='otherpassword123'
        )
        
        # VerifyUserIdentityMixinにより、他のユーザーのプロフィールはアクセス不可
        response = self.client.get(reverse('users:profile', kwargs={'pk': other_user.pk}))
        
        # VerifyUserIdentityMixinの実装により結果が決まる
        # 通常は403や404が返される
        self.assertIn(response.status_code, [403, 404])


class FormTestCase(TestCase):
    """フォームのテスト"""
    
    def test_signin_form_valid(self):
        """有効なサインインフォームテスト"""
        user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpassword123'
        )
        
        form = SigninForm(data={
            'username': 'test@example.com',
            'password': 'testpassword123'
        })
        
        self.assertTrue(form.is_valid())
        
    def test_signup_form_valid(self):
        """有効なサインアップフォームテスト"""
        form = SignupForm(data={
            'email': 'test@example.com',
            'name': 'Test User',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        
        self.assertTrue(form.is_valid())
        
    def test_profile_form_valid(self):
        """有効なプロフィールフォームテスト"""
        form = ProfileForm(data={
            'email': 'test@example.com',
            'name': 'Test User'
        })
        
        self.assertTrue(form.is_valid())


class URLTestCase(TestCase):
    """URL設定のテスト"""
    
    def test_url_patterns(self):
        """URL パターンのテスト"""
        # 各URLが正しく解決されるかテスト
        self.assertEqual(reverse('users:signin'), '/users/signin/')
        self.assertEqual(reverse('users:signout'), '/users/signout/')
        self.assertEqual(reverse('users:signup'), '/users/signup/')
        self.assertEqual(reverse('users:welcome'), '/users/welcome/')
        self.assertEqual(reverse('users:change_password'), '/users/change_password/')
        self.assertEqual(reverse('users:password_reset'), '/users/password_reset/')
        
        # パラメータありのURL
        self.assertEqual(
            reverse('users:profile', kwargs={'pk': 1}),
            '/users/profile/1'
        )
        
        self.assertEqual(
            reverse('users:password_reset_confirm', kwargs={'uidb64': 'test', 'token': 'test'}),
            '/users/password_reset_confirm/test/test/'
        )


# テストの実行方法：
# python manage.py test users
# または特定のテストクラスのみ：
# python manage.py test users.tests.UserModelTestCase

# カバレッジレポートの取得（coverage.pyが必要）：
# coverage run --source='.' manage.py test users
# coverage report
# coverage html
