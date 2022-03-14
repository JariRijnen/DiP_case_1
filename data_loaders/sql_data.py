import pandas as pd
import sqlalchemy
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('env_user.env')
load_dotenv(dotenv_path=dotenv_path)


class Employee_DB:
    def __init__(self):
        self.username = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')
        self.host_name = os.getenv('DB_HOST_NAME')
        self.name = os.getenv('DB_NAME')
        self.engine = self.establish_engine()

    def establish_engine(self) -> sqlalchemy.engine:
        """Create SQLalchemy engine"""
        return sqlalchemy.create_engine(f'postgresql://{self.username}:{self.password}'
                                        f'@{self.host_name}/{self.name}')

    def insert_sql_data(self) -> pd.DataFrame:
        """Insert SQL data into a pandas dataframe"""
        with self.engine.connect() as con:
            df = pd.read_sql('SELECT * FROM dip_employees', con)

            # If last name is given, concat first and last name into a single column
            df['name'] = df.agg(lambda x: f"{x['first_name']} {x['last_name']}" if
                                x['last_name'] is not None else x['first_name'], axis=1)
            return df


if __name__ == '__main__':
    dip_data = Employee_DB()
    df = dip_data.insert_sql_data()
    print(df.dtypes)
    print(df)
