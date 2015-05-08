from sqlalchemy.ext.declarative import declarative_base
BaseMaster = declarative_base()


from sqlalchemy.dialects.mysql import (
    DATE,
    DATETIME,
    INTEGER,
    VARCHAR
)
from sqlalchemy.schema import (
    Column,
    ForeignKey,
)


class MArea(BaseMaster):
    __tablename__ = "m_area"
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(50))


class MStage(BaseMaster):
    __tablename__ = "m_stage"
    id = Column(INTEGER, primary_key=True)
    area_id = Column(INTEGER, ForeignKey('m_area.id'))
    stage_no = Column(INTEGER)
    round = Column(INTEGER)
    time_limit = Column(INTEGER)


class MProduct(BaseMaster):
    __tablename__ = "m_product"
    id = Column(INTEGER, primary_key=True)
    product_id = Column(VARCHAR(50), unique=True)
    tier = Column(VARCHAR(50))
    price = Column(INTEGER)
    amount = Column(INTEGER)
    name = Column(VARCHAR(50))


class MTerm(BaseMaster):
    __tablename__ = "m_term"
    id = Column(INTEGER, primary_key=True)
    starttime = Column(DATETIME)
    endtime = Column(DATETIME)
    startdate = Column(DATE)
