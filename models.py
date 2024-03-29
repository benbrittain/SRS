class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    nick = Column(String(100))
    messages = relationship("Message", backref="user", lazy="dynamic")
     
    def __init__(self,nick):
        self.nick = nick
        
    def __repr__(self):
        return self.nick

