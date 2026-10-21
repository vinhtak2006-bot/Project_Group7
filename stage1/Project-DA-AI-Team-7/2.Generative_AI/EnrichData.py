import json
import random
import re
import ollama

input_file = "2.Generative_AI/reviews_data.json"
output_file = "2.Generative_AI/enrich_data.json"

with open(input_file, "r", encoding="utf-8") as f:
    reviews_data = json.load(f)

sentiment_dict = {
    "5/5": "Positive",
    "4/5": "Positive",
    "3/5": "Neutral",
    "2/5": "Negative",
    "1/5": "Negative"
}

for i in range(len(reviews_data)):
    item = reviews_data[i]
    review_text = item.get("generated_review", "")

    rand_rating = random.choice(list(sentiment_dict.keys()))
    
    rand_sentiment = sentiment_dict[rand_rating]

    prompt = f"""Bạn là một khách hàng đang viết đánh giá sản phẩm nội thất bằng tiếng Việt. 
Hãy viết lại đoạn review gốc sau đây: "{review_text}"

Yêu cầu bắt buộc:
1. Sắc thái cảm xúc (Sentiment): **{rand_sentiment}** (Positive: khen/hài lòng, Neutral: bình thường, Negative: chê bai/phàn nàn).
2. Mức điểm đánh giá (Rating): **{rand_rating}**.
3. CHỈ viết nội dung bài đánh giá bằng tiếng Việt, TUYỆT ĐỐI KHÔNG kèm theo bất kỳ câu dẫn dắt tiếng Anh nào ở đầu hay cuối.
4. Ở dòng cuối cùng của phản hồi, bắt buộc phải hiển thị đúng cú pháp:
Rating: {rand_rating}
Sentiment: {rand_sentiment}"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}],
    )

    text = response["message"]["content"]
    item["generated_review"] = text

    rating = re.search(r"Rating:\s*([^\n]+)", text)
    sentiment = re.search(r"Sentiment:\s*([^\n]+)", text)

    item["rating"] = rating.group(1).strip() if rating else rand_rating
    item["sentiment"] = sentiment.group(1).strip() if sentiment else rand_sentiment

    print(f"Đã xử lý xong sản phẩm {i+1} -> {item['rating']} | {item['sentiment']}")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(reviews_data, f, ensure_ascii=False, indent=4)
