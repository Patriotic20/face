from sqladmin import ModelView
from .model import Camera

class CameraView(ModelView, model=Camera):
    name = "Camera"
    name_plural = "Cameras"
    icon = "fa-solid fa-camera"

    column_list = [
        Camera.id,
        Camera.device_ip,
        Camera.username,
        Camera.camera_type,
    ]

    form_columns = [
        Camera.device_ip,
        Camera.username,
        Camera.password,
        Camera.camera_type,
    ]
