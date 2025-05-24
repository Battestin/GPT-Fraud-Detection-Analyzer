# GPT Fraud Detection Analyzer

Automated system for analyzing financial transactions using **GPT-4**, focused on identifying fraud and issuing technical recommendations.

## 🕵️‍♂️ What the script does

1. **Reads a CSV file** of financial transactions  
2. **Detects suspicious patterns** based on amount, location, and behavior  
3. **Generates justified opinions** for flagged transactions  
4. **Provides technical recommendations**: Notify Customer, Trigger Anti-Fraud Department, or Perform Manual Verification  

> ⚠️ Requires GPT-4 — simpler models like GPT-3.5 often fail to identify fraud properly.

## 📂 Expected CSV input format

Each row represents a transaction (id, type, amount, location, etc).

Example:  
```
id,type,merchant,time,amount,product_name,location
123,debit,Store A,10:43,R$9999,TV,Recife - PE (Brazil)
...
```

## 📄 Output format

- A JSON with enriched transaction data and fraud status (`"Approved"` or `"Possible Fraud"`)
- `.txt` files with tailored recommendations for each flagged transaction

## 🔁 Example flow

```bash
1. Starting transaction analysis
2. Generating opinion for transaction 123
3. Generating recommendations
✅ Output saved to: recomendation-123-TV-Possible Fraud.txt
```

## 🧠 Fraud signals considered

- Highly unusual transaction amounts
- Geographically inconsistent activity
- Rapid purchases of high-value items

## 📦 Requirements

- Python 3.10+
- `openai`, `python-dotenv`

## 🛡️ License

MIT
