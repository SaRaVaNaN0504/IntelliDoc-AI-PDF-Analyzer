import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables and configure the API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# MODIFIED: Use a single model for both tasks
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def summarize_text(pdf_context, summary_type):
    """
    Generates a summary for the given text using the Gemini model.
    This is now a single, efficient API call.
    """
    prompt_map = {
        "Concise": "Generate a concise, easy-to-read summary of the following document, focusing on the main purpose and key findings.",
        "Detailed": "Provide a detailed, section-by-section summary of the following document. Use markdown headings for each section.",
        "Bullet Points": "Extract the most important findings, conclusions, and action items from the following document as a clear, concise bulleted list."
    }
    prompt = f"{prompt_map[summary_type]}\n\nHere is the document text:\n---\n{pdf_context}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during summarization: {e}"

def ask_question(pdf_context, user_question):
    """
    Answers a user's question based on the provided PDF text.
    CRITICAL FIX: The full PDF context is passed in for accurate answers.
    """
    prompt = f"""
    Based *only* on the document context provided below, answer the user's question.
    If the answer is not found in the document, say "The answer is not available in the provided document."

    CONTEXT:
    ---
    {pdf_context}
    ---

    QUESTION:
    "{user_question}"
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while answering the question: {e}"