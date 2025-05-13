from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


def run():
    email = input("Please provice your email: ")
    # Replace with your user’s email or username, depending on your user model
    user = get_user_model().objects.get(email=email)

    # Generate and retrieve the token
    token, created = Token.objects.get_or_create(user=user)
    if created:
        token.save()
    # Print the token key
    print(token.key)
