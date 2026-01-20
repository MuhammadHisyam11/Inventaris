from django.contrib.auth.tokens import PasswordResetTokenGenerator

class SimpleResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # token berubah kalau password berubah -> link lama otomatis invalid
        return f"{user.pk}{user.password}{timestamp}"

reset_token_generator = SimpleResetTokenGenerator()