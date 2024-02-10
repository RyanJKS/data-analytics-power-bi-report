from db_utils import RDSDatabaseConnector


def main():
    db_instance = RDSDatabaseConnector('../db_creds/postgres_db_creds.yaml')
    
    tables = db_instance.get_table_list()
    db_instance.save_to_csv(tables, '../datasets/db_query/', 'tables_list.csv')
    
    for table in tables['Table Name']:
        columns = db_instance.get_columns_list(table)
        db_instance.save_to_csv(columns, '../datasets/db_query/', f'{table}_columns.csv')

    print("Database tables and columns have been saved to CSV files.")

    
if __name__ == "__main__":
    main()