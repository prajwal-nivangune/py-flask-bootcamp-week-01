import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
ENV_PATH = os.path.join(ROOT_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)


class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    # role should be here too

    FEATURE_FLAGS = {
        # Auth Routes
        "registration": os.getenv("FEATURE_REGISTRATION_ENABLED", "true").lower() == "true",
        "login": os.getenv("FEATURE_LOGIN_ENABLED", "true").lower() == "true",
        "logout": os.getenv("FEATURE_LOGOUT_ENABLED", "true").lower() == "true",
        # Admin routes
        "promote_user": os.getenv("FEATURE_PROMOTE_USER", "true").lower() == "true",
        "create_department": os.getenv("FEATURE_CREATE_DEPARTMENT", "true").lower() == "true",
        "list_departments": os.getenv("FEATURE_LIST_DEPARTMENTS", "true").lower() == "true",
        "onboard_doctor": os.getenv("FEATURE_ONBOARD_DOCTOR", "true").lower() == "true",
        "assign_doctor": os.getenv("FEATURE_ASSIGN_DOCTOR", "true").lower() == "true",
        "view_appointments": os.getenv("FEATURE_VIEW_APPOINTMENTS", "true").lower() == "true",
        # Doctor routes
        "create_availability": os.getenv("FEATURE_CREATE_AVAILABILITY", "true").lower() == "true",
        "get_availability": os.getenv("FEATURE_GET_AVAILABILITY", "true").lower() == "true",
        "update_availability": os.getenv("FEATURE_UPDATE_AVAILABILITY", "true").lower() == "true",
        # Member appointment routes
        "book_appointment": os.getenv("FEATURE_BOOK_APPOINTMENT", "true").lower() == "true",
        "update_appointment_status": os.getenv("FEATURE_UPDATE_APPOINTMENT_STATUS", "true").lower()
        == "true",
        # Reimbursement routes
        "submit_claim": os.getenv("FEATURE_SUBMIT_CLAIM", "true").lower() == "true",
        "review_claim": os.getenv("FEATURE_REVIEW_CLAIM", "true").lower() == "true",
        "view_all_claims": os.getenv("FEATURE_VIEW_ALL_CLAIMS", "true").lower() == "true",
    }
