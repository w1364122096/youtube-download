try:
    from sqlalchemy import create_engine, Column, Integer, String, DateTime, Table, ForeignKey, Float
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, relationship
except ImportError:
    print("请先安装 SQLAlchemy: pip install sqlalchemy")
    raise

from datetime import datetime
from pathlib import Path
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

# 视频和标签的多对多关系表
video_tags = Table('video_tags', Base.metadata,
    Column('video_id', Integer, ForeignKey('videos.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Video(Base):
    __tablename__ = 'videos'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    filename = Column(String, unique=True)
    url = Column(String)
    format = Column(String)
    size = Column(Float)  # MB
    download_type = Column(String)
    download_time = Column(DateTime, default=datetime.now)
    last_watched = Column(DateTime)
    path = Column(String)
    status = Column(String)  # downloaded, deleted, failed
    tags = relationship('Tag', secondary=video_tags, back_populates='videos')
    
    @property
    def file_exists(self):
        return Path(self.path).exists() if self.path else False

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    videos = relationship('Video', secondary=video_tags, back_populates='tags')

class DownloadHistory(Base):
    __tablename__ = 'download_history'
    
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    timestamp = Column(DateTime, default=datetime.now)
    action = Column(String)  # download, delete, rename
    details = Column(String)
    video = relationship('Video')

try:
    # 创建数据库目录
    db_dir = Path("data")
    db_dir.mkdir(exist_ok=True)
    
    # 创建数据库引擎和会话
    engine = create_engine('sqlite:///data/videos.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    logger.info("数据库初始化成功")
except Exception as e:
    logger.error(f"数据库初始化失败: {e}")
    raise