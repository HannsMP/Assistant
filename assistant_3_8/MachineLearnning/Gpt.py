import openai
from secrets import Api_Key

openai.api_key = Api_Key

response = openai.chat.completions.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {"role": "system", "content": "Eres un interprete que recibe palabras enlistadas por una entrada visual de lenguaje de señas, tu trabajo corregir y dar sentido a lo que dicen"},
        {"role": "user","content": "jona ne lamo jelnanda" }
    ]
)

print(response)