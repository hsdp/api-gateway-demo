from sqlalchemy import Column, Sequence, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from database import ModelBase


users_id_seq = Sequence('users_id_seq')


class Users(ModelBase):
    __tablename__ = 'users'

    id = Column(Integer,
                users_id_seq,
                server_default=users_id_seq.next_value(),
                primary_key=True,
                nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    comments = Column(JSONB)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'comments': self.comments,
        }
