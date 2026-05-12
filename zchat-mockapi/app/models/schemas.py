from pydantic import BaseModel


"""
InitRequest - מודל הבקשה ל-endpoint /init
מייצג את ה-body של הבקשה הנשלחת מהלקוח לאיתחול המשתמש.
כל השדות אופציונליים - הלקוח יכול לשלוח רק חלק מהם.
"""
class InitRequest(BaseModel):
    unit: str | None = None         # שם היחידה שאליה שייך המשתמש. None אם לא רלוונטי
    reality: str | None = None      # הסביבה/מציאות שבה המשתמש פועל (למשל "production", "training")
    module: str | None = None       # המודול הנוכחי באפליקציה שהמשתמש עובד בו
    role: str | None = None         # תפקיד המשתמש במערכת (למשל "operator", "admin")
    plan: str | None = None         # התוכנית/משימה שהמשתמש עובד עליה
    case: str | None = None         # המקרה/תרחיש הספציפי בתוך התוכנית


"""
ChatRequest - מודל הבקשה ל-endpoint /chat
מייצג את ה-body של בקשת השליחה של הודעה. כולל את ההודעה עצמה,
מזהה הסשן, ושדות הקשר עסקי לעדכון או override על המידע מ-init.
"""
class ChatRequest(BaseModel):
    message: str                              # תוכן ההודעה שהמשתמש שלח. שדה חובה
    session_id: str | None = None             # מזהה השיחה. None בהודעה הראשונה (השרת ייצור אחד חדש)
    unit: str | None = None                   # יחידת המשתמש (override של מה שנשלח ב-init)
    reality: str | None = None                # הסביבה (override של init)
    module: str | None = None                 # המודול הנוכחי (override של init)
    role: str | None = None                   # התפקיד (override של init)
    plan: str | None = None                   # התוכנית הנוכחית (override של init)
    case: str | None = None                   # המקרה הספציפי (override של init)


"""
Entity - מודל של ישות גיאוגרפית
מייצג אובייקט בודד במערכת ה-GIS/מפות. נשלח כחלק מתגובת השרת
כדי שהלקוח יוכל לצייר את הישות על המפה.
"""
class Entity(BaseModel):
    layer: str | None = None        # שם השכבה שהישות שייכת אליה (למשל "כבישים", "בניינים")
    entity_id: str | None = None    # מזהה ייחודי של הישות במערכת המקור
    geometry: str | None = None     # הצורה הגיאומטרית במחרוזת WKT (פירוט מלא בתיעוד למטה)
    """
    WKT geometry string using lat/lon (WGS84) coordinates.
    Coordinate order: latitude longitude (e.g. POINT (32.0853 34.7818))
    Supported types: POINT, LINESTRING, POLYGON

    מחרוזת גיאומטריה בפורמט WKT (Well-Known Text) עם קואורדינטות WGS84 (GPS).
    סדר הקואורדינטות: latitude (קו רוחב) ואז longitude (קו אורך).
    דוגמה לתל אביב: POINT (32.0853 34.7818)
    סוגים נתמכים:
        - POINT - נקודה בודדת
        - LINESTRING - קו בין כמה נקודות
        - POLYGON - מצולע (חייב להיסגר - הנקודה הראשונה והאחרונה זהות)
    """


"""
ChatResponse - מודל התגובה מ-endpoint /chat
מייצג את ה-body של התגובה שהשרת שולח חזרה ללקוח.
כולל את תשובת ה-AI, מזהה הסשן (לשימוש בהמשך), דגלי הבהרה,
chain of thought, ורשימת ישויות גיאוגרפיות לציור על המפה.
"""
class ChatResponse(BaseModel):
    response: str                           # הטקסט של תשובת ה-AI שיוצג למשתמש. שדה חובה
    session_id: str                         # מזהה השיחה - הלקוח ישלח אותו בבקשה הבאה. שדה חובה
    needs_clarification: bool               # האם ה-AI צריך הבהרה מהמשתמש לפני שיוכל להמשיך
    clarify_for: str | None = None          # אם נדרשת הבהרה - הנושא/השדה שצריך להבהיר
    reasoning_content: str | None = None    # תוכן חשיבה פנימית של המודל (chain of thought) לדיבוג/הצגה
    entities: list[Entity] = []             # מערך ישויות שזוהו/הופקו. ברירת מחדל רשימה ריקה (לא None)