import pandas as pd

df_static = pd.read_json("crawldata/output.json")
df_dynamic = pd.read_json("Generative_AI/enrich_data_final.json")

df_static = df_static.rename(columns={
    "ProductID": "product_id",
    "ProductName": "product_name",
    "Price": "product_price",
    "Category": "category",
    "Dimensions": "dimensions",
    "ProductURL": "product_url"
})

df_static['product_price'] = df_static['product_price'].astype(str).str.replace(',', '').astype(float)


if df_dynamic['product_price'].dtype == object:
    df_dynamic['product_price'] = df_dynamic['product_price'].astype(str).str.replace(',', '').astype(float)

df_dynamic_subset = df_dynamic[['product_id', 'generated_review', 'rating', 'sentiment']]

final_merged_df = pd.merge(
    df_static,
    df_dynamic_subset,
    on="product_id",
    how="left"
)

final_merged_df.to_csv("Final_Data.csv", index=False, encoding="utf-8-sig")