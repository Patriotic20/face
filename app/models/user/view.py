from sqladmin import ModelView
from .model import User



class UserView(ModelView, model=User):
    
    column_list = [
        User.id,
        User.first_name,
        User.last_name,
        User.middle_name,
        User.image_path,
        User.passport_serial,
    ]
    
    column_searchable_list = [User.last_name, User.passport_serial]
    
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    
    # Allows viewing logs directly from user page
    # column_details_exclude_list = [User.image_path]

    # column_exclude_list = ["logs"]
