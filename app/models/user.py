from datetime import datetime, timezone
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so

from ..extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.find_by_id(int(user_id))


class User(db.Model, UserMixin):
    id : so.Mapped[int] = so.mapped_column(primary_key=True)
    status : so.Mapped[str] = so.mapped_column(sa.String(50), default='user')
    name : so.Mapped[str] = so.mapped_column(sa.String(50))
    login : so.Mapped[str] = so.mapped_column(sa.String(50))
    password : so.Mapped[str] = so.mapped_column(sa.String(100))
    date : so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    posts = so.relationship("Post", back_populates="author")


    @classmethod
    def find_by_id(cls, id):
        return db.session.get(cls, id)


    @classmethod
    def find_by_login(cls, login):
        query = sa.select(cls).where(cls.login == login)
        return db.session.scalar(query)


    @classmethod
    def find_by_name(cls, name):
        query = sa.select(cls).where(cls.name == name)
        return db.session.scalar(query)
    

    @classmethod
    def create_user(cls, status, name, login, password_hsd):
        user = cls(status=status, name=name, login=login, password=password_hsd)
        db.session.add(user)
        db.session.commit()
        return user
    
    @classmethod
    def find_by_status(cls, status):
        query = sa.select(cls).where(cls.status == status)
        return db.session.scalars(query).all()
    
