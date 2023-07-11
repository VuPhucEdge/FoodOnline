from django.core.exceptions import ValidationError
import os


# only image validator
def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".png", "jpg", ".jpeg"]

    # compare
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            "Unsupported file extension. Alowed extensions: " + str(valid_extensions)
        )
