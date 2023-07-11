from sqlalchemy import create_engine


CONNSTR = f'postgresql://abulaman6:yicaSQ6N9Kpq@ep-red-tooth-652944.us-east-2.aws.neon.tech/neondb'

engine = create_engine(CONNSTR)
