import openai

# Устанавливаем ключ API OpenAI
neuro_client = openai.OpenAI(
    base_url='https://api.deepseek.com',  # Адрес вашего сервера
    api_key=''  # Ключ не требуется, но поле обязательно (можно указать любое значение)
)


def generate_ai_comment(meeting_title: str, meeting_text: str) -> str:
    openai_messages = [{"role": "system", "content": "Ты помощник в совете директоров."
                                                     "Твоя задача дать свой экспертный комментраий по поводу повесткий собрания."
                                                     "Не используй форматирование текста."},
                       {"role": "user", "content": f"Заголовок: {meeting_title}\nПовестка: {meeting_text}"}]

    response = neuro_client.chat.completions.create(
        model='deepseek-chat',  # Название модели, загруженной в LM Studio
        messages=openai_messages,
        temperature=0.8,
        max_tokens=128
    )

    # Возвращаем сгенерированный комментарий
    return response.choices[0].message.content
