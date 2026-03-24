import os
import yfinance as yf
from groq import Groq
from dotenv import load_dotenv

# 1. טעינת המפתחות הסודיים מקובץ ה-.env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# בדיקה שהמפתח קיים
if not api_key:
    print("❌ שגיאה: לא נמצא מפתח GROQ_API_KEY בקובץ ה-.env שלך!")
    exit()

# הגדרת הלקוח של Groq
client = Groq(api_key=api_key)

def get_stock_analysis(symbol):
    try:
        # 2. שליפת נתונים מהבורסה בעזרת yfinance
        print(f"🔍 מחלץ נתונים עבור {symbol}...")
        stock = yf.Ticker(symbol)
        
        # לוקחים היסטוריה של 5 ימים כדי לראות מגמה
        hist = stock.history(period="5d")
        if hist.empty:
            return "❌ לא נמצאו נתונים עבור הסימול הזה. וודא שהקלדת נכון (למשל NVDA)."

        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2]
        change_percent = ((current_price - prev_price) / prev_price) * 100
        stock_name = stock.info.get('longName', symbol)

        # 3. בניית ה"פרומפט" (השאלה) לבינה המלאכותית
        print(f"🧠 שולח לניתוח AI...")
        
        prompt = f"""
        נתח את המניה הבאה: {stock_name} ({symbol}).
        המחיר הנוכחי הוא ${current_price:.2f}.
        ביממה האחרונה המחיר השתנה ב- {change_percent:.2f}%.
        תמצת לי ב-2 משפטים בעברית:
        1. מה המשמעות של השינוי הזה?
        2. האם זו נראית כמו הזדמנות מעניינת או סיכון?
        """

        # 4. קריאה ל-AI (Groq)
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "אתה אנליסט בורסה בכיר שכותב בעברית קולעת ומקצועית."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        analysis = completion.choices[0].message.content
        return f"\n--- ניתוח מניית {stock_name} ---\n💰 מחיר: ${current_price:.2f}\n📈 שינוי יומי: {change_percent:.2f}%\n\n{analysis}"

    except Exception as e:
        return f"❌ קרתה שגיאה: {str(e)}"

# --- נקודת ההתחלה של התוכנית ---
if __name__ == "__main__":
    print("🚀 סוכן הבורסה של Gemini באוויר!")
    ticker = input("הכנס סימול מניה (למשל AAPL, TSLA, NVDA): ").upper()
    
    final_report = get_stock_analysis(ticker)
    print(final_report)
