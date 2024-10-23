class User:
    def __init__(self, user_id):
        self.user_id = ''
        self.state = 'chat_start'
        self.t_user_id = user_id
        self.callback = self
        self.revit_choise = ''
        self.feedback_text = ''
        self.license_key = ''
        self.build_version = ''
        self.revit_version = ''
        self.choise = ""
        self.file_path = ''
        self.photo_path = ''
        self.renga_version = ''
        self.plugin_id = ''