# -*- coding: utf-8 -*-
#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

engine = create_engine('mysql+mysqlconnector://root:123456@192.168.0.7:3306', poolclass=NullPool)
Session = sessionmaker(bind=engine)

session = Session()
print(id(session))
