from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so

from ..extensions import db


class Post(db.Model):
    id : so.Mapped[int] = so.mapped_column(primary_key=True)
    teacher : so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id", ondelete="CASCADE"))
    subject : so.Mapped[str] = so.mapped_column(sa.String(250))
    student : so.Mapped[int] = so.mapped_column(sa.Integer)
    date : so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    author = so.relationship("User", back_populates="posts")
    
    @classmethod
    def create_post(cls, teacher, subject, student):
        post = Post(teacher=teacher, subject=subject, student=student)

        db.session.add(post)
        db.session.commit()

        return post
    

    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)


    @classmethod
    def update_post(cls, post, subject, student):
        post.subject = subject
        post.student = student

        db.session.commit()

        return post
    

    @classmethod
    def delete_post(cls, id):
        post = db.session.get(cls, id)
        
        db.session.delete(post)
        db.session.commit()

    
    @classmethod
    def get_all_oredered_by_date(cls, descending=True):
        query = sa.select(cls)

        if descending:
            query = query.order_by(sa.desc(cls.date))
        else:
            query = query.order_by(cls.date)

        return db.session.scalars(query).all()
    

    @classmethod
    def get_by_teacher(cls, teacher, descending=True):
        query = sa.select(cls).where(cls.teacher == teacher)
        if descending:
            query = query.order_by(sa.desc(cls.date))
        else:
            query = query.order_by(cls.date)
        
        return db.session.scalars(query).all()



