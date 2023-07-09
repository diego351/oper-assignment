from django.core.mail import send_mail


class EmailService:
    @classmethod
    def send_invitation(cls, email, token, quiz_id):
        send_mail(
            "Quiz invitation",
            f"""Hello there! Here's a token your gonna need: {token}.
            And quiz id: {quiz_id}
            """,
            "service@opercredits.com",
            [email],
            fail_silently=False,
        )
