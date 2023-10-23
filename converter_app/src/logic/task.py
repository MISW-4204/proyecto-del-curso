from src.models.task import Task
from sqlalchemy.orm import Session


def get_user_tasks(db: Session, user_id: int, limit: int = 100, order: int = 0):
    if order == 0:
        return (
            db.query(Task)
            .filter(Task.id_user == user_id)
            .order_by(Task.id.asc())
            .limit(limit)
            .all()
        )
    elif order == 1:
        return (
            db.query(Task)
            .filter(Task.id_user == user_id)
            .order_by(Task.id.desc())
            .limit(limit)
            .all()
        )
    return db.query(Task).filter(Task.id_user == user_id).limit(limit).all()


def delete_task_by_id(db: Session, id):
    task = db.query(Task).filter_by(id=id).first()
    task.delete()
    db.commit()
    return task
