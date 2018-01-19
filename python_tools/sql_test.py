# -*- coding: utf-8 -*-
#!/usr/bin/env python
#-*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

engine = create_engine('mysql+mysqlconnector://root:wolongdata@mysql.test.cdecube.com', poolclass=NullPool)
Session = sessionmaker(bind=engine)

session = Session()
print(id(session))

#a = Session()
#a.close()
#print(id(a))
#Session().close()
#print(id(Session()))
