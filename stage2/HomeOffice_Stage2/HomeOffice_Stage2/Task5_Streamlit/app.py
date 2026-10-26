
import pandas as pd
import streamlit as st
from joblib import load

st.set_page_config(page_title="HomeOffice Stage 2")
st.title("HomeOffice - Stage 2")
st.caption("Ứng dụng Streamlit cơ bản | Task 1, 2, 3, 4")

page = st.sidebar.selectbox(
    "Chọn chức năng",
    [
        "Tổng quan",
        "Task 1 - PCA",
        "Task 2 - KMeans",
        "Task 3 - Regression",
        "Task 4 - Classification"
    ]
)

df = pd.read_json("../clean_data.json")

if page == "Tổng quan":
    st.header("Tổng quan sản phẩm")
    st.write("Số sản phẩm:", len(df))
    st.write("Số danh mục:", df["category"].nunique())
    st.write("Giá trung bình:", f"{df['price_vnd'].mean():,.0f} VNĐ")
    st.bar_chart(df["category"].value_counts().head(10))
    st.dataframe(df[["product_id", "product_name", "category", "price_vnd"]])

elif page == "Task 1 - PCA":
    st.header("Task 1 - PCA")
    variance = pd.read_csv("artifacts/homeoffice_pca_variance_report.csv")
    transformed = pd.read_csv("artifacts/homeoffice_pca_transformed.csv")
    st.write("Số thành phần chính:", len([c for c in transformed.columns if c.startswith("PC")]))
    st.write("Phương sai giữ lại:", f"{variance['Explained Variance Ratio'].iloc[:len([c for c in transformed.columns if c.startswith('PC')])].sum():.2%}")
    st.dataframe(variance)
    st.line_chart(variance.set_index("Thành phần")["Cumulative Explained Variance"])
    if "PC2" in transformed:
        st.scatter_chart(transformed, x="PC1", y="PC2")

elif page == "Task 2 - KMeans":
    st.header("Task 2 - KMeans")
    clustered = pd.read_csv("artifacts/stage2_task2_clustered.csv")
    st.write("Số cụm K:", clustered["Cluster_Label"].nunique())
    summary = pd.read_csv("artifacts/stage2_task2_cluster_summary.csv")
    st.subheader("Thống kê các cụm KMeans")
    summary_display = summary.rename(columns={
        "Cluster_Label": "Cụm", "Ten_cum": "Tên cụm", "So_san_pham": "Số sản phẩm",
        "Gia_trung_binh": "Giá TB (VNĐ)", "Rating_trung_binh": "Rating TB",
        "Dai_trung_binh": "Dài TB (cm)", "Rong_trung_binh": "Rộng TB (cm)",
        "Cao_trung_binh": "Cao TB (cm)"
    })
    summary_display["Giá TB (VNĐ)"] = summary_display["Giá TB (VNĐ)"].map(lambda x: f"{x:,.0f}")
    st.dataframe(summary_display.round(2), hide_index=True, use_container_width=True)
    st.subheader("Sản phẩm theo cụm")
    cluster_names = dict(zip(summary["Cluster_Label"], summary["Ten_cum"]))
    cluster = st.selectbox(
        "Chọn cụm", sorted(clustered["Cluster_Label"].unique().tolist()),
        format_func=lambda k: f"Cụm {k} - {cluster_names.get(k, '')}"
    )
    filtered = clustered.loc[clustered["Cluster_Label"] == cluster,
        ["product_id", "product_name", "price_vnd", "Cluster_Label", "Cluster_Name"]].copy()
    filtered["price_vnd"] = filtered["price_vnd"].map(lambda x: f"{x:,.0f}")
    st.dataframe(filtered)

elif page == "Task 3 - Regression":
    st.header("Task 3 - Regression")
    metrics = pd.read_csv("artifacts/task3_metrics.csv", index_col=0)
    st.subheader("Kết quả hai mô hình")
    st.dataframe(metrics)
    model_name = st.selectbox("Chọn mô hình", ["LinearRegression", "DecisionTreeRegressor"])
    st.subheader("Dự đoán giá")
    rating = st.slider("Rating", 1, 5, 3)
    length = st.number_input("Chiều dài (cm)", min_value=1.0, value=140.0)
    width = st.number_input("Chiều rộng (cm)", min_value=1.0, value=70.0)
    height = st.number_input("Chiều cao (cm)", min_value=1.0, value=75.0)
    if st.button("Dự đoán"):
        # Dùng trực tiếp imputer, scaler và model đã fit trong Task 3.
        imputer = load("artifacts/task3_imputer.joblib")
        scaler = load("artifacts/task3_scaler.joblib")
        model = load(f"artifacts/task3_{model_name}.joblib")
        x = pd.DataFrame([[rating, length, width, height]],
                 columns=["rating_num", "length_cm", "width_cm", "height_cm"])
        if not hasattr(imputer, "_fill_dtype"):
            imputer._fill_dtype = imputer._fit_dtype
        x_scaled = scaler.transform(imputer.transform(x))
        predicted = model.predict(x_scaled)[0]
        st.success(f"Giá dự đoán: {max(0, predicted):,.0f} VNĐ")
    st.caption("Đây là giá ước lượng từ mô hình học máy, không phải giá bán thực tế.")

elif page == "Task 4 - Classification":
    st.header("Task 4 - Phân loại cảm xúc")
    st.write("Dự đoán cảm xúc Positive, Neutral hoặc Negative từ nội dung đánh giá sản phẩm.")
    st.subheader("So sánh mô hình")
    metrics = pd.read_csv("artifacts/task4_metrics.csv")
    st.dataframe(metrics)

    model_name = st.selectbox("Chọn mô hình phân loại", ["LogisticRegression", "DecisionTreeClassifier"])
    review = st.text_area("Nhập đánh giá sản phẩm", "Sản phẩm đẹp, chất lượng tốt, tôi rất hài lòng.")
    if st.button("Phân loại cảm xúc"):
        if not review.strip():
            st.warning("Vui lòng nhập nội dung đánh giá.")
        else:
            tfidf = load("artifacts/task4_tfidf.joblib")
            model = load(f"artifacts/task4_{model_name}.joblib")
            features = tfidf.transform([review])
            result = model.predict(features)[0]
            st.success(f"Cảm xúc dự đoán: {result}")
    st.caption("Mô hình dùng TF-IDF từ review; không dùng rating làm đặc trưng dự đoán.")
