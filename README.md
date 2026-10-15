# 📊 Practical problem

##  Calculator personal budget — level 2: quarterly report


## 1. 🎯 Educational goal

After implementation tasks student :

* knows how to work with ** several sets data * *;
* uses ** tabs ** and navigation in Streamlit ;
* again uses code ( functions );
* unites data (` pandas.concat` ) ;
* performs ** aggregation data * *;
* builds more complex tables and graphs ;
* generates structured CSV for further tasks .

---

## 2. 🧩 Scenario / context

You develop application for user who​ wants :

* to lead budget ** for each month separately * *;
* receive ** consolidated report by quarter * *;
* export results for further analysis .

Your task — to create comfortable interface for work with 3 months and automatic formation quarterly report .

---

## 3. ⚙️ Functional description

### 🔹 3.1 General structure application

Addition has contain :

### Sidebar ( left panel ) :

* switch :

* " Monthly data "
* " Quarterly report "

---

### 🔹 3.2 Tabs for months

If selected " Monthly data ":

Use :

```python
st.tabs ([" Month 1", " Month 2", " Month 3"])
```

For each month :

#### Input :

* income
* expenses ( same categories as in task 1 ) :

* Food
* Transportation
* Entertainment
* Housing / Utilities
* Other

#### Actions :

* " Calculate " button

#### Result :

* table expenses
* general costs
* balance
* status ( surplus / deficit )
* schedule

👉 ** IMPORTANT:* *
logic has be moved to a function ( for example : ` calculate_month_ budget ( )`)

---

### 🔹 3.3 Saving data on months

Data each month have to be stored :

👉 or in ` st.session _state `
👉 or in the dictionary

---

### 🔹 3.4 " Quarterly " tab report "

At choosing " Quarterly" report ":

Addition has :

#### 1. Merge data :

```python
pd.concat ([df_month1, df_month2, df_month3])
```

#### 2. Calculate :

* general income
* general costs
* balance

#### 3. Group expenses :

```python
df.groupby (" Category " ).sum ()
```

#### 4. Output :

* table ( by categories )
* general indicators
* schedule

---

#### 5. CSV Export

Button :

```
📥 Download quarterly report
```

---

## 4. 🧪 Technical requirements

* Python 3.10+
* Streamlit
* pandas
* without using third-party UI libraries

---

## 5. 📦 Required components Streamlit

The student MUST have use :

* ` st.sidebar `
* ` st.tabs `
* ` st.number _input `
* ` st.button`
* ` st.dataframe `
* ` st.bar_chart `
* ` st.download _button`
* ` st.session _state ` ⚠️ ( key element this level )

---

## 6. 📄 Requirements to CSV export

CSV has contain :

* all costs by quarter
* final lines

---

## 7. 📊 CSV format (REQUIRED)

File : `quarterly_budget.csv`

| Month | Category | Amount |
| -------- | --------- | ---- |
| Month 1 | Food | 3000 |
| Month 1 | Transport | 1000 |
| ... | ... | ... |
| Month 2 | Food | 3200 |
| ... | ... | ... |

---

### At the end file :

| Month | Category | Amount |
| ------ | --------- | ---- |
| TOTAL | INCOME | XXXX |
| TOTAL | EXPENSES | XXXX |
| TOTAL | BALANCE | XXXX |

---

## 8. 🚫 Limitation

* not duplicate code 3 times → use functions
* not save data to files under time works ( download only )
* interface has be readable
* mandatory to process situation :

* if data entered not for all months

---

## 9. 📁 Expected structure repository

```
budget-quarterly-report/
├ ─ ─ . github /
│ └── workflows/
│ └── ci.yml
├ ── streamlit_app.py
├ ── test_streamlit_app.py
├ ── requirements.txt
└── README.md
```

---

## 10. 📌 Requirements to files

### app.py

* main UI logic
* challenges functions

### utils.py ( optional , but preferably )

* functions :

* calculation budget
* aggregation

### README.md

* description tasks
* how launch

---

## 11. 🔁 Which knowledge used from the previous tasks

* ` st.number _input `
* ` st.button`
* ` st.dataframe `
* ` st.bar_chart `
* creation DataFrame
* basic calculation

---

## 12. 🆕 What new attached

* ` st.tabs `
* ` st.sidebar `
* ` st.session _state `
* association DataFrame (` concat` )
* grouping (` groupby `)
* working with multiple sets data
* repeated using code

---

## 13. ⚠️ Typical mistakes students

1. ❌ Copying code 3 times instead functions

2. ❌ Data " disappears " when switching tabs
→ not used ` session_state `

3. ❌ Wrong unite DataFrame
→ absent " Month " column

4. ❌ CSV without structures ( chaotic )

5. ❌ Quarterly report counts without checks data

---
## In this project use current Streamlit API .

❗ ** Prohibited use ` use_container_width `**
Instead this use :

```python
st.dataframe ( df , width="stretch")
```
