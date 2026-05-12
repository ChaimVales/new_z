# מבנה קבצי הפרוייקט — Zchat

## שורש

- `HANDOFF.md` — מסמך מסירה כללי לפרוייקט: stack, הוראות הרצה, פירוט API, MapActions, שאלות פתוחות לאינטגרציה.

## Frontend — `zchat-mock-front/`

### תצורה ושורש
- `package.json` — תלויות והפקודות `dev`, `build`, `lint`, `preview`. כולל React, Radix, Tailwind, Vite.
- `package-lock.json` — נעילה אוטומטית של גרסאות החבילות. לא לערוך ידנית.
- `vite.config.ts` — תצורת Vite מינימלית עם `defineConfig` ו-plugin `react()`.
- `tsconfig.json` — תצורת TypeScript ראשית, מפנה לשני tsconfig-ים נפרדים.
- `tsconfig.app.json` — תצורת TypeScript לקוד הדפדפן (`src/`) עם DOM ו-`jsx: react-jsx`.
- `tsconfig.node.json` — תצורת TypeScript ל-`vite.config.ts` (קוד שרץ ב-Node).
- `tailwind.config.js` — סורק `index.html` ו-`src/**/*.{ts,tsx}` למחלקות Tailwind.
- `postcss.config.js` — מפעיל את ה-plugins `tailwindcss` ו-`autoprefixer`.
- `eslint.config.js` — חוקי ESLint עם plugins `react-hooks` ו-`react-refresh`.
- `.gitignore` — מתעלם מ-`node_modules`, `dist`, לוגים, קבצי IDE.
- `index.html` — דף ה-HTML הראשי, RTL+עברית, טוען את `main.tsx`.
- `README.md` — README ברירת מחדל של תבנית Vite (לא רלוונטי לפרוייקט).

### `public/`
- `public/vite.svg` — לוגו Vite, משמש כ-favicon.

### `src/` — שורש
- `src/main.tsx` — נקודת הכניסה של React. `createRoot().render(<StrictMode><App /></StrictMode>)`.
- `src/App.tsx` — קומפוננט ראשי. State: `messages`, `sessionId`, `isLoading`. פונקציות: `handleSend`, `useEffect` לקריאת `initUser`.
- `src/index.css` — מייבא `@tailwind` (base/components/utilities), reset גלובלי, `height: 100%` ל-html/body/root.
- `src/vite-env.d.ts` — שורה אחת `/// <reference types="vite/client" />`.

### `src/api/`
- `src/api/chat.ts` — תקשורת עם ה-Backend. קבועים: `BASE_URL`, `API_KEY`, `defaultHeaders`. פונקציות: `initUser()`, `sendMessage(message, sessionId)`.

### `src/types/`
- `src/types/index.ts` — שלושה interfaces: `Entity`, `ChatResponse`, `Message`.

### `src/mapActions/`
- `src/mapActions/index.ts` — interface `MapActions` עם `drawEntities`, `zoomToEntity`, `clearEntities` ומימוש דמה `defaultMapActions` (console.log).

### `src/contexts/`
- `src/contexts/MapActionsContext.tsx` — Context של React. מייצא `MapActionsProvider` ו-Hook `useMapActions()`.

### `src/components/Chat/`
- `src/components/Chat/ChatPanel.tsx` — קונטיינר עם כותרת "Zchat", `<MessageList>`, `<ChatInput>`. Layout `flex flex-col`.
- `src/components/Chat/MessageList.tsx` — רשימת ההודעות עם Radix `ScrollArea`, auto-scroll, מצב ריק, אינדיקציית טעינה.
- `src/components/Chat/MessageBubble.tsx` — בועת הודעה אחת. שונה למשתמש/בוט. כפתורי entities עם `onClick={() => mapActions.zoomToEntity(entity)}`.
- `src/components/Chat/ChatInput.tsx` — textarea + כפתור שליחה. State: `value`. פונקציות: `handleSend`, `handleKeyDown` (Enter שולח, Shift+Enter שובר שורה).

### `src/assets/`
- `src/assets/react.svg` — לוגו React מהתבנית, לא בשימוש.

## Backend — `zchat-mockapi/`

### שורש
- `requirements.txt` — תלויות Python: `fastapi`, `uvicorn[standard]`, `pydantic`.
- `run.py` — מפעיל את `uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)`.
- `.gitignore` — template סטנדרטי של Python (220 שורות).
- `README.md` — תיעוד ה-API: endpoints, headers, body, פורמט WKT, טבלת תרחישים.

### `app/`
- `app/__init__.py` — קובץ ריק שמסמן `app/` כ-package.
- `app/main.py` — יוצר `app = FastAPI()`, מוסיף CORS middleware (`allow_origins=["*"]`), מחבר `init.router` ו-`chat.router`.
- `app/store.py` — `user_contexts: dict[str, dict] = {}` — מאגר זיכרון בלבד.

### `app/models/`
- `app/models/__init__.py` — קובץ ריק.
- `app/models/schemas.py` — ארבעה מודלי Pydantic: `InitRequest`, `ChatRequest`, `Entity`, `ChatResponse`.

### `app/routers/`
- `app/routers/__init__.py` — קובץ ריק.
- `app/routers/init.py` — endpoint `POST /init`. פונקציה `init(body, api_key, user_personal_number)` שומרת ב-`user_contexts`.
- `app/routers/chat.py` — endpoint `POST /chat`. פונקציה `chat(...)` יוצרת `session_id` אם אין, קוראת ל-`match_scenario`, בונה `ChatResponse`.

### `app/mocks/`
- `app/mocks/__init__.py` — קובץ ריק.
- `app/mocks/scenarios.py` — `SCENARIOS` (7 תרחישים: מיקום/קרבה/רשימה/סטטוס/מנחתים/אזור/מסלול), `DEFAULT_SCENARIO`, פונקציה `match_scenario(message)`.
