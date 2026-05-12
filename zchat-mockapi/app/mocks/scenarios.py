from app.models.schemas import Entity   # מודל Pydantic של ישות גיאוגרפית

# Mock scenarios matched by keywords in the user message.
# Geometry uses WKT format with lat/lon (WGS84) coordinates.
# Coordinate order: latitude longitude (e.g. POINT (32.0853 34.7818))
#
# תרחישים מדומים שמתאימים לפי מילות מפתח בהודעת המשתמש.
# הגיאומטריה בפורמט WKT עם קואורדינטות WGS84.
# סדר קואורדינטות: latitude longitude (לא תקני - חשוב לתעד!)


"""
SCENARIOS - רשימה של תרחישים מדומים
כל תרחיש הוא dict עם: keywords (לחיפוש), response (טקסט Markdown),
entities (ישויות גיאוגרפיות). הסדר חשוב - התרחיש הראשון שמתאים יוחזר.
"""
SCENARIOS = [
    # תרחיש 1: שאלות מיקום של מטרה - מחזיר נקודה בודדת על המפה
    {
        "keywords": ["איפה", "מיקום"],                 # מילות מפתח לזיהוי הודעות מיקום
        "response": (                                   # התשובה ב-Markdown - הכוכביות = bold ברינדור בלקוח
            "מטרה X נמצאת בנקודה:\n"
            "**נ.צ:** 32.0853, 34.7818\n\n"
            "**סטטוס:** פעיל\n"
            "**סוג:** מטרה קרקעית"
        ),
        "entities": [                                   # ישות אחת - נקודה במרכז תל אביב
            Entity(
                layer="targets",                        # שכבת "מטרות" - הלקוח יצבע בצבע ייעודי
                entity_id="target-001",                 # מזהה ייחודי - נשתמש בו גם בתרחישים אחרים על אותה ישות
                geometry="POINT (32.0853 34.7818)",     # WKT POINT - נקודה בודדת
            )
        ],
    },

    # תרחיש 2: כוחות לפי קרבה - מחזיר 3 נקודות על המפה
    {
        "keywords": ["קרוב", "קרובים", "ליד"],         # 3 וריאציות של אותה כוונה
        "response": (
            "כוחות לפי קרבה למטרה X:\n\n"
            "1. **כוח א** — מרחק 300 מטר\n"
            "2. **כוח ב** — מרחק 450 מטר\n"
            "3. **כוח ג** — מרחק 700 מטר"
        ),
        "entities": [                                   # 3 ישויות באותה שכבה - יוצגו עם אותו צבע
            Entity(layer="forces", entity_id="force-001", geometry="POINT (32.0880 34.7830)"),
            Entity(layer="forces", entity_id="force-002", geometry="POINT (32.0865 34.7800)"),
            Entity(layer="forces", entity_id="force-003", geometry="POINT (32.0820 34.7850)"),
        ],
    },

    # תרחיש 3: רשימת כוחות בגזרה - אותם 3 כוחות אבל עם תיאור שונה
    {
        "keywords": ["רשימה", "כוחות", "גזרה"],
        "response": (
            "כוחות בגזרה:\n\n"
            "- **כוח א** — 32.0880, 34.7830\n"
            "- **כוח ב** — 32.0865, 34.7800\n"
            "- **כוח ג** — 32.0820, 34.7850"
        ),
        "entities": [                                   # אותן ישויות בדיוק כמו בתרחיש 2 - עקביות בין תרחישים
            Entity(layer="forces", entity_id="force-001", geometry="POINT (32.0880 34.7830)"),
            Entity(layer="forces", entity_id="force-002", geometry="POINT (32.0865 34.7800)"),
            Entity(layer="forces", entity_id="force-003", geometry="POINT (32.0820 34.7850)"),
        ],
    },

    # תרחיש 4: סטטוס מטרה - אותה מטרה כמו בתרחיש 1 (target-001) - עקביות
    {
        "keywords": ["סטטוס", "מצב"],
        "response": (
            "**סטטוס מטרה X:** פעיל\n\n"
            "**זמן עדכון אחרון:** 10:32\n"
            "**הערות:** ללא שינוי חריג"
        ),
        "entities": [
            Entity(layer="targets", entity_id="target-001", geometry="POINT (32.0853 34.7818)")
        ],
    },

    # תרחיש 5: מנחת נחיתה - מחזיר 2 מנחתים (מומלץ + חלופה)
    {
        "keywords": ["מנחת", "נחיתה"],
        "response": (
            "**המנחת המומלץ:** מנחת אלפא — מרחק 1.2 ק״מ\n\n"
            "**התאמה:**\n"
            "- פעילות: יום ולילה\n"
            "- סטטוס: פעיל\n"
            "- סוג כלי: מסוקים\n\n"
            "**חלופות:**\n"
            "- מנחת בראבו — 2.5 ק״מ (יום בלבד)"
        ),
        "entities": [                                   # שכבה ייחודית למנחתים
            Entity(layer="landing-pads", entity_id="pad-alpha", geometry="POINT (32.0910 34.7750)"),
            Entity(layer="landing-pads", entity_id="pad-bravo", geometry="POINT (32.0950 34.7700)"),
        ],
    },

    # תרחיש 6: אזור פוליגון - מצולע על המפה
    {
        "keywords": ["אזור", "פוליגון", "גבול"],
        "response": "האזור המבוקש מסומן על גבי המפה.",
        "entities": [
            Entity(
                layer="areas",
                entity_id="area-001",
                # POLYGON עם סוגריים כפולים: חיצוני = הפוליגון, פנימי = הגבול שלו
                # 5 נקודות (4 פינות + סגירה) = מלבן. הנקודה הראשונה והאחרונה חייבות להיות זהות
                geometry=(
                    "POLYGON ("
                    "(32.0800 34.7700, "      # פינה 1 (התחלה)
                    "32.0900 34.7700, "       # פינה 2
                    "32.0900 34.7850, "       # פינה 3
                    "32.0800 34.7850, "       # פינה 4
                    "32.0800 34.7700)"        # סגירה - חזרה לפינה 1
                    ")"
                ),
            )
        ],
    },

    # תרחיש 7: מסלול - קו שובר על המפה (בניגוד לפוליגון, לא חייב להיסגר)
    {
        "keywords": ["מסלול", "דרך", "קו"],
        "response": "המסלול המבוקש מסומן על גבי המפה.",
        "entities": [
            Entity(
                layer="routes",
                entity_id="route-001",
                # LINESTRING - 3 נקודות = 2 מקטעים. סוגריים בודדים
                geometry=(
                    "LINESTRING "
                    "(32.0800 34.7700, "      # נקודת התחלה
                    "32.0850 34.7750, "       # נקודת ביניים
                    "32.0900 34.7820)"        # נקודת סיום (לא חוזרת להתחלה!)
                ),
            )
        ],
    },
]


"""
DEFAULT_SCENARIO - תרחיש ברירת מחדל
מוחזר אם אף מילת מפתח לא תואמת. תגובה גנרית עם ישות placeholder
כדי שהמערכת לא תקרוס ותחזיר תמיד מבנה תקין.
"""
DEFAULT_SCENARIO = {
    "response": "This is a mock response.",                 # תגובה גנרית באנגלית - placeholder לפיתוח
    "needs_clarification": False,                            # לא נדרשת הבהרה
    "entities": [
        Entity(layer="mock-layer", entity_id="mock-entity-1", geometry="POINT (32.0853 34.7818)")
    ],
}


"""
match_scenario - מתאימה תרחיש להודעה לפי מילות מפתח
עוברת על SCENARIOS בסדר שלהם, ומחזירה את הראשון שמכיל לפחות מילת מפתח אחת
שמופיעה בהודעת המשתמש. אם אף תרחיש לא מתאים - מחזירה את DEFAULT_SCENARIO.

@param message - הודעת המשתמש לבדיקה
@returns dict - התרחיש המתאים (כולל response, entities וכו')
"""
def match_scenario(message: str) -> dict:
    for scenario in SCENARIOS:                                                  # עובר על כל התרחישים בסדר ההגדרה
        # any() = True אם לפחות אחת ממילות המפתח נמצאת איפשהו בהודעה
        # keyword in message = בדיקת תת-מחרוזת (לא רגישה למיקום, רגישה לאותיות)
        if any(keyword in message for keyword in scenario["keywords"]):
            return scenario                                                      # מחזיר את התרחיש הראשון שמתאים ויוצא מהלולאה
    return DEFAULT_SCENARIO                                                      # אם הלולאה הסתיימה - אף תרחיש לא התאים, מחזיר ברירת מחדל
