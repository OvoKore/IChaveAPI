from app.route.default import bp_default
from app.route.refresh_token import bp_refresh_token
from app.route.user import bp_user
from app.route.login import bp_login
from app.route.locksmith import bp_locksmith
from app.route.login_locksmith import bp_login_locksmith
from app.route.serivce import bp_service
from app.route.address_locksmith import bp_address_locksmith
from app.route.address_user import bp_address_user
from app.route.locksmith_list import bp_locksmith_list
from app.route.whatsapp import bp_whatsapp

blueprints = [
    bp_default,
    bp_refresh_token,
    bp_user,
    bp_login,
    bp_locksmith,
    bp_login_locksmith,
    bp_service,
    bp_address_locksmith,
    bp_address_user,
    bp_locksmith_list,
    bp_whatsapp
]
