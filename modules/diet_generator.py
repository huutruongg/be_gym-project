import os
import google.generativeai as genai

def generate_diet_plan(gender, age, height, weight, intensity, goal, level, expected, tdee, calories):
    # Access the API key from the environment variable
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 4096,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config
    )
    chat_session = model.start_chat(
        history=[
        ]
    )
    # Write prompt to sennd to gemini
    prompt = f"Tôi là {gender}, {age} tuổi, cao {height} cm và nặng {weight} kg. Mức độ hoạt động thể dục của tôi là {intensity}. TDEE của tôi là {tdee} calo"
    if goal == 'tăng cân':
        prompt += f" và mục tiêu của tôi là {goal}."
    elif goal == 'duy trì':
        prompt += "."
    elif goal == 'giảm cân':
        prompt += f" và mục tiêu của tôi là {goal} với mức độ là {level}. Và cuối cùng, cụ thể cần khoảng bao nhiêu ngày để giảm từ {weight} xuống {expected} kg!"
    prompt += f" Hãy gợi ý cho tôi thực đơn chi tiết cho một ngày(dự phòng 2 đến 3 set thực đơn để chống ngán), với tổng lượng calo mỗi ngày khoảng {calories}, giàu dinh dưỡng và phù hợp với người Việt Nam. "
    print("Handling...")
    response = chat_session.send_message(prompt)
    prompt = ""
    text = response.text
    print(text)
    return text