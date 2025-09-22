import sqlite3
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
import re

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_KEY:
    raise ValueError("OpenAI API key not found")

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=OPENAI_KEY
)

DB_PATH = "lottery.db"

def ask_question(question: str) -> str:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()

            c.execute("SELECT answer FROM faq WHERE question LIKE ? LIMIT 1", (f"%{question}%",))
            result = c.fetchone()
            if result:
                return result[0]

            if "last draw" in question.lower() or "recent" in question.lower():
                c.execute("SELECT draw_date, numbers, jackpot_amount FROM winning_numbers ORDER BY draw_date DESC LIMIT 5")
                rows = c.fetchall()
                if not rows:
                    return "Sorry, I don’t have that information."
                response = "Recent lottery draws:\n"
                for date, numbers, jackpot in rows:
                    response += f"{date}: {numbers} (Jackpot: ${int(jackpot):,})\n"
                return response.strip()

            if "jackpot" in question.lower():
                c.execute("SELECT draw_date, jackpot_amount FROM winning_numbers ORDER BY draw_date DESC LIMIT 5")
                rows = c.fetchall()
                if not rows:
                    return "Sorry, I don’t have that information."
                response = "Recent jackpots:\n"
                for date, jackpot in rows:
                    response += f"{date}: ${int(jackpot):,}\n"
                return response.strip()

            date_match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', question)
            if date_match:
                draw_date = date_match.group(1)
                c.execute("SELECT numbers, jackpot_amount FROM winning_numbers WHERE draw_date = ?", (draw_date,))
                row = c.fetchone()
                if row:
                    numbers, jackpot = row
                    return f"Numbers for {draw_date}: {numbers} (Jackpot: ${int(jackpot):,})"
                else:
                    return "Sorry, I don’t have that information."
        prompt = (
            f"You are a helpful assistant for Ontario Lottery questions. "
            f"Only answer if you know the answer safely. "
            f"If you don't know, say 'Sorry, I don’t have that information.'\n\n"
            f"Question: {question}\nAnswer:"
        )
        return llm.predict(prompt).strip()

    except Exception as e:
        return f"Error: {e}"
