from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_login_cancelled_redirect_url(self, request):
        print("✅ Custom adapter method called!")  # 👈 Check terminal
        return '/signin'