import json
import ollama

input_file = "crawldata/output.json"
with open(input_file, "r", encoding="utf-8") as f:
    products = json.load(f)

reviews_data = []

for i in range(len(products)):
  product = products[i]
  name = product.get("ProductName", "Sản phẩm nội thất")
  price = product.get("Price", "Liên hệ")
  category = product.get("Category", "Nội thất văn phòng")

  prompt = (
        f"Viết một đoạn đánh giá chi tiết của khách hàng bằng tiếng Việt cho sản phẩm {name} thuộc danh mục {category} có giá {price} VNĐ. Đánh giá nên bao gồm trải nghiệm về chất lượng, thiết kế và độ hài lòng."
    )

  response = ollama.chat(
        model="llama3",
        messages=[{
            "role": "system",
            "content": (
                "Bạn là một khách hàng thực tế chuyên viết các bài đánh giá sản phẩm nội thất bằng tiếng Việt."
            ),
        }, {"role": "user", "content": prompt}],
    )

  raw_text = response["message"]["content"]

  reviews_data.append({
        "product_id": product.get("ProductID"),
        "product_name": name,
        "product_price": price,
        "generated_review": raw_text,
    })
  print(i)
output_file = "reviews_data.json"
with open(output_file, "w", encoding="utf-8") as f:       
  json.dump(reviews_data, f, ensure_ascii=False, indent=4)
