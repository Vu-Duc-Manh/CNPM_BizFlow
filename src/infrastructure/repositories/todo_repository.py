from typing import List, Optional
from sqlalchemy.orm import Session

from domain.models.itodo_repository import ITodoRepository
from domain.models.todo import Todo
from infrastructure.models.todo_model import TodoModel
from infrastructure.databases import SessionLocal


class TodoRepository(ITodoRepository):

    def __init__(self):
        self.db: Session = SessionLocal()

    # ========== BẮT BUỘC ==========
    def list(self) -> List[Todo]:
        todos = self.db.query(TodoModel).all()
        return [Todo(id=t.id, title=t.title) for t in todos]

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        todo = self.db.query(TodoModel).filter(TodoModel.id == todo_id).first()
        if todo:
            return Todo(id=todo.id, title=todo.title)
        return None

    def add(self, todo: Todo) -> Todo:
        todo_model = TodoModel(title=todo.title)
        self.db.add(todo_model)
        self.db.commit()
        self.db.refresh(todo_model)
        return Todo(id=todo_model.id, title=todo_model.title)

    def update(self, todo: Todo) -> Optional[Todo]:
        db_todo = self.db.query(TodoModel).filter(TodoModel.id == todo.id).first()
        if not db_todo:
            return None
        db_todo.title = todo.title
        self.db.commit()
        return Todo(id=db_todo.id, title=db_todo.title)

    def delete(self, todo_id: int) -> bool:
        todo = self.db.query(TodoModel).filter(TodoModel.id == todo_id).first()
        if not todo:
            return False
        self.db.delete(todo)
        self.db.commit()
        return True
