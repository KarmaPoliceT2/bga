import datetime
from bga.models.meta import Base
from sqlalchemy import Column, Integer, Unicode, UnicodeText, DateTime, String
from passlib.apps import custom_app_context as blogger_pwd_context
from bigchaindb_driver.crypto import generate_keypair


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    pubkey = Column(String, nullable=False)
    privkey = Column(String, nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)

    def verify_password(self, password):
        if password == self.password:
            self.set_password(password)
        return blogger_pwd_context.verify(password, self.password)

    def set_password(self, password):
        password_hash = blogger_pwd_context.encrypt(password)
        self.password = password_hash

    def setup_keypair(self):
        v = generate_keypair()
        self.pubkey = v.public_key
        self.privkey = v.private_key
