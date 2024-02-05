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

## Phase 2: Data Modeling and Analysis

### Date Table Creation and Time Intelligence
- Implemented a continuous Date table using DAX, essential for our time-based analysis.
  - DAX formula for creating Date table covering from the start of the year with the earliest `Orders['Order Date']` to the end of the year with the latest `Orders['Shipping Date']`: 
   ```sh
   Dates = CALENDAR(MIN(Orders[Order Date]), MAX(Orders[Shipping Date]))
   ```

- Enriched the Date table with additional columns for comprehensive time intelligence including Day of Week, Month Number, Month Name, Quarter, Year, and various start of period markers.
  - DAX formulas for additional columns: 
      - Day of Week
         ```sh
         DayOfWeek = WEEKDAY(Dates[Date]-1)
         ``` 
      - Month Number
         ```sh
         Month Number = MONTH(Dates[Date])
         ``` 
      - Month Name
         ```sh
         Month Name = FORMAT(Dates[Date], "MMMM")
         ``` 
      - Quarter 
         ```sh
         Quarter = QUARTER(Dates[Date])
         ``` 
      - Year
         ```sh
         Year = YEAR(Dates[Date])
         ``` 
      - Start of Period (Year, Quarter, Month, Week)
         ```sh
         StartOfYear = STARTOFYEAR(Dates[Date])
         StartOfQuarter = STARTOFQUARTER(Dates[Date])
         StartOfMonth = STARTOFMONTH(Dates[Date])
         StartOfWeek = Dates[Date] - WEEKDAY(Dates[Date],2) + 1
         ```


### Star Schema Development
- Formulated a star-based schema connecting `Products`, `Stores`, `Customers`, `Date`, and `Orders` through one-to-many relationships, streamlining data analysis.
  - Key Relationships: 
      - Products[Product Code] to Orders[Product Code]
      - Stores[Store Code] to Orders[Store Code]
      - Customers[User UUID] to Orders[User UUID]
      - Dates[Date] to Orders[Order Date]
      - Dates[Date] to Orders[Shipping Date]

### Measures Table Organization
- Centralized DAX measures in a dedicated `Measures Table`, enhancing model clarity and manageability.
  - Steps for creating Measures Table:
      - This can be done using the Power Query Editor for visibility and ease of debugging.
      - Model View > Enter Data > Enter table Name

### Key Measures and Hierarchies

#### DAX Formulated Measures

- Developed foundational measures for reporting, including order counts, revenue, profit, and YTD calculations.
**Key Measures:**
   - `Total Orders`: Counts the number of orders.
      ```sh
      Total Orders = COUNT(Orders[Order Date])
      ```
   - `Total Revenue`: 
      ```sh
      Total Revenue = SUMX(Orders, Orders[Product Quantity] * RELATED(Products[Sale Price]))
      ```
   - `Total Profit`: 
      ```sh
      Total Profit = SUMX(Orders, (RELATED(Products[Sale Price]) - RELATED(Products[Cost Price])) * Orders[Product Quantity])
      ```

   - `Total Customers`: Counts unique customers in the `Orders` table.
      ```sh
      Total Custoemrs = DISTINCTCOUNT(Orders[User UUID])
      ```

   - `Total Quantity`: Counts the items sold.
      ```sh
      Total Quantity = SUM(Orders[Product Quantity])
      ```

   - `Profit YTD`: Calculate the year-to-date profit.
      ```sh
      Profit YTD = TOTALYTD(SUMX(Orders, (RELATED(Products[Sale Price]) - RELATED(Products[Cost Price])) * Orders[Product Quantity]), Dates[StartOfYear])
      ```

   - `Revenue YTD`: Calculate the year-to-date revenue.
      ```sh
      Revenue YTD = TOTALYTD(SUMX(Orders, Orders[Product Quantity] * RELATED(Products[Sale Price])), Dates[StartOfYear])
      ```

#### Analytical Hierarchies & Data Model Enhancement
- Introduced Date and Geography hierarchies to deepen report analysis capabilities.
   - **Date Hierarchy:** Facilitates drill-down in reports with levels for Year, Quarter, Month, Week, and Date.
   - **Geography Hierarchy:** Enhances data filtering by region, country, and province/state. Includes a calculated `Country` column mapping country codes to names and a `Geography` column for accurate mapping.
   - Create a new calculated column in the Stores table called Country that creates a full country name for each row, based on the Stores[Country Code] column, according to the following scheme:
   GB : United Kingdom
   US : United States
   DE : Germany

   ```sh
   Country = SWITCH([Country Code], "GB", "United Kingdom", "US", "United States", "DE", "Germany")
   ```
   - Create a new calculated column in the Stores table called Geography that creates a full geography name for each row, based on the Stores[Country Region], and Stores[Country] columns, separated by a comma and a space.

   ```sh
   Geography = CONCATENATE(Stores[Country Region], CONCATENATE(", ", Stores[Country]))
   ```

   - Assigned appropriate data categories for improved geographical analysis and mapping precision.
  - Instructions for assigning data categories: 
   - Table view > Column Tools > Data Category > Select Type below.
      - World Region : Continent
      - Country : Country
      - Country Region : State or Province

This phase underlines a pivotal advancement in crafting a dynamic business intelligence solution. It lays down a robust foundation for insightful analytics, paving the way for the next stages of visual enhancement and data optimization.

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