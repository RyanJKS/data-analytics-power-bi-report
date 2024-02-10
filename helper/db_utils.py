from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
import os
import pandas as pd
import yaml


class RDSDatabaseConnector:
    """
    A class for connecting to an RDS database using credentials from a YAML file.

    Attributes:
        db_creds (dict): Database credentials loaded from a YAML file.
        engine (create_engine): SQLAlchemy engine object for database connection.

    Methods:
        read_db_creds(yaml_file_path: str) -> dict: Reads database credentials from a YAML file.
        init_db_engine() -> create_engine: Initializes the database engine.
        extract_from_db(table_name: str) -> pd.DataFrame: Extracts data from the database into a DataFrame.
        save_to_csv(df: pd.DataFrame, data_type: str, file_name: str): Saves a DataFrame to a CSV file.
    """
        
    def __init__(self, yaml_file_path) -> None:
        """
        Initializes the RDSDatabaseConnector instance.

        Args:
            yaml_file_path (str): The file path to the YAML file containing database credentials.

        Returns:
            None
        """
        self.db_creds = self.read_db_creds(yaml_file_path)
        self.engine = self.init_db_engine()
    
    def read_db_creds(self, yaml_file_path) -> dict:
        """
        Reads database credentials from a YAML file.

        Args:
            yaml_file_path (str): The file path to the YAML file.

        Returns:
            dict: A dictionary containing the database credentials.
        """        
        if not os.path.exists(yaml_file_path):
            raise FileNotFoundError(f"YAML file {yaml_file_path} not found")
        
        try:
            with open(yaml_file_path, 'r') as file:
                return yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise Exception(f"Error reading YAML file: {e}")
    
    def init_db_engine(self) -> create_engine:
        """
        Initializes the database engine.

        Returns:
            create_engine: A SQLAlchemy engine object for database connection.
        """
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        USER = self.db_creds['USER']
        PASSWORD = self.db_creds['PASSWORD']
        ENDPOINT = self.db_creds['HOST']
        PORT = self.db_creds['PORT']
        DATABASE = self.db_creds['DATABASE']

        try:
            engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
            return engine
        except SQLAlchemyError as e:
            raise Exception(f"Error initializing database engine: {e}")

    
    def get_table_list(self) -> pd.DataFrame:
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        df = pd.DataFrame(tables, columns=['Table Name'])
        return df
    
    def get_columns_list(self, table_name: str) -> pd.DataFrame:
        inspector = inspect(self.engine)
        columns = inspector.get_columns(table_name)
        df = pd.DataFrame(columns)
        return df[['name', 'type']]
    
    @staticmethod
    def save_to_csv(df: pd.DataFrame, path: str, file_name: str) -> None:
        """
        Saves a DataFrame to a CSV file.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            path (str): A string representing the path to save the dataframe to.
            file_name (str): The name of the file to save.

        Returns:
            None
        """

        if not os.path.exists(path):
            os.makedirs(path)
        df.to_csv(os.path.join(path, file_name), index=False)

            