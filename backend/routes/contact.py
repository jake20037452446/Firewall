from flask import Blueprint, request, jsonify
from utils.validators import (
    validate_name,
    validate_email,
    validate_phone,
    validate_message
)

# ================================
# CONTACT ROUTES
# ================================
contact_bp = Blueprint("contact", __name__)


# ================================
# SUBMIT CONTACT FORM
# ================================
@contact_bp.route("/contact", methods=["POST"])
def submit_contact():
    """
    Handles consultation form submissions
    """

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    company = data.get("company")
    service = data.get("service")
    message = data.get("message")

    # ================================
    # VALIDATION
    # ================================
    if not validate_name(name):
        return jsonify({"success": False, "error": "Invalid name"}), 400

    if not validate_email(email):
        return jsonify({"success": False, "error": "Invalid email"}), 400

    if not validate_phone(phone):
        return jsonify({"success": False, "error": "Invalid phone"}), 400

    if not validate_message(message):
        return jsonify({"success": False, "error": "Message too short"}), 400

    # ================================
    # SIMULATED SAVE (NO DATABASE YET)
    # ================================
    contact_entry = {
        "name": name,
        "email": email,
        "phone": phone,
        "company": company,
        "service": service,
        "message": message
    }

    # (Later you would save this to database or email it)
    print("NEW CONTACT FORM:", contact_entry)

    return jsonify({
        "success": True,
        "message": "Contact form submitted successfully"
    }), 201