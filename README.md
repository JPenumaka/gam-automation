"# GAM Automation MVP" 

# GAM Automation Scripts

This repository contains Python scripts to automate operations in **Google Ad Manager (GAM)**, such as:

- 🔄 Creating orders
- 📦 Bulk-creating line items with custom CPM pricing
- 🧠 Managing advertiser and trafficker IDs programmatically

---

## 🔧 Features

- Uses the **Google Ads API** (Ad Manager)
- Supports **bulk creation of 10+ line items**
- Customizable **CPM pricing per line item**
- Built-in support for **time zone handling** and **goal-based delivery**

---

## 🚀 Setup Instructions

1. **Clone this repo**
   ```bash
   git clone https://github.com/JPenumaka/gam-automation.git
   cd gam-automation


### 🔐 Google Ads API Setup

1. Copy `googleads_template.yaml` to `googleads.yaml`
2. Replace placeholders with your actual credentials:
   - `network_code`
   - `developer_token`
   - `service_account_email`
   - `path_to_private_key_file`
3. Ensure `googleads.yaml` is never committed — it's ignored via `.gitignore`
