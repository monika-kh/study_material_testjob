from django.conf import settings
import openai
import pdfplumber

openai.api_key = settings.OPEN_AI_API_KEY


def count_pdf_pages(pdf_file):
    try:
        with pdfplumber.open(pdf_file) as pdf:
            num_pages = len(pdf.pages)
            return num_pages
    except Exception as e:
        print(f"Error counting pages: {e}")
        return None


def get_summary(pdf_file, pages):
    token = 4096 / pages

    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        generated_text = ""

        for page in pdf.pages:
            text = page.extract_text()

            if len(text) >= token:
                text = text[: int(token)]
                generated_text += text
            else:
                generated_text += text

        generated_text = generated_text[1:4096]
        summarized_text = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Summarize the following text: {generated_text}",
            max_tokens=3050,
        )
        summary = summarized_text.choices[0].text.replace("\n", " ")
        return summary


def generate_system_design(summary):
    summary = summary[1:4096]
    system_design = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"create system desing for following text: {summary}",
        max_tokens=3500,
    )
    system_design_text = system_design.choices[0].text.replace("\n", " ")

    return system_design_text


def generate_questions(summary):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Create choice based question for {summary}",
        max_tokens=100,
        n=2,
    )
    questions = [choice["text"] for choice in response.choices]
    formatted_questions = []
    for i, question in enumerate(questions, start=1):
        question_text = question.replace("\n\n", "").replace("\n", " ").split("?")
        options = ""
        if "Answer" in question_text[1]:
            options = question_text[1].split("Answer")[0]
            if "2)" in options:
                options = options.split("2)")[0]
        elif "2)" in question_text[1]:
            options = question_text[1].split("2)")[0]
        else:
            options = question_text[1]

        ques_data = {"ques": question_text[0], "options": options}

        formatted_questions.append(ques_data)
    return formatted_questions


def get_image(summary):
    summary = summary[1:500]
    response = openai.Image.create(
        prompt=f" generate image for following text: {summary}", n=1, size="1024x1024"
    )

    image_url = response["data"][0]["url"]
    return image_url


def generate_application(summary):
    summary = summary[1:1000]
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Create a high-level application architecture for the following summary:\n{summary}",
        max_tokens=150,
        api_key=settings.OPEN_AI_API_KEY,
    )

    text = response.choices[0].text.replace("\n\n", "")
    return text
