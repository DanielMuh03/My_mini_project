from django.core.mail import send_mail


def send_activation_code(email, activation_code):
    activation_url = f"http://localhost:8000/v1/api/account/activate/{activation_code}"
    massage = f"""Thank you for singing up.
                Please, activate your account.
                Activation link: {activation_url}
                """
    send_mail(
        'Activate your account',
        massage,
        'test@test.com',
        [email, ],
        fail_silently=False
    )
