import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))
        if not re.findall("[a-z]", password):
            raise ValidationError(_("Password must contain at least one lowercase letter."))
        if not re.findall("[A-Z]", password):
            raise ValidationError(_("Password must contain at least one uppercase letter."))
        if not re.findall("[0-9]", password):
            raise ValidationError(_("Password must contain at least one number."))
        if not re.findall("[!@#$%^&*()]", password):
            raise ValidationError(_("Password must contain at least one special character."))

    def get_help_text(self):
        return _("Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one number, and one special character.")