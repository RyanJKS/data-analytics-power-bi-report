from sqlalchemy import create_engine
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
        USER = self.db_creds['RDS_USER']
        PASSWORD = self.db_creds['RDS_PASSWORD']
        ENDPOINT = self.db_creds['RDS_HOST']
        PORT = self.db_creds['RDS_PORT']
        DATABASE = self.db_creds['RDS_DATABASE']

        try:
            engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
            return engine
        except SQLAlchemyError as e:
            raise Exception(f"Error initializing database engine: {e}")

    
    def extract_from_db(self, table_name: str) -> pd.DataFrame:
        """
        Extracts data from the specified table in the database into a DataFrame.

        Args:
            table_name (str): The name of the table from which to extract data.

        Returns:
            pd.DataFrame: A DataFrame containing the extracted data.
        """        
        try:
            with self.engine.begin():
                # Read the data and return it in datafram format
                df = pd.read_sql_table(table_name, self.engine)
                return df

        except SQLAlchemyError as e:
            raise Exception(f"An error occurred while extracting data: {e}")
    
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

            