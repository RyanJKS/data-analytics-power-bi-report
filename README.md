# Quarterly Business Intelligence Report with Power BI

## Project Overview
This project aims to elevate the business intelligence practices of a medium-sized international retailer by transforming their extensive sales data into actionable insights. Leveraging Microsoft Power BI, we design a comprehensive quarterly report that aids in informed decision-making at various levels of the organization.

<!--Include GIF to show how report works-->

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

### Data Connection & Extraction
1. **Orders Data (Fact Table):** Azure SQL Database
   - Contains information about each order, including the order and shipping dates, the customer, store and product IDs for associating with dimension tables, and the amount of each product ordered. 
   - Each order in this table consists of an order of a single product type, so there is only one product code per order.

2. **Products Data:** Import CSV file
   - Contains information about each product sold by the company, including the product code, name, category, cost price, sale price, and weight.

3. **Stores Data:** Azure Blob Storage
   - Contains information about the location of the stores

4. **Customers Data:** Import CSV files from folder
   - Contains information about the customers personal data and purchase history

### Data Preparation
The following transformation were made in order to ensure data integrity and consistency across all dataset.

- Dropping data sensitive columns
- Renaming columns to fit Power BI conventions.
- Splitting columns
- Dropping duplicates
- Removing irrelevant columns
- Splitting date-time details


> Note: All changes were made whilst in the `Table View` > `Transform Data` and by making use of the `Data Preview` features under the `View` tab. This project also assume you have **on-object formatting** enabled on Power BI Desktop app. To enable it, follow these steps: **File > Options and Settings > Options > Preview Features > On-object interaction** and make sure the checkbox is ticked.


## Phase 2: Data Modeling


### Introduction to Date Table and Time Intelligence

In our dataset, the absence of a dedicated Date table limits our ability to leverage Power BI's time intelligence capabilities fully. A continuous Date table, spanning the entire timeframe of our data, is crucial for enabling these functions. The Date table is fundamental for time-based analysis, allowing us to perform operations like year-over-year comparisons, calculating running totals, and more. The importance of having a Date table formatted as a `date` data type lies in its necessity for time intelligence calculations, which require a continuous date range to function correctly.

#### Creating a Continuous Date Table
To address this, we've implemented a continuous Date table using DAX, covering from the earliest `Order Date` to the latest `Shipping Date`. This enables a broad range of time intelligence functions in Power BI.
   ```sh
   Dates = CALENDAR(MIN(Orders[Order Date]), MAX(Orders[Shipping Date]))
   ```
**Enriching the Date Table for Comprehensive Analysis**
The Date table has been enriched with several columns to support comprehensive time intelligence markers.

<details>
  <summary>DAX Queries for Additional Date Table Columns</summary>

   - **Day of Week**
      ```sh
      DayOfWeek = WEEKDAY(Dates[Date]-1)
      ``` 
   - **Month Number**
      ```sh
      Month Number = MONTH(Dates[Date])
      ``` 
   - **Month Name**
      ```sh
      Month Name = FORMAT(Dates[Date], "MMMM")
      ``` 
   - **Quarter** 
      ```sh
      Quarter = QUARTER(Dates[Date])
      ``` 
   - **Year**
      ```sh
      Year = YEAR(Dates[Date])
      ``` 
   - **Start of Period (Year, Quarter, Month, Week)**
      ```sh
      StartOfYear = STARTOFYEAR(Dates[Date])
      StartOfQuarter = STARTOFQUARTER(Dates[Date])
      StartOfMonth = STARTOFMONTH(Dates[Date])
      StartOfWeek = Dates[Date] - WEEKDAY(Dates[Date],2) + 1
      ```
</details>

### Star Schema Development
The adoption of a star schema in this project is strategic, enhancing our data model's analytical capabilities. This schema simplifies complex data relationships, making it easier to perform queries and generate insightful analyses and visualizations. By centralizing the data around a single fact table (Orders) and connecting it to related dimension tables (Products, Stores, Customers, Dates), we can efficiently query the model and produce meaningful reports.

#### Schema Relationships
- **Products[Product Code]** ↔ **Orders[Product Code]**
- **Stores[Store Code]** ↔ **Orders[Store Code]**
- **Customers[User UUID]** ↔ **Orders[User UUID]**
- **Dates[Date]** ↔ **Orders[Order Date]** (active relationship)
- **Dates[Date]** ↔ **Orders[Shipping Date]** (inactive)

![Star Scehma Diagram](/assets/misc/star-schema.PNG)

> Note: All relationships were established in the `Model View` by linking primary and foreign keys between the dimension tables and the fact table.


## Phase 3: DAX Mesaures and Analysis

### Establishing a Measures Table
Introducing a dedicated Measures Table has significantly enhanced the manageability and clarity of our data model. This centralized table, constructed using DAX and aggregating values from other tables, is essential for efficient data analysis within Power BI.

- **Creation of the Measures Table:**
  - Utilized the Power Query Editor for its setup, providing an intuitive interface for debugging.
  - Through the Model View, "Enter Data" was selected to initiate a new table specifically designated for measures.

### Comprehensive DAX Measures for In-depth Reporting
We have developed a robust set of DAX measures that are foundational for our reporting needs. These measures range from simple counts such as total orders to complex calculations for year-to-date (YTD) analytics.

**Key Measures Include:**
- **Total Orders**: Counts the number of orders by evaluating the Orders table's Order Date column.
- **Total Revenue & Profit**: Computes revenue and profit by correlating product quantities and prices between the Orders and Products tables.
- **Total Customers**: Identifies unique customers within the Orders dataset.
- **Profit YTD & Revenue YTD**: Analyzes profitability and revenue over the current fiscal year.
- **Advanced Measures**: Features like **Revenue per Customer**, **Top Customer Analysis**, and **Quarterly Targets** elevate the project's analytical depth.

<details>
  <summary>DAX Queries Measures</summary>

   - **Total Orders**: 
      ```sh
      Total Orders = COUNT(Orders[Order Date])
      ```
   - **Total Revenue**: 
      ```sh
      Total Revenue = SUMX(Orders, Orders[Product Quantity] * RELATED(Products[Sale Price]))
      ```
   - **Total Profit**: 
      ```sh
      Total Profit = SUMX(Orders, (RELATED(Products[Sale Price]) - RELATED(Products[Cost Price])) * Orders[Product Quantity])
      ```
   - **Total Customers**: Counts unique customers in the `Orders` table.
      ```sh
      Total Custoemrs = DISTINCTCOUNT(Orders[User UUID])
      ```
   - **Total Quantity**: Counts the items sold.
      ```sh
      Total Quantity = SUM(Orders[Product Quantity])
      ```
   - **Profit YTD**: Calculate the year-to-date profit.
      ```sh
      Profit YTD = TOTALYTD([Total Profit], Dates[Date])
      ```
   - **Revenue YTD**: Calculate the year-to-date revenue.
      ```sh
      Revenue YTD = TOTALYTD([Total Revenue], Dates[Date])
      ```
   - **Revenue per Customer**:
      ```sh
      Revenue per Customer = [Total Revenue] / [Total Customers]
      ```
   - **Top Customer**:
      ```sh
      Top Customer = MAXX(
         TOPN(1, ALL(Customers), [Total Revenue]),
         Customers[Full Name]
      )
      ```

   - **Top Customer Total Orders**:
      ```sh
      Top Customer Total Orders = CALCULATE(
         [Total Orders],
         FILTER(
            ALL(Customers),
            Customers[Full Name] = [Top Customer]
         )
      )
      ```

   - **Top Customer Total Revenue**:
      ```sh
      Top Customer Total Revenue = CALCULATE(
         [Total Revenue],
         FILTER(
            ALL(Customers),
            Customers[Full Name] = [Top Customer]
         )
      )
      ```
   **KPI**: Mostly be used on Executive Summary page of report
   - `Previous Quarter Orders, Profit and Revenue`: In this measure, DATEADD(Dates[Date], -1, QUARTER) moves the current date context back by one quarter. Then TOTALQTD computes the quarter-to-date total within this shifted context. Essentially, this measure is attempting to calculate the revenue from the start of the previous quarter to the date equivalent to today's date but in the previous quarter. `PREVIOUSQUARTER()` causes an issue because there the current date is not available in the Dates table which is why we have to manually shift the date using DATEADD. The TOTALQTD function with DATEADD could be calculating a different set of data than PREVIOUSQUARTER due to how dates are handled in your model. TOTALQTD is designed to work with complete quarters, but when combined with DATEADD, it may be looking at an incomplete set of dates.

   The PREVIOUSQUARTER function expects a complete date table that includes dates up to the current date. If the Dates table ends in June 2023 and you're attempting to calculate values in February 2024, the PREVIOUSQUARTER function will not work because it cannot find the context of dates for the previous quarter in 2024. This results in a blank value because there is no data for it to calculate.

   On the other hand, the DATEADD function with TOTALQTD is more flexible because it shifts the context back by one quarter from the latest available date in your Dates table. If the latest date is in June 2023, DATEADD is able to calculate the total for what would have been the "previous quarter" from that point in time.
   
      ```sh
      Previous Quarter Orders = CALCULATE([Total Orders], PREVIOUSQUARTER(Dates[Date]))
      Previous Quarter Revenue = CALCULATE([Total Revenue], PREVIOUSQUARTER(Dates[Date]))
      Previous Quarter Profit = CALCULATE([Total Profit], PREVIOUSQUARTER(Dates[Date]))

      Previous Quarter Orders = CALCULATE(
         TOTALQTD([Total Orders], DATEADD(Dates[Date], -1, QUARTER))
      )
      
      Previous Quarter Revenue = CALCULATE(
         TOTALQTD([Total Revenue], DATEADD(Dates[Date], -1, QUARTER))
      )
      Previous Quarter Revenue = CALCULATE(
         TOTALQTD([Total Revenue], DATEADD(Dates[Date], -1, QUARTER))
      )
      ```
      > Note: This is why the PREVIOUSQUARTER() method does not work in this scenario.

   - `Targets`: Set to 5% Growth compared to the previous quarter
      ```sh
      Target Profit = [Previous Quarter Profit] * 1.05
      Target Revenue = [Previous Quarter Revenue] * 1.05
      Target Orders = [Previous Quarter Orders] * 1.05
      ```
   **Quartely Targets**: Mostly used in the Customer Detail Page

   - `Total Orders QTD`:
   ```sh
   Total Orders QTD = TOTALQTD(
      [Total Orders],
      Dates[Date]
   )
   ```

   - `Total Profit QTD`:
   ```sh
   Total Profit QTD = TOTALQTD(
      [Total Profit],
      Dates[Date]
   )
   ```

   - `Total Revenue QTD`:
   ```sh
   Total Revenue QTD = TOTALQTD(
      [Total Revenue],
      Dates[Date]
   )
   ```

   - `Current Targets`: The CEO has told you that they are targeting 10% quarter-on-quarter growth in all three metrics.
   ```sh
   Current Target Profit = [Previous Quarter Profit] * 1.1
   Current Target Revenue = [Previous Quarter Revenue] * 1.1
   Current Target Orders = [Previous Quarter Orders] * 1.1
   ```
   - Milestone 7 given: Mostly used in the STores Drillthorugh page
   ```sh
   Category Selection = IF(ISFILTERED(Products[Category]), SELECTEDVALUE(Products[Category]), "No Selection")

   Country Selection = IF(ISFILTERED(Stores[Country]), SELECTEDVALUE(Stores[Country]), "No Selection")
   ```

   ```sh
   Profit per Order = [Total Profit] / [Total Orders]
   ```
</details>


Note: All changes were made whilst in the `Model View`


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


## Overview of Report Pages

This section delves into the specifics of each page within our Power BI report. Each page is meticulously designed to cater to various analytical needs, from high-level executive summaries to detailed customer insights. For every report page, we provide an overview, visual setup explanations, and insights into the cross-filtering and highlighting features that interconnect the data visualizations, enhancing the report's interactivity and analytical depth.

### Executive Summary Page

#### Visual Overview
![Executive Summary](path/to/executive_summary_image.png)

**Setup and Purpose**: The Executive Summary page is crafted to provide a snapshot of the company's overall performance. It includes key performance indicators (KPIs), trend analyses, and summary charts to give executives a quick, yet comprehensive view of business health.

- Cards:
Format > Callout Value pane to ensure no more than 2 decimal places in the case of the revenue and profit cards, and only 1 decimal place in the case of the Total Orders measure

- KPI Visuals:

KPI Graph > 
The Value field should be Total Revenue
The Trend Axis should be Start of Quarter
The Target should be Target Revenue

In the Format pane, set the Trend Axis to On, expand the associated tab, and set the values as follows:


Direction : High is Good
Bad Colour : red
Transparency : 15%

- Table:
Top 10 products that racks more revfenue.
TopN filter on description column with total revenue as value.

**Cross Filtering and Highlighting**: 
- `Product Category Bar Chart` and `Top 10 Products Table` should not filter the `Card` visuals or `KPIs`

> Note: This was achieved by using the `Edit Interactions` view in the `Format` tab of the ribbon.

### Customer Detail Page

#### Visual Overview
![Customer Detail](path/to/customer_detail_image.png)

**Setup and Purpose**: This page focuses on analyzing customer behavior and segmentation. It includes detailed metrics on customer value, purchase patterns, and segmentation analyses to inform targeted marketing strategies.

- Renaming VIsuals (Card data):
Report View > Build a visual > Fields > Right Click (Rename Visual)

- Line Chart - Forecasts
Power BI allows you to forecast future data points based on historical data, offering insights into potential future trends.

Activate Forecast: With the line chart selected, navigate to the Analytics pane and click on the + Add button next to Forecast

Adjust Forecast Settings: The following settings can be defined for the forecast:

Units: The units of the time domain of the forecast. You can choose any absolute time value (eg. months or seconds), or choose "points" to have it reflect the current timebase of the chart.

Forecast Length: The number of the specified units over which the forecast should be made

Seasonality: The value of any periodicity in the data. For example if you choose months as units, and expect periodicity over the course of a year, you can set this value to 12. If left on the default value of Auto, it will attempt to estimate the periodicity.

Confidence Interval: The probability that the result falls within the forecast area. Generally, the higher the confidence interval, the broader the forecast area, as it accounts for more potential variability and uncertainty in the data. This means that with a higher confidence interval, there's a greater likelihood that the actual outcome will fall within the predicted range, but the range itself will be wider.

- Table TopnN customers
TopN Filter
Taking the bar chart in the previous figure, let's say we want to change it to only display the top 3 product categories by revenue.


Select the Visual: Click on the bar chart you want to filter
Open the Filter Pane: Navigate to the Filter pane on the right
Apply TopN Filter:
From the Data pane, we drag the Product[Category] field into the Filters on this visual section of the filter pane
Click on Filter type dropdown
Choose the TopN filter option
We then specify the number 3 to filter the top 3 categories, and then drag the value we want to rank the categories by (in this case our Total Revenue measure ), inbto the By Value field

Conditional format for bars:
 Report View > Build a Visual > Column NAme > Right Click > Condigitonal Formating > Data bars

- 3 CArds for top customers:
Dax formuala: Top Customer ... to be used

- Slicer
Slicer > Field  (Year) 
Format > Slicer Settings > Select (Between)


**Cross Filtering and Highlighting**:
- `Top 20 Customers table` should not filter any of the other visuals 
- `Total Customers by Product Donut Chart` should not affect the `Customers Line Graph` 
- `Total Customers by Country Donut chart` should cross-filter `Total Customers by Product Donut Chart`

### Product Detail Page

#### Visual Overview
![Product Detail](path/to/product_detail_image.png)

**Setup and Purpose**: Aimed at understanding product performance, this page breaks down sales by product categories, performance against targets, and inventory levels, offering insights into product strategy and optimization.

- Guage Format :
   - Report View > Format > Callout value > Values > Fx > set conditional format

- Cards:
   - If the Products[Category] column is filtered to a single value, Category Selection returns that specific category.
   - If Products[Category] is not filtered or is filtered to multiple values, Category Selection returns "No Selection".
   - The same logic applies to Country Selection for the Stores[Country] column.
   - These measures can be used in visuals or cards to display the currently selected category or country, or to indicate if no specific selection has been made. They are helpful for providing interactive feedback to report users about the current filtering context.

- Area Chart: Shows how the different product categories are performing in terms of revenue over time.

   - X axis should be Dates[Start of Quarter]
   - Y axis values should be Total Revenue
   - Legend should be Products[Category]
   
- Scatter Graph
   - Create CALCULATED COLUMN in products table.
      ```sh
      Profit per Item = [Sale Price] - [Cost Price]
      ```

   - Values should be Products[Description]
   - X-Axis should be Products[Profit per Item]
   - Y-Axis should be Orders[Total Quantity]
   - Legend should be Products[Category]

**Cross Filtering and Highlighting**:
- `Orders vs. Profitability Scatter Graph` should not affect any other visuals 
- `Top 10 Products Table` should not affect any other visuals

### Stores Map

#### Visual Overview
![Stores Map](path/to/stores_map_image.png)

**Setup and Purpose**: The Stores Map provides a geographical view of retail performance, including sales, customer footfall, and regional market penetration, essential for strategic planning and regional analysis.

- Settings:
Format Pane > Category labels on
Format Pane > Map Settings > Controls > :
Auto-Zoom: On
Zoom buttons: Off
Lasso button: Off


Assign your Geography hierarchy to the Location field, and ProfitYTD to the Bubble size field

**Cross Filtering and Highlighting**:
- Discuss how selecting specific regions or stores on the map influences data across the report, particularly in the Stores Drill Through and Product Detail pages, illustrating the geographical impact on sales and product popularity.

### Stores Drill Through

#### Visual Overview
![Stores Drill Through](path/to/stores_drill_through_image.png)

**Setup and Purpose**: Designed for deep dives into individual store performances, this page offers detailed analytics on sales, customer demographics, and inventory for selected stores from the Stores Map.

- Create a new page named Stores Drillthrough. Open the format pane and expand the Page information tab. Set the Page type to Drillthrough and set Drill through when to Used as category. Set Drill through from to country region.
- Guage:
   -  Profit YTD and Revenue YTD: You should have already created this earlier in the project
   -  Profit Goal and Revenue Goal, which should be a 20% increase on the previous year's year-to-date profit or revenue at the current point in the year

- DAX
   ```sh
   Profit YTD Previous Year = 
   CALCULATE(
      [Profit YTD],
      SAMEPERIODLASTYEAR(Dates[Date])
   )

   Revenue YTD Previous Year = 
   CALCULATE(
      [Revenue YTD],
      SAMEPERIODLASTYEAR(Dates[Date])
   )

   ```

   ```sh
   Profit Goal = [Profit YTD Previous Year] * 1.20
   Revenue Goal = [Revenue YTD Previous Year] * 1.20
   ```

**Cross Filtering and Highlighting**:
- Explain the functionality that allows users to navigate from the Stores Map to this detailed view seamlessly. Highlight how data selected here can offer insights into specific customer segments or product performances tied to the store's location.

### Stores Tooltip

#### Visual Overview
![Stores Tooltip](path/to/stores_tooltip_image.png)

**Setup and Purpose**: The Stores Tooltip enhances the interactive experience by providing quick, contextual insights when hovering over elements in the Stores Map, delivering immediate data snapshots without navigating away from the page.

-  Make sure page is setup as tooltip a
- Put graph at top left corner of page and make sure the size of cahrt is the same as Canvas
   Tooltip Size.
- GIF on how it works

**Cross Filtering and Highlighting**:
- Outline how this feature complements the overall navigational flow and data exploration within the report, enriching the user's understanding of store-specific metrics in relation to the broader business landscape.

---

Each page of the report is interconnected through Power BI's robust cross-filtering and highlighting capabilities, ensuring a fluid, intuitive analytical journey across different dimensions of the business data.

### Navbar

Creating an intuitive navigation system within your Power BI report enhances user experience by providing easy access to various report sections and interactive elements. This guide outlines the final steps to add navigation buttons, implement slicers for interactive filtering, and ensure your Navbar is both functional and aesthetically pleasing, including dynamic on-hover effects for better user interaction.

#### Adding Navigation Buttons and Implementing On-Hover Effects

1. **Button Creation**:
   - Start by adding blank buttons for each report page.
   - Go to `Format` > `Button Style` > `Icon` > `Format` = `Custom`, and add an image for each button. This image serves as the visual representation of the button's purpose (e.g., navigating to a specific report page).

2. **Tooltip Configuration**:
   - For each button, activate the tooltip feature under `Action` > `Tooltip` and insert descriptive text, such as "Open Slicer Panel," to guide users on the button's function.

3. **On-Hover Appearance**:
   - Customize the on-hover appearance of each button to enhance user interactivity. Under `Format` > `Button Style`, set the `Apply settings to` field to "On Hover."
   - Select an alternative colorway for the button icon under the `Icon` tab to indicate that the button is interactive when hovered over with the mouse pointer.

#### Setting Up the Slicer Panel

1. **Slicer Background**:
   - Add a new rectangle shape in the same color as your Navbar. This shape should span the same height as the page and be 3-5 times wider than the Navbar itself, serving as a backdrop for the slicers.

2. **Adding Slicers**:
   - Place Vertical Slicer visuals on the newly added box, setting one to `Products[Category]` and the other to `Stores[Country]`. Customize the titles to "Product Category" and "Country" respectively, ensuring clear and intuitive navigation.

3. **Slicer Configuration**:
   - Adjust both slicers to a Vertical List style. The Product Category slicer should allow multiple selections, whereas the Country slicer should be configured to only allow a single selection and include a "Select All" option.

4. **Grouping and Bookmarking**:
   - In the Selection pane, group the slicers with your slicer toolbar shape for organized management.
   - Create two bookmarks: "Slicer Bar Closed" with the slicer toolbar group hidden, and "Slicer Bar Open" with it visible. Make sure "Data" is unchecked in the bookmark options to maintain slicer states when toggling the toolbar.

5. **Assigning Button Actions**:
   - Configure the actions on your buttons to correspond with the bookmarks created. For each button, set the `Type` to "Bookmark," and select the appropriate bookmark. This linkage allows for the dynamic opening and closing of the slicer panel based on user interaction.

#### Finalizing Navigation Buttons

1. **Custom Icon Selection**:
   - For each navigation button, choose a custom icon from the collection you've prepared. Use white icons for the default appearance and cyan (or any color that matches your report's theme) for the on-hover state to visually indicate interactivity.

2. **Recoloring Icons** (Optional):
   - If the default colors do not fit your report's theme, use online tools to recolor your images accordingly.

3. **Page Navigation Configuration**:
   - Turn on the `Action` format option for each button, setting the type to "Page navigation." Then, specify the correct page under `Destination` to ensure accurate navigation.

4. **Grouping and Replication**:
   - Group all navigation buttons together for a unified look. Then, replicate this Navbar setup across all report pages to maintain consistent navigation throughout your Power BI report.

By meticulously following these steps, you'll craft a Power BI report that not only delivers insightful analytics but also offers an engaging and interactive user experience, highlighted by a dynamic Navbar that responds to user interactions.


## Getting Started
To work on this project, you'll need Microsoft Power BI Desktop installed on your computer. Clone this repository to get started with the pre-configured Power BI template and the sample datasets.

### Prerequisites
- Microsoft Power BI Desktop
- Basic understanding of Power BI and data modeling concepts

### Environment Setup for Mac/Linux Users
**Create an Azure Virtual Machine (VM):**
   - Sign up for a free Azure account.
   - Create a Windows VM with the size D2s_v3. The Azure free trial includes a $200 credit.
   - Connect to the VM using Microsoft Remote Desktop and the Remote Desktop Protocol (RDP).


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