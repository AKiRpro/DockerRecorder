from enum import Enum
from sqlalchemy import Integer, String, Column, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import ChoiceType


Base = declarative_base()


class State(Enum):
    """Choices for the state attribute of the Room class."""
    PENDING = 0
    PROCESSING = 1
    READY = 2
    ERROR = 3
    PAUSE = 4


class Room(Base):
    """ORM class repeats the structure of the Room table."""
    __tablename__ = 'rooms_room'
    id = Column(Integer, primary_key=True)
    session = Column(String(255), nullable=True)
    start_date = Column(DateTime)
    stop_date = Column(DateTime)
    state = Column(ChoiceType(State, impl=Integer()))
    celery_task = Column(String(255), nullable=True)
    error = Column(Text)
    display = Column(Integer, nullable=True, default=-1)
    chrome_pid = Column(Integer, nullable=True)
    ffmpeg_pid = Column(Integer, nullable=True)
    server = Column(String(50), nullable=True)
    url = Column(String(255), nullable=True)
    check_date = Column(DateTime)
    selected_user = Column(String(255), nullable=True)
    callback_url = Column(Text)
    error_code = Column(Integer, nullable=True, default=0)
    split_status = Column(Text)
    stream_url = Column(String(255), nullable=True)
    token = Column(Text)
    env = Column(String(20), nullable=True)
    blob_container = Column(String(255), nullable=True)
    size = Column(String(100), nullable=True)

    def __repr__(self):
        return f'<Room "{self.id}">'
