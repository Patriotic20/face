from sqladmin import Admin
from app.models.user.view import UserView
from app.models.camera.view import CameraView
# from app.models.user_log.view import UserLogsView

def register_models(admin: Admin):
    admin.add_view(UserView)
    admin.add_view(CameraView)
    # admin.add_view(UserLogsView)
