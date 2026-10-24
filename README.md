# Ecommerce-Checkout-Analytics-Platform

This project looks at three common problems people run into when they try to buy something online, and checks if fixing them actually leads to more people finishing their purchase, using real statistics instead of guessing. Alongside the analysis, I also built an interactive Power BI dashboard to visualize the results, with completion and conversion rates by group, sample sizes, and chi-square significance for each test, plus a summary page comparing all three.

As an extension of this project, I also designed and built the relational database backend that a system like this would run on in production, along with a MongoDB store for unstructured data and a small Flask application layer connecting to it. The database actually stores the real results from the three A/B tests below, so the two halves of this project connect to each other, not just in writing. That part is covered further down in this README.

## What this project does

I picked three checkout problems that show up again and again in real online stores, and ran an A and B test on each one.

1. Ad vs PSA exposure (real data). Does showing users a real ad lead to more conversions than showing a neutral public service announcement. This uses a public Kaggle dataset with 588,101 users.
2. Guest checkout vs forced signup (simulated data). Does letting people check out without forcing them to make an account lead to more completed purchases.
3. Short checkout form vs long checkout form (simulated data). Does a shorter form with fewer fields lead to more completed purchases compared to a long form.

Test 1 uses real user data. Test 2 and test 3 use simulated data, since companies do not publish this kind of internal experiment publicly. The completion rates used for the simulation are grounded in real published checkout research, not random guesses. All sources are listed inside the notebook.

## Method

Every test in this project uses a chi square test, since the outcome in each case is a yes or no answer, meaning did the person convert or complete checkout, or not. A chi square test is the correct choice for comparing two groups on a yes or no outcome. For each test I set up a clear hypothesis, defined the two groups, picked one metric to measure, ran the test, and wrote out a plain recommendation at the end, either ship the change or run it longer.

## Results

| Test | Groups compared | Result | Recommendation |
|------|------------------|--------|-----------------|
| Test 1 (real data) | PSA vs ad exposure | statistically significant | ship the change |
| Test 2 (simulated) | forced signup vs guest checkout | statistically significant | ship the change |
| Test 3 (simulated) | long form vs short form | statistically significant | ship the change |

All three tests point in the same direction, a clearer, more flexible, and shorter checkout process leads to more people actually finishing their purchase.

## Tools used

Python, pandas, scipy, matplotlib, inside a Jupyter notebook.

## Files in this repo

- Checkout_Funnel_AB_Testing.ipynb — the full notebook, with all the code, explanations, charts, and results
- marketing_AB.csv — the real dataset used for test 1
- test1_chart.png — a saved chart from test 1
- test2_guest_checkout.csv — simulated dataset used for test 2
- test2_chart.png — a saved chart from test 2
- test3_form_length.csv — simulated dataset used for test 3
- test3_chart.png — a saved chart from test 3

## Database backend (extension):

- schema.sql — MySQL schema: 9 tables covering customers, products, categories, inventory, promotions, orders, order items, and reviews
- sample_data.sql — sample data to populate the schema
- triggers_procedures.sql — inventory triggers, stored procedures for revenue and customer lifetime value reporting, and a transaction/concurrency demo
- ab_test_results_addition.sql — a table holding the actual results from the three A/B tests above (real numbers, not placeholders), so the database and the         notebook are telling the same story.
- mongodb_setup.js — MongoDB collections for review text and clickstream data (the unstructured companion store)
- app.py — a small Flask application connecting to MySQL, with routes for low stock alerts, revenue by category, customer lifetime value, and the A/B test results
- ERR1.png — the EER diagram for the schema
- relational_algebra_queries.md — relational algebra expressions for the main queries, alongside their SQL equivalents


## Dashboard
![Dashboard preview](./dashboard_summary.png)
Interactive Power BI dashboard: [checkout_funnel_dashboard.pbix](./checkout_funnel_dashboard.pbix)

## Database backend extension

The A/B testing notebook and dashboard above analyze checkout conversion from the data side, looking at what happens once a checkout attempt is logged. This extension builds the actual database a system like this would run on: a normalized MySQL schema for customers, products, orders and inventory, triggers and stored procedures for automatic inventory management and revenue reporting, a MongoDB store for review text and clickstream logs that don't fit a fixed schema, and a Flask application layer that connects to MySQL and runs the stored procedures through a browser.



## About me

I am a graduate student at Northeastern University's Khoury College of Computer Science. I built this project to carry out A and B testing on some common issues faced by customers during the checkout process. I picked this topic because I have personally run into most of these problems myself while shopping online, and I wanted to see if there was real data behind why these small changes actually matter.

GitHub: [github.com/mohanaHarshita4](https://github.com/mohanaHarshita4)

LinkedIn: [linkedin.com/in/mohana-harshita](https://linkedin.com/in/mohana-harshita)
