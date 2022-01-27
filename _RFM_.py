# understanding and preparing data
import datetime as dt
import pandas as pd
df1 = pd.read_excel("C:/Users/hp/PycharmProjects/pythonProject2/online_retail_II.xlsx", sheet_name= "Year 2010-2011")
df=df1.copy()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df1.describe([0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]).T
df1.isnull().sum()
df1.dropna(inplace=True)
df1.nunique()
df["Description"].value_counts().sort_values(ascending=True)
df.groupby("Description").agg({"Quantity":"sum"}).sort_values("Quantity", ascending=False)
df1 = df1[~df1["Invoice"].str.contains("C",na=False)]
df1["TotalPrice"] = df1["Quantity"] * df1["Price"]
df1.head()
#Calculation of RFM metrics
import datetime as dt
df1["InvoiceDate"].max()


today_date = dt.datetime(2010, 12, 11)


rfm = df1.groupby('Customer ID').agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                     'Invoice': lambda Invoice: Invoice.nunique(),
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

rfm.head()

rfm.columns = ['recency', 'frequency', 'monetary']
rfm = rfm[(rfm['monetary'] > 0)& (rfm["Frequency"] > 0]

# Calculating RFM Scores
rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])

rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

rfm.head()

#segmentation
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
rfm.head()

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

rfm[rfm["segment"] == "potential_loyalists"].head()

rfm[rfm["segment"] == "at_Risk"].index

new_df = pd.DataFrame()
new_df["at_Risk_id"] = rfm[rfm["segment"] == "at_Risk"].index
new_df.to_csv("at_Risk.csv")
