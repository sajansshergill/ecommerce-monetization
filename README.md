# Revenue, Pricing &amp; Customer Segmentation Analysis

## 📌 Business Context
E-commerce businesses generate massive volumes of transactional data — but revenue does not grow automatically.

Leaders constantly ask:
Who are our most valuable customers, and where are we losing money?

This project answers that question using real-world transaction data, applying customer segmentation, revenue analysis, and executive-level storytelling to surface actionable insights.


## 🎯 Business Problem
### Primary Question
Whare our most valuable customers, and where is revenue leaking across customers, regions, and transactions?

### Secondary Questions
- Which customer segments drive the majority of revenue?
- How concentrated is revenue among top customers?
- Where do refunds, cancellations, or negative quantities reduce revenue?
- Which countries and customer cohorts should be prioritized?

---

Dataset: Online Retail II (UCI / Kaggle)
Source: https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci
This dataset contains real transactional data from a UK-based online retailer.

Key Columns 

| Column        | Description                |
| ------------- | -------------------------- |
| `InvoiceNo`   | Unique invoice identifier  |
| `CustomerID`  | Unique customer identifier |
| `InvoiceDate` | Transaction timestamp      |
| `Quantity`    | Number of units purchased  |
| `UnitPrice`   | Price per unit             |
| `Country`     | Customer country           |

📌 Size: 500K+ transaction rows
📌 Grain: One row per invoice line item
This dataset closely mirrors real monetization and revenue analytics work.


## 🧠 Analytical Framework
1. RFM Customer Segmentation (Core)
Customers are segmented using RFM analysis:
- **Recency**: How recently a customer purchased
- **Frequency:** How often a customer purchases
- **Monetary:** How much revenue the customer generates

This enable identification of:
- High-value customers
- At-risk customers
- Low-value / one-time buyers


 2. Revenue & Monetization Analysis
Key analyses include:
- Revenue concentration by customer
- Revenue by country
- High-value vs low-value customer comparison
- Order value distribution
- Negative quantity / refund impace (revenue leakage)

3. Lifetime Value (LTV) Estimation
Approximate customer LTV is calcualted using:
- Historical purchase behavior
- Segment-level revenue contribution

This supports **investment** and **retention decisions**.


## 📐 Metrics & Dimensions

### Metrics
- Total Revenue
- Average Order Value (AOV)
- Purchase Frequency
- Customer Lifetime Value (LTV)
- Revenue Leakage (refunds / cancellations)

### Dimensions
- Customer Segment (RFM)
- Country
- Time (month, year)
- Customer tenure

### 🛠️ Tech Stack
| Tool                   | Usage                                 |
| ---------------------- | ------------------------------------- |
| **SQL**                | Joins, aggregations, window functions |
| **Python**             | Pandas, RFM segmentation, analysis    |
| **Excel**              | Data validation & reconciliation      |
| **Tableau / Power BI** | Revenue dashboards                    |


### 📁 Project Structure
<img width="878" height="610" alt="image" src="https://github.com/user-attachments/assets/84c86e00-f688-41b4-9ae4-2e8ebf44b4ab" />


### 📈 Key Deliverables
- ✅ RFM customer segments
- ✅ Revenue & monetization dashboard
- ✅ Revenue leakage analysis
- ✅ LTV by customer segment
- ✅ Executive-level business narrative

### 🧾 Executive Summary (Example)
A small percentage of customers drive a disproportionate share of revenue.
By prioritizing high-RFM customers and reducing refund-related leakage, the business can significantly improve revenue efficiency without increasing acquisition spend.

### 💼 Skills Demonstrated
- Business problem framing
- SQL analytics (real-world queries)
- Customer segmentation
- Revenue & monetization analysis
- Stakeholder-focused storytelling
- Dashboarding & reporting
