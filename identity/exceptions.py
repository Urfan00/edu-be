from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException
from rest_framework import status


class EmailNotVerifiedError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("Email is not verified. "
                       "Please check your inbox and verify your account.")
    default_code = "email_not_verified"

    def __init__(self, email=None, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = {"detail": str(detail)}
        if email is not None:
            self.detail["email"] = email
