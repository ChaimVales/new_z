import uuid                                     # מודול סטנדרטי ליצירת מזהים ייחודיים אוניברסליים

from fastapi import APIRouter, Header

from app.mocks.scenarios import match_scenario   # פונקציה שמחזירה תרחישים מדומים לפי תוכן ההודעה (מחליף AI אמיתי בפיתוח)
from app.models.schemas import ChatRequest, ChatResponse   # מודלי Pydantic ל-input ו-output

router = APIRouter()


"""
chat - endpoint לטיפול בהודעות צ'אט מהמשתמש
מקבל הודעה, מייצר/משתמש במזהה סשן, מתאים תרחיש מדומה לפי ההודעה,
ובונה תגובה מובנית עם הטקסט, הישויות הגיאוגרפיות, ודגלי הבהרה.

response_model=ChatResponse מבטיח: ולידציה של התגובה, סינון שדות לא רצויים,
ותיעוד אוטומטי ב-Swagger.

@param body - אובייקט ChatRequest עם ההודעה ומזהה הסשן (אופציונלי)
@param api_key - מפתח API לאימות. מגיע מה-HTTP header 'api-key'
@param user_personal_number - מזהה המשתמש מ-header 'user-personal-number'
@returns ChatResponse - תגובת ה-AI, מזהה הסשן, וישויות גיאוגרפיות
"""
@router.post("/chat", response_model=ChatResponse)   # POST /chat, מחזיר 200 עם body מסוג ChatResponse
async def chat(
    body: ChatRequest,                          # body מסוג ChatRequest. FastAPI מאמת ומפרש את ה-JSON
    api_key: str = Header(...),                 # header חובה לאימות (כרגע לא נבדק - placeholder)
    user_personal_number: str = Header(...),    # מזהה המשתמש (כרגע לא משמש - placeholder לטעינת context)
) -> ChatResponse:
    # אם הלקוח לא שלח session_id (הודעה ראשונה) - יוצרים UUID חדש.
    # אחרת משתמשים במזהה שהלקוח שלח (כדי לשמור על המשך השיחה)
    session_id = body.session_id or str(uuid.uuid4())

    # מתאים תרחיש מדומה לפי תוכן ההודעה (placeholder ל-AI אמיתי)
    scenario = match_scenario(body.message)

    # בונה את התגובה. שימוש ב-[] לשדות חובה ו-.get() לאופציונליים
    return ChatResponse(
        response=scenario["response"],                                          # טקסט התשובה - שדה חובה בתרחיש
        session_id=session_id,                                                  # מזהה השיחה (חדש או קיים)
        needs_clarification=scenario.get("needs_clarification", False),         # אופציונלי, ברירת מחדל False
        clarify_for=scenario.get("clarify_for"),                                # אופציונלי, ברירת מחדל None
        reasoning_content=None,                                                 # אין chain of thought במצב mock
        entities=scenario["entities"],                                          # ישויות גיאוגרפיות - שדה חובה בתרחיש
    )