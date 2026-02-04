from sqladmin import Admin
from models.user.view import UserView
from models.user_logs.view import UserLogsView


def register_models(admin: Admin):
    admin.add_view(UserView)
    admin.add_view(UserLogsView)