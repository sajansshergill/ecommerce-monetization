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

---

🧠 Analytical Framework
1. RFM Customer Segmentation (Core)
Customers are segmented using RFM analysis:
- **Recency**: How recently a customer purchased
- **Frequency:** How often a customer purchases
- **Monetary:** How much revenue the customer generates

This enable identification of:
- High-value customers
- At-risk customers
- Low-value / one-time buyers

---

