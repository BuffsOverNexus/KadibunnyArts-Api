from enum import Enum

from database import Session

from models import Option

class OptionType(Enum):
    NONE = -1
    TOGGLE = 0
    TEXT = 1
    TEXTAREA = 2

class OptionKey(Enum):
    COMMISSION_STATUS = "COMMISSION_STATUS"
    COMMISSION_DISABLED_MESSAGE = "COMMISSION_DISABLED_MESSAGE"
    COMMISSION_REQUIRE_ACCOUNT = "COMMISSION_REQUIRE_ACCOUNT"
    ACCOUNT_EDIT_EMAIL = "ACCOUNT_EDIT_EMAIL"


def load_default_options():
    session = Session()
    commission_available = option_commission_available()
    disabled_message = option_commission_disabled_message()
    require_account = option_commission_require_account()
    account_edit_email = option_account_edit_email()

    # Determine if the options exist.
    commission_available_exists = session.query(Option).filter_by(key=OptionKey.COMMISSION_STATUS.value).first() is not None
    disabled_message_exists = session.query(Option).filter_by(key=OptionKey.COMMISSION_DISABLED_MESSAGE.value).first() is not None
    require_account_exists = session.query(Option).filter_by(key=OptionKey.COMMISSION_REQUIRE_ACCOUNT.value).first() is not None
    account_edit_email_exists = session.query(Option).filter_by(key=OptionKey.ACCOUNT_EDIT_EMAIL.value).first() is not None

    if not commission_available_exists:
        session.add(commission_available)
    if not disabled_message_exists:
        session.add(disabled_message)
    if not require_account_exists:
        session.add(require_account)
    if not account_edit_email_exists:
        session.add(account_edit_email)

    session.commit()
    session.close()


def option_commission_available():
    option = Option()
    option.key = OptionKey.COMMISSION_STATUS.value
    option.value = "false"
    option.type = OptionType.TOGGLE.value
    option.title = "Commission Form Availability"
    option.description = "Allow new commission requests?"
    return option

def option_commission_disabled_message():
    option = Option()
    option.key = OptionKey.COMMISSION_DISABLED_MESSAGE.value
    option.value = "New commission requests are currently unavailable. Please try again later."
    option.type = OptionType.TEXTAREA.value
    option.title = "Commissions Unavailable Message"
    option.description = "Please enter in what the user will see when visiting the Commissions form when it is not available:"
    return option

def option_commission_require_account():
    option = Option()
    option.key = OptionKey.COMMISSION_REQUIRE_ACCOUNT.value
    option.value = "false"
    option.type = OptionType.TOGGLE.value
    option.title = "Require Account For Commissions"
    option.description = "Are users required to login or create an account to request a commission?"
    return option

def option_account_edit_email():
    option = Option()
    option.key = OptionKey.ACCOUNT_EDIT_EMAIL.value
    option.value = "true"
    option.type = OptionType.TOGGLE.value
    option.title = "Allow Users To Change Their Email"
    option.description = "Are users allowed to edit their email within the account page?"
    return option
