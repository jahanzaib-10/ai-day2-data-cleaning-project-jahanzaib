# Part 1: Project Setup

To ensure a clean, modular, and maintainable project architecture, the following folder structure was implemented:

day2-data-cleaning-project-jahanzaib/
│
├── data/
│   ├── processed/
│   │   ├── clean_customers.csv
│   │   ├── clean_orders.csv
│   │   ├── clean_products.csv
│   │   ├── final_sales_dataset.csv
│   │   └── rejected_records.csv
│   │
│   └── raw/
│       ├── customers.csv
│       ├── orders.csv
│       └── products.csv
│
├── notebooks/
│   └── day2_exploration.ipynb
│
├── reports/
│   ├── data_dictionary.csv
│   ├── data_quality_report.csv
│   ├── data_quality_summary.md
│   └── duplicate_records.csv
│
├── sql/
│   └── quality_checks.sql
│
├── src/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── build_pipeline.py
│   ├── clean_data.py
│   ├── load_data.py
│   └── validate_data.py
│
├── data_dictionary.csv
├── README.md
└── requirements.txt

## Important Rule

Files inside the `data/raw/` folder are treated as an immutable source of truth and must never be edited, modified, or overwritten directly.

---

## Part 2: Load and Inspect the Data

All three primary CSV files were loaded into memory using `pandas` to perform initial exploratory data profiling.

### Inspection Metrics Covered

* Total number of rows and columns.
* Column names and active data types.
* First five and last five records preview.
* Missing-value and duplicate-record counts.
* Unique-value cardinality and comprehensive summary statistics.

### Initial Dataset Observations

**Customers Dataset** Contains customer demographic profiles. Initial profiling highlighted formatting inconsistencies in names and trailing whitespace characters inside email fields.
**Products Dataset** Contains item-level catalog details. Observed that several `unit_price` fields were improperly stored as object/string types instead of numeric values.
**Orders Dataset** Contains transactional line items. Identified missing customer/product foreign keys and occasional negative quantity anomalies that required intervention.

---

## Part 3: NumPy Quality Checks

NumPy was integrated to execute fast, vectorized numerical validations and conditional data classifications:

* **Anomaly Detection:** Flagged negative quantities, prices below zero, and impossible numeric values, securely replacing them with `np.nan`.
* **Statistical Calculations:** Computed minimum, maximum, mean, and median metrics across numerical arrays.
*Conditional Classifications (`np.select`)* Categorized transactions into distinct business tiers based on calculated order values using vectorized conditions

```python
conditions = [
    orders["order_value"] < 1000,
    orders["order_value"].between(1000, 5000),
    orders["order_value"] > 5000
]
labels = ["Low Value", "Medium Value", "High Value"]
orders["order_value_category"] = np.select(
    conditions,
    labels,
    default="Unknown"
)

```

## Part 4: Clean the Customer Dataset (`clean_customers`)

A dedicated reusable function named `clean_customers()` was built to standardize customer profiles:

1. Standardized column names to a uniform snake_case convention.
2. Removed unnecessary leading and trailing whitespace.
3. Converted customer names to **Title Case** and email addresses to lowercase.
4. Stripped internal spaces from email strings and standardized regional city names.
5. Parsed registration timestamps into standard datetime formats while identifying unparseable invalid dates.
6. Detected duplicate customer IDs and established strict rules for handling missing attributes safely without corrupting personal data integrity.

---

## Part 5: Clean the Product Dataset (`clean_products`)

A reusable function named `clean_products()` was implemented to clean catalog data:

1. Standardized product names and category groupings.
2. Converted `unit_price` to proper floating-point numeric types and `stock_quantity` to nullable integers.
3. Replaced invalid negative values and handled missing supplier names using standard placeholder text (`"Not Provided"`).
4. Detected duplicate product IDs and flagged products with missing prices or invalid stock values.
5. Ensured faulty records were never silently deleted; instead, they were corrected, replaced with nulls, flagged, or routed to a rejected-records dataset.

---

## Part 6: Clean the Orders Dataset (`clean_orders`)

A robust function named `clean_orders()` was structured to process transaction logs:

1. Standardized column names and dropped completely empty rows.
2. Converted order dates to datetime objects and quantities to numeric values.
3. Normalized discounts into a consistent decimal format.
4. Standardized payment statuses and sales channel categories.
5. Detected duplicate order IDs, negative/zero quantities, and anomalous future order dates.
6. Handled missing foreign keys and created an automated issue-status tracking column:

```python
orders["record_status"] = np.where(
    orders["customer_id"].isna() | orders["product_id"].isna(),
    "Needs Review",
    "Valid"
)


# Part 7: Missing-Value Treatment Strategy

Below is the missing-value treatment table explaining how missing values are handled across different columns and the reasoning behind each strategy.

## Missing-Value Treatment Table

| Column Name | Missing Count | Strategy Selected | Reason / Explanation |
| :--- | :---: | :--- | :--- |
| **customer_name** | 5 | **Keep as missing** | Cannot safely infer name. Filling arbitrary names would corrupt customer identity and personal data integrity. |
| **city** | 12 | **Replace with "Unknown"** | Required for geographic grouping and analysis. Replacing with "Unknown" prevents data loss while maintaining category breakdowns. |
| **quantity** | 8 | **Reject record** | Order value and sales metrics cannot be calculated without quantity. Invalid or missing quantities require record rejection to avoid skewed calculations. |
| **supplier_name** | 20 | **Replace with "Not Provided"** | Supplier name is not critical for core sales analysis. Replacing with a placeholder prevents null-handling errors in reports. |
| **registration_date** | 3 | **Keep as missing** | Temporal analysis requires accurate timestamps. Arbitrarily filling dates would distort time-series trends. |

## Explanation of Methods Used

* **Business-Rule Replacement (`fillna()`):** Applied to `city` and `supplier_name` to insert standard placeholder text ("Unknown" / "Not Provided"), ensuring categorical groupings remain intact.
* **Record Rejection:** Applied to `quantity` because numeric transactions cannot be reliably processed or valued without it.
* **Keep as Missing:** Applied to sensitive fields like `customer_name` and critical timestamps like `registration_date` to prevent artificial data distortion and maintain dataset integrity.

## Part 8: Duplicate Detection & Resolution Strategy

We implemented a systematic check to identify and manage four distinct types of duplicates across the datasets. All identified duplicate records were logged into `reports/duplicate_records.csv` for tracking and auditing.

## Duplicate Handling Documentation

1. **Exact Duplicate Rows:**
   * **Action Taken:** Removed.
   * **Reasoning:** Identical rows across all columns introduce redundancy and artificially inflate transaction counts and metrics. We kept the first occurrence (`keep='first'`) and dropped the rest.

2. **Duplicate Primary Keys (Order IDs / Customer IDs):**
   * **Action Taken:** Removed / Filtered.
   * **Reasoning:** Primary keys must be unique. Duplicate keys break database integrity and relational mappings. We retained the first valid entry and removed subsequent duplicates.

3. **Possible Duplicate Customers:**
   * **Action Taken:** Sent for review / Retained with flagging.
   * **Reasoning:** Customers sharing similar names and emails might represent typos or multiple accounts by the same person. These were flagged for manual review rather than automatic deletion to avoid losing valid customer history.

4. **Duplicate Orders with Conflicting Information:**
   * **Action Taken:** Sent for review.
   * **Reasoning:** When the same `order_id` appeared with conflicting details (e.g., different quantities or amounts), automated resolution was unsafe. These records were isolated and sent for review to verify correct transaction logs.

## Part 10: Date Engineering & Validation

Using advanced pandas datetime functionality, several new temporal features were extracted to support time-series and behavioral analysis. Furthermore, strict validation checks were executed to catch logical data errors.

### Extracted Date Features

* **Order Year, Month, Month Name, Day:** Extracted from `order_date` to enable seasonal and monthly sales aggregation.
* **Day of Week & Weekend Flag (`is_weekend`):** Identifies whether an order was placed on a weekday or weekend (`Saturday`/`Sunday`) to analyze consumer buying patterns.
* **Customer Registration Year:** Extracted to track customer cohort growth over time.
* **Customer Age in Days:** Calculated as the time elapsed between registration and the current reference date.
* **Days Between Registration and First Order:** Measures customer activation time (onboarding lag).

### Date Validation Findings

1. **Invalid Dates:** Rows containing unparseable string formats or missing timestamps were coerced to `NaT` (Not a Time) using `pd.to_datetime(..., errors='coerce')`.
2. **Future Dates:** Checked against the current system timestamp to catch anomalous log entries where orders occurred in the future. These were flagged and filtered.

**Orders Placed Before Registration:** Identified via relational merging of customer registration dates with order timestamps. Orders predating customer registration represent data corruption or historical account mapping issues and were flagged for review.

## Part 11: Advanced Text Cleaning & Standardization

Inconsistent textual data can cause grouping errors, duplicate records, and poor readability. To resolve this, rigorous text-cleaning operations were applied across all string-based columns.

### Implemented Text Operations

1. **Whitespace Removal:** Stripped leading/trailing spaces and replaced internal multiple whitespace characters (`\s+`) with a single space in names and descriptions.
2.**Case Standardization:**
    Converted names, cities, product titles, and categories to **Title Case** (`.str.title()`).
    Converted email addresses and codes to **Lowercase** (`.str.lower()`) to ensure unique and uniform matching.

**Symbol & Punctuation Stripping:** Removed unnecessary special characters and stray punctuation marks from text attributes using regex pattern matching (`[^\w\s]`).
4. **Abbreviation & Spelling Standardization:** Utilized custom dictionary mappings (e.g., mapping `"Lhr"` and `"Lahore City"` to `"Lahore"`, or `"Electronic"` to `"Electronics"`) to unify spelling variations and regional abbreviations.
5. **Blank String Handling:** Standardized empty strings, whitespace-only entries, and missing text fields into uniform placeholder categories (e.g., `"Unknown"` for cities or `"Not Provided"` for suppliers).

## Part 12: Dataset Integration & Relational Joining

To create a consolidated master dataset (`final_sales_dataset.csv`), the cleaned `orders` table was sequentially joined with the `customers` and `products` tables using relational keys (`customer_id` and `product_id`).

### Join Strategy & Validation Findings

1. **Indicator Parameter (`indicator=True`):** Utilized during preliminary validation merges to track row lineage and identify unmatched keys.
2. **Orders Without Matching Customers:** Identified through left-merge indicators where customer data was missing or referenced an obsolete ID.
3. **Orders Without Matching Products:** Isolated orders pointing to non-existent product IDs, which ensures transparency in inventory mapping.
4. **Duplicate Keys & Row Count Integrity:** Used the `validate="many_to_one"` constraint to ensure that multiple orders correctly map to single unique customers and products without unexpected row expansion or cartesian product inflation.
5. **Null Value Tracking:** Evaluated null values introduced by left joins to confirm that missing dimension attributes default to designated placeholder values rather than breaking down financial calculations.

## Part 13: Business Feature Engineering & Calculated Metrics

To drive advanced sales analytics and transaction monitoring, core financial attributes and boolean indicator flags were engineered into the master dataset.

### Financial Calculations

* **Gross Amount:** Computed as `quantity × unit_price` to determine total line-item value before discounts.
* **Discount Amount:** Calculated as `gross_amount × discount` to quantify total savings extended per order.
* **Net Amount:** Final payable revenue derived via `gross_amount − discount_amount`.

### Categorical & Flag Metrics

* **Order Value Category:** Segregates orders into tiers (`Low`, `Medium`, `High`) based on net transaction value for tier-based customer profiling.
* **Missing-Data Flag (`missing_data_flag`):** Identifies records that contain null values in crucial transactional fields.
* **Valid-Record Flag (`valid_record_flag`):** Marks clean, error-free rows suitable for primary financial reporting.
* **Customer/Product Match Flags:** Confirms whether transactional rows successfully linked with master dimension tables during relational joins.
* **High-Discount Flag (`high_discount_flag`):** Flags transactions where applied discounts exceeded a threshold (>15%) for promotional effectiveness tracking.
* **Out-of-Stock Flag (`out_of_stock_flag`):** Detects fulfillment discrepancies where ordered quantities surpassed available inventory stock levels.

## Part 14: Data Dictionary

The data dictionary serves as the official metadata repository for the final processed dataset (`final_sales_dataset.csv`), documenting all core attributes, types, rules, and constraints.

### Data Dictionary Table

| Column Name | Dataset | Description | Data Type | Nullable | Example | Validation Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **order_id** | Orders | Unique order identifier | String | No | ORD1001 | Must be unique and not null |
| **customer_id** | Customers | Unique customer identifier | String | No | CUST101 | Must match customer table keys |
| **product_id** | Products | Unique product identifier | String | No | PROD501 | Must match product table keys |
| **quantity** | Orders | Number of items ordered | Integer | No | 4 | Must be greater than 0 |
| **unit_price** | Products/Orders | Price per unit of product | Float | No | 45.50 | Must be positive numeric |
| **discount** | Orders | Discount applied as decimal | Float | Yes | 0.10 | Value between 0.0 and 1.0 |
| **order_date** | Orders | Date order was placed | Datetime | No | 2026-01-15 | Valid timestamp, not in future |
| **customer_name** | Customers | Full name of customer | String | Yes | John Doe | Title case formatted text |
| **email** | Customers | Customer email address | String | Yes | <john@example.com> | Standardized lowercase string |
| **city** | Customers | Customer city | String | Yes | Lahore | Standardized category/text |
| **product_name** | Products | Name of product | String | No | Wireless Mouse | Non-empty string |
| **category** | Products | Product category | Category | Yes | Electronics | Predefined category group |
| **net_amount** | Calculated | Final payable amount | Float | No | 163.80 | Calculated value >= 0 |

## Part 15: Automated Schema Validation & Quality Assurance

To guarantee data reliability before final export, an automated schema validation function (`validate_schema()`) was implemented. This acts as a quality gate enforcing structural and business rule constraints.

### Enforced Validation Rules & Checks

1. **Schema Structure & Columns:** Verifies that all mandatory columns (such as `order_id`, `customer_id`, `product_id`, `order_date`, `quantity`) exist in the dataset and flags any structural omissions.
2. **Primary Key Integrity:** Ensures that primary identifiers (`order_id`) are completely free of null values and maintain absolute uniqueness.
3. **Numeric Constraints & Ranges:**
   * `quantity > 0`: Prevents zero or negative item quantities.
   * `unit_price >= 0`: Ensures prices are valid non-negative numbers.
   * `0 <= discount <= 1`: Restricts discount decimals within valid percentage boundaries.
4. **Temporal Constraints:** Validates that all order timestamps (`order_date`) are logically sound and do not reference future dates.
5. **Categorical Compliance:** Checks that categorical attributes like `payment_status` and `sales_channel` conform to pre-approved business terminology.
6. **Referential Integrity:** Cross-references foreign keys (`customer_id` and `product_id`) against master dimension tables to isolate orphaned transactional records.

## Part 16: SQL Analysis & Database Quality Checks

To enable relational querying and business intelligence reporting, the final processed dataset (`final_sales_dataset.csv`) was loaded into an SQLite database table named `final_sales`. All analytical queries were structured and stored in `sql/quality_checks.sql`.

### Key SQL Analytical Findings & Queries Covered

1. **Total Order Volume:** Counted total transactions to measure overall business activity.
2. **Total Net Sales:** Computed aggregate financial returns using `SUM(net_amount)`.
3. **Top 5 Products:** Aggregated sales by product name, sorted in descending order, to identify top revenue-generating items.
4. **Top 5 Cities:** Evaluated regional performance by grouping sales totals by customer city.
5. **Data Completeness (Missing Customers):** Filtered records to track orders lacking customer association.
6. **Primary Key Integrity (Duplicates):** Used `GROUP BY` and `HAVING COUNT(*) > 1` to audit any duplicate order IDs.
7. **Average Order Value (AOV):** Calculated the mean transaction value using `AVG(net_amount)`.
8. **Sales Channel Distribution:** Segmented transaction volume across different purchase mediums (e.g., Online, In-Store).
9. **Payment Status Breakdown:** Monitored cash flow and transaction health through payment status frequencies.
10. **High-Frequency Customers:** Isolated repeat customers who placed more than three orders to support loyalty programs.

## Part 17: End-to-End Reusable Pipeline Architecture

To fulfill the requirement of reproducibility and automation, a master execution function (`run_pipeline()`) was structured inside `src/build_pipeline.py`

### Pipeline Execution Flow

1. **Data Ingestion:** Automatically reads raw CSV files (`customers.csv`, `products.csv`, `orders.csv`) from the `data/raw/` directory.
2. **Modular Cleaning:** Applies cleaning, normalization, and text-standardization routines across all independent tables.
3. **Quality Gates & Validation:** Triggers schema checks to catch structural errors, foreign key orphans, or invalid types before final compilation.
4. **Dataset Integration & Metrics:** Merges dimensions with transactional facts and computes calculated financial columns (`net_amount`, value categories, and flags).
5. **Reporting & Persistence:** Exports quality summaries, logs, and the consolidated master file (`final_sales_dataset.csv`) directly into the `data/processed/` and `reports/` directories with a single script execution.

## Project Deliverables Checklist

1. Raw datasets stored unchanged (`data/raw/`)
2. Clean customer dataset (`data/processed/clean_customers.csv`)
3. Clean product dataset (`data/processed/clean_products.csv`)
4. Clean order dataset (`data/processed/clean_orders.csv`)
5. Final joined sales dataset (`data/processed/final_sales_dataset.csv`)
6. Reusable Python cleaning pipeline (`src/build_pipeline.py`)
7. Jupyter Notebook for exploration (`notebooks/day2_exploration.ipynb`)
8. Data dictionary (`reports/data_dictionary.csv`)
9. Schema-validation script (`src/validate_data.py`)
10. SQL quality-check file (`sql/quality_checks.sql`)
11. Duplicate-record report (`reports/duplicate_records.csv`)
12. Rejected-records file (`data/processed/rejected_records.csv`)
13. Data-quality report (`reports/data_quality_report.csv`)
14. Comprehensive README file
15. Presentation readiness (5-minute demonstration guide)

---

## Pipeline Execution Command

To run the entire end-to-end data cleaning and processing pipeline, execute:
bash
python src/build_pipeline.py
Final Reflection Answers
Which issue had the greatest effect on business reporting?

Missing customer IDs and unmatched foreign keys had the greatest impact because they caused records to drop or misalign during relational joins, directly distorting total net sales calculations.

Which records should not be automatically corrected?

Records with ambiguous financial values (such as conflicting quantities and unit prices) or mutated critical identifiers should never be automatically guessed or overwritten to avoid introducing false data into financial models.

When is deleting a duplicate record dangerous?

Deleting duplicates is dangerous when records share the same primary key (e.g., order_id) but represent distinct split-shipments, concurrent transactions, or legitimate multi-item orders processed at the exact same timestamp.

Why should raw data remain unchanged?

Raw data must remain untouched to serve as an immutable source of truth, ensuring reproducibility, audit compliance, and the ability to re-run or debug pipeline transformations from scratch.

How can schema validation prevent future problems?

Schema validation acts as an automated quality gate that catches data type drift, range violations, and missing primary keys before corrupted data propagates into downstream reporting tools or databases.

What could happen if a join creates duplicate records?

Uncontrolled cartesian products or many-to-many join inflation can artificially multiply row counts, leading to severely inflated sales totals and flawed business metrics.

Which cleaning rules should be confirmed by a business expert?

Rules regarding high-value thresholds, acceptable discount caps, categorization logic for unmapped products, and criteria for rejecting vs. retaining orphan records require domain-expert validation.

How would you schedule this pipeline in a real company?

In a production environment, this pipeline would be orchestrated using tools like Apache Airflow, Prefect, or Cron jobs to run automatically on a scheduled daily or hourly frequency.

Which quality checks should run daily?

Daily checks must include primary key uniqueness, null-value audits on crucial foreign keys, row count anomaly tracking, and schema contract verifications.

What would you improve in the next version of the pipeline?

Future enhancements will include automated logging (logging module), dynamic YAML-based configuration settings, unit tests using pytest, and an interactive HTML data-quality reporting dashboard.
