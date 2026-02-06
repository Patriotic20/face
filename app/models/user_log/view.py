from sqladmin import ModelView
from .model import UserLogs


class UserLogsView(ModelView, model=UserLogs):
    column_list = [
        UserLogs.id, 
        UserLogs.user, 
        UserLogs.enter_time, 
        UserLogs.exit_time
    ]
    # Filter logs by specific user or dates
    # column_filters = [UserLogs.user_id, UserLogs.enter_time]
    
    name = "Access Log"
    name_plural = "Access Logs"
    icon = "fa-solid fa-clipboard-list"