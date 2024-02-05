# Quarterly Business Intelligence Report with Power BI

## Project Overview
This project aims to elevate the business intelligence practices of a medium-sized international retailer by transforming their extensive sales data into actionable insights. Leveraging Microsoft Power BI, we design a comprehensive quarterly report that aids in informed decision-making at various levels of the organization.

### Objectives
- **Data Consolidation**: Extract and transform data from multiple sources to create a unified dataset.
- **Data Modeling**: Implement a robust star-schema data model to facilitate insightful analysis.
- **Report Design**: Develop a multi-page Power BI report that includes:
  - A high-level business summary for C-suite executives.
  - Customer segmentation by sales region to identify high-value customers.
  - Analysis of top-performing products by category against sales targets.
  - A map visual highlighting retail outlet performance across territories.


## Phase 1: Data Loading and Preparation

### Overview
The initial phase focuses on setting up the environment, connecting to various data sources, and preparing the dataset for analysis. This includes:

- Connecting to an Azure SQL Database, Microsoft Azure Storage account, and web-hosted CSV files.
- Cleaning and organizing the data by removing irrelevant columns, splitting date-time details, ensuring data consistency, and renaming the columns to fit Power BI conventions.
- Datasets: Orders (fact) Table and Dimension Tables (Products, Stores and Customers)

### Environment Setup for Mac/Linux Users
1. **Create an Azure Virtual Machine (VM):**
   - Sign up for a free Azure account.
   - Create a Windows VM with the size D2s_v3. The Azure free trial includes a $200 credit.
   - Connect to the VM using Microsoft Remote Desktop and the Remote Desktop Protocol (RDP).

2. **Install Power BI Desktop on the VM:**
   - Download and install Power BI Desktop from the official Microsoft website.

### Data Connection and Preparation
1. **Orders Data:** Azure SQL Database
   - Contains information about each order, including the order and shipping dates, the customer, store and product IDs for associating with dimension tables, and the amount of each product ordered. 
   - Each order in this table consists of an order of a single product type, so there is only one product code per order.

2. **Products Data:** Import CSV file
   - Contains information about each product sold by the company, including the product code, name, category, cost price, sale price, and weight.

3. **Stores Data:** Azure Blob Storage


4. **Customers Data:** Import CSV files from folder


Common prepartion:
- Dropping data sensitive columns
- Renaming columns
- Splitting columns
- Dropping duplicates

## Getting Started
To work on this project, you'll need Microsoft Power BI Desktop installed on your computer. Clone this repository to get started with the pre-configured Power BI template and the sample datasets.

### Prerequisites
- Microsoft Power BI Desktop
- Basic understanding of Power BI and data modeling concepts

### Installation
1. Install Microsoft Power BI Desktop from the [official website](https://powerbi.microsoft.com/en-us/downloads/).
2. Clone this repository or download the ZIP file and extract it to your local machine.
3. Open the `.pbix` file with Power BI Desktop to start exploring the report.

## Usage
The project is structured to guide users through the process of data extraction, transformation, and visualization:
1. **Load Data**: Import your sales data from the various sources into Power BI.
2. **Transform Data**: Utilize the Power Query Editor to clean and prepare your data.
3. **Model Data**: Build the star-schema model to link your data tables effectively.
4. **Visualize Data**: Create the report pages using Power BI's visualization tools.

Refer to the `Documentation` folder for detailed guides on each step.

## Contributing
We welcome contributions to improve this project. If you have suggestions or improvements, please fork the repository and create a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## Acknowledgments
- AiCore
- Microsoft Power BI Community for the invaluable resources and support.