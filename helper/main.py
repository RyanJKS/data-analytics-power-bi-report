from db_utils import RDSDatabaseConnector


def get_finance():
    finance_instance = RDSDatabaseConnector('db_creds/postgres_db_creds.yaml')
    
    dataset = finance_instance.extract_from_db('loan_payments')
    path_to_save_file = 'datasets/finance/'
    file_name = 'Finance_Data.csv'
    finance_instance.save_to_csv(dataset, path_to_save_file, file_name)
    return None
    
    
if __name__ == "__main__":
    print(get_finance())