import re


# ================================
# BASIC STRING VALIDATION
# ================================

def is_empty(value: str) -> bool:
    """Check if a value is empty or only spaces."""
    return value is None or str(value).strip() == ""


def clean_string(value: str) -> str:
    """Trim whitespace safely."""
    if value is None:
        return ""
    return str(value).strip()


# ================================
# NAME VALIDATION
# ================================

def validate_name(name: str) -> bool:
    """
    Valid names:
    - Letters only
    - Spaces allowed
    - 2–50 characters
    """
    if is_empty(name):
        return False

    name = clean_string(name)

    pattern = r"^[A-Za-z\s]{2,50}$"
    return bool(re.match(pattern, name))


# ================================
# EMAIL VALIDATION
# ================================

def validate_email(email: str) -> bool:
    """
    Basic safe email validation.
    """
    if is_empty(email):
        return False

    email = clean_string(email)

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return bool(re.match(pattern, email))


# ================================
# PHONE VALIDATION (OPTIONAL FIELD)
# ================================

def validate_phone(phone: str) -> bool:
    """
    Accepts:
    - 10 digit US numbers
    - (xxx) xxx-xxxx
    - xxx-xxx-xxxx
    - optional field allowed (empty = valid)
    """
    if is_empty(phone):
        return True  # optional field

    phone = clean_string(phone)

    pattern = r"^(\+1\s?)?(\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}$"
    return bool(re.match(pattern, phone))


# ================================
# MESSAGE VALIDATION
# ================================

def validate_message(message: str) -> bool:
    """
    Prevent empty or extremely short messages.
    """
    if is_empty(message):
        return False

    message = clean_string(message)

    return 10 <= len(message) <= 2000


# ================================
# FORM VALIDATION (FULL CHECK)
# ================================

def validate_contact_form(data: dict) -> dict:
    """
    Used in Flask routes.
    Returns:
    {
        "valid": True/False,
        "errors": []
    }
    """

    errors = []

    name = clean_string(data.get("name"))
    email = clean_string(data.get("email"))
    phone = clean_string(data.get("phone"))
    message = clean_string(data.get("message"))

    if not validate_name(name):
        errors.append("Invalid name (letters only, 2–50 characters).")

    if not validate_email(email):
        errors.append("Invalid email address.")

    if not validate_phone(phone):
        errors.append("Invalid phone number format.")

    if not validate_message(message):
        errors.append("Message must be 10–2000 characters.")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


# ================================
# EXTRA SECURITY HELPERS
# ================================

def sanitize_text(text: str) -> str:
    """
    Basic protection against script injection.
    Removes dangerous tags.
    """
    if text is None:
        return ""

    text = str(text)

    dangerous = ["<script>", "</script>", "<", ">"]
    for d in dangerous:
        text = text.replace(d, "")

    return text.strip()