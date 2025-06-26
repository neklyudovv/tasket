class Task:
    def __init__(self, id, user_id, title, due_date, is_done, created_at):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.due_date = due_date
        self.is_done = is_done
        self.created_at = created_at