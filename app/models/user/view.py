import os
import shutil
from sqladmin import ModelView
from wtforms import FileField, Form
from markupsafe import Markup
from .model import User 

# 1. Define a plain WTForms class with your extra field
class UserUploadForm(Form):
    image_upload = FileField("Upload Image")

class UserView(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    column_list = [
        User.id,
        User.first_name,
        User.last_name,
        User.passport_serial,
        User.image_path,
    ]
    
    # 2. Tell SQLAdmin to use your custom form as a base
    form_base_class = UserUploadForm
    
    # 3. Only use form_columns (include all fields you want except image_path)
    form_columns = [
        "first_name", 
        "last_name", 
        "middle_name", 
        "passport_serial", 
        # image_upload comes from form_base_class automatically
        # image_path is excluded by not listing it here
    ]
    
    async def on_model_change(self, data, model, is_created, request):
        # Handle file upload
        if "image_upload" in data:
            file_obj = data["image_upload"]
            if file_obj and file_obj.filename:
                upload_dir = "static/uploads"
                os.makedirs(upload_dir, exist_ok=True)
                filename = f"{model.passport_serial}_{file_obj.filename}"
                file_path = os.path.join(upload_dir, filename)
                
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file_obj.file, buffer)
                
                model.image_path = f"/static/uploads/{filename}"
            
            # Remove it so SQLAlchemy doesn't see it
            del data["image_upload"]
    
    column_formatters = {
        "image_path": lambda m, a: Markup(f'<img src="{m.image_path}" width="50">') if m.image_path else ""
    }