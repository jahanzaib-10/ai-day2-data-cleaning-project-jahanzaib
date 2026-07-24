# AI Internship Day 02 - End-to-End Data Cleaning & EDA Pipeline Project

---

## 📌 Project Overview

This repository contains the solution and documentation for my AI Internship Day 2 project. In this project, I implemented an end-to-end data cleaning, integration, schema validation, and Exploratory Data Analysis (EDA) pipeline using Python, Pandas, NumPy, and SQL.

---

## 🚀 Learning Outcomes

- Learned how to write modular, reusable data-cleaning functions in Python.
- Implemented robust error handling and automated schema validation checks (`validate_schema`).
- Gained a solid understanding of relational dataset joining, missing-value treatment, and duplicate resolution strategies.
- Integrated NumPy for vectorized computations and conditional classifications (`np.select`).
- Performed relational SQL quality checks and business intelligence queries.

---

## 🗂️ Project Architecture & Folder Structure

To ensure a clean, modular, and maintainable project architecture, the following folder structure was implemented:

```text
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

```

## ⚠️ Important Rule

 Files inside the data/raw/ folder are treated as an immutable source of truth and must never be edited, modified, or overwritten directly.

## 💻 Environment Setup & Installation

**1. Open your project folder in VS Code.**

**2.Ensure that Python is installed on your system.**

**Open the terminal and run the following command to install dependencies:**

**Bash
python -m pip install -r requirements.txt**

## 🏃‍♂️ Running the Project

To run the exploratory data analysis notebook, open notebooks/EDA_Ecommerce_Analysis.ipynb in VS Code or Jupyter Notebook.
📊 Key Tasks Performed

## 1. Descriptive Statistics

Calculated mean, median, min, max, and standard deviation for key customer features to understand central tendencies and spreads.

## 2. Data Distribution

Generated histograms and box plots to check data spread, skewness, and normality across numerical features.
3. Sampling & Splitting Strategy
Designed a robust dataset partition strategy consisting of a 70% training set, a 15% validation set, and a 15% testing split.

## 4. Correlation Analysis

Created correlation matrices and heatmaps to examine linear relationships and dependencies between variables.

## ## 5. Outlier Detection

Identified unusual customer records and extreme data points using the Interquartile Range (IQR) method.

## 6. Target Analysis

Evaluated class distributions and imbalances across customer value tiers to prepare targets for classification models.

## 7. Leakage Detection

Identified features that risk leaking future or target information prematurely into the training process.

## 8. Visualizations & Management Insights

Summarized key statistical findings and actionable business recommendations into a professional management report (reports/management_summary.md).

## 📋 Project Deliverables Checklist

**[x] Immutable raw e-commerce dataset (data/raw/)**

**[x] Exploratory Jupyter Notebook (notebooks/EDA_Ecommerce_Analysis.ipynb)**

**[x] Management summary report (reports/management_summary.md)**

**[x] Requirements configuration file (requirements.txt)**

**[x] Comprehensive README file (README.md)**

## 💡 Final Reflections & Answers

**Why is exploratory data analysis essential before machine learning modeling?**
 EDA uncovers hidden anomalies, data types, missing structures, and data leakage risks that would otherwise cause silent model failure or overoptimistic performance.

 **How does class imbalance affect model training?**
  Severe class imbalance can cause models to bias heavily towards the majority class, resulting in poor predictive performance on minority or high-value customer tiers.

**Why is data splitting important before feature scaling or encoding?**
 Splitting data prior to transformations prevents data leakage from the validation and test sets into the training pipeline.

**What is the primary danger of data leakage?**
 Data leakage introduces target information from the future or test space into training features, leading to unrealistically high training scores followed by poor generalization in production.

 **How does the IQR method handle outliers?**
  The IQR method flags data points that fall below Q1-1.5*IQR or above Q3+1.5*IQR, providing a robust measure against extreme skewness compared to standard deviation methods.

**Author Name: "Muhammad Jahanzaib Azhar"**  
**Date: July 21, 2026**
