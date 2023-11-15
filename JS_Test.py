import os
import time
import json

import openai

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("ORGANIZATION")



def extract_sentiment_factors(review_text):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=f"리뷰: {review_text}\n\n긍정 요인:\n-",
      max_tokens=1000,
      n=1,
      stop=["부정 요인:", "End"]
    )
    positive_factors = response.choices[0].text.strip().split('\n')[1:]

    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=f"리뷰: {review_text}\n\n부정 요인:\n-",
      max_tokens=1000,
      n=1,
      stop=["긍정 요인:", "End"]
    )
    negative_factors = response.choices[0].text.strip().split('\n')[1:]

    return positive_factors, negative_factors

if __name__ == "__main__":
    # 리뷰 내용을 저장하는 리스트
    reviews = []
    file_names = ["data/review1.txt", "data/review2.txt", "data/review3.txt", "data/review4.txt", "data/review5.txt"]

    for file_name in file_names:
        with open(file_name, 'r', encoding='utf-8') as f:
            reviews.append(f.read().strip())

    positive_reviews = []
    negative_reviews = []

    for i, review in enumerate(reviews):
        pos, neg = extract_sentiment_factors(review)
        positive_reviews.append(f"review{i + 1}: {', '.join(pos)}")
        negative_reviews.append(f"review{i + 1}: {', '.join(neg)}")

    print("\033[92m긍정 내용:")
    for pos_review in positive_reviews:
        print(pos_review)
    print("\033[0m")

    print("\n" + "-"*50 + "\n")

    print("\033[91m부정 내용:")
    for neg_review in negative_reviews:
        print(neg_review)
    print("\033[0m")

    while True:
        user_input = input("\n질문이나 의견을 입력하세요 (종료하려면 'Q'를 입력): ").strip()
        if user_input.upper() == 'Q':
            break

        # 질문을 기반으로, 긍정/부정 요인과 함께 질문을 전달합니다.
        context = f"긍정 내용: {', '.join(positive_reviews)}\n부정 내용: {', '.join(negative_reviews)}\n사용자: {user_input}\nChatGPT: "
        
        response = openai.Completion.create(
          engine="text-davinci-003",
          prompt=context,
          max_tokens=500,
        )
        print(f"\nChatGPT: {response.choices[0].text.strip()}")
