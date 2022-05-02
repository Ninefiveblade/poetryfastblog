from db.base_class import Base


class Post(Base):
    """Модель поста"""
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(String)
