import React, { useState, useRef, useEffect } from 'react';
import {
    Minus, Send, MessageSquare, X, Maximize2, Minimize2,
    PanelLeft, PanelRight, PanelTop, PanelBottom,
} from 'lucide-react';

type DockPosition = 'left' | 'right' | 'top' | 'bottom';

interface Message {
    id: number;
    text: string;
    sender: 'bot' | 'user';
}

interface ChatLayoutProps {
    children?: React.ReactNode;
}

// ערכי ברירת מחדל - אליהם חוזרים כשלוחצים X
const DEFAULT_POSITION: DockPosition = 'right';
const DEFAULT_SIZE = 30;
const INITIAL_MESSAGES: Message[] = [
    {
        id: 1,
        sender: 'bot',
        text: 'היי! המערכת מוכנה. אתה יכול לעגן אותי לכל צד מהכפתורים בכותרת.',
    },
];

const ChatLayout: React.FC<ChatLayoutProps> = ({ children }) => {
    const [position, setPosition] = useState<DockPosition>(DEFAULT_POSITION);
    const [size, setSize] = useState<number>(DEFAULT_SIZE);
    const [isMinimized, setIsMinimized] = useState<boolean>(false);
    const [isMaximized, setIsMaximized] = useState<boolean>(false);

    // סטייט של תוכן השיחה - נשמר במזעור, מתאפס בסגירה
    const [messages, setMessages] = useState<Message[]>(INITIAL_MESSAGES);
    const [inputText, setInputText] = useState<string>('');

    const isVertical = position === 'left' || position === 'right';
    const chatFirst = position === 'left' || position === 'top';

    const isResizing = useRef<boolean>(false);

    // ---------- שלוש פעולות שונות: סגור / מזער / שחזר ----------

    // X = סגור: מאפס את הכל - מיקום, גודל, הודעות, וקלט
    const handleClose = () => {
        setIsMinimized(true);
        setPosition(DEFAULT_POSITION);
        setSize(DEFAULT_SIZE);
        setIsMaximized(false);
        setMessages(INITIAL_MESSAGES);
        setInputText('');
    };

    // מזער: שומר את הכל בדיוק כפי שהיה - מיקום, גודל, הודעות, וטקסט בקלט
    const handleMinimize = () => {
        setIsMinimized(true);
    };

    // פתיחה מחדש - הסטייט כבר תקין (אם נסגר ב-X הוא אופס, אם מוזער הוא שמור)
    const handleRestore = () => {
        setIsMinimized(false);
    };

    // שליחת הודעה
    const handleSend = () => {
        const trimmed = inputText.trim();
        if (!trimmed) return;
        const newMsg: Message = {
            id: Date.now(),
            sender: 'user',
            text: trimmed,
        };
        setMessages((prev) => [...prev, newMsg]);
        setInputText('');
    };

    const handleInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    // ---------- שינוי גודל ----------
    const startResize = (e: React.MouseEvent) => {
        if (isMaximized) return;
        isResizing.current = true;
        document.body.style.cursor = isVertical ? 'ew-resize' : 'ns-resize';
        document.body.style.userSelect = 'none';
        e.preventDefault();
    };

    useEffect(() => {
        const handleMouseMove = (e: MouseEvent) => {
            if (!isResizing.current) return;

            let newSize: number;
            if (position === 'right') {
                newSize = ((window.innerWidth - e.clientX) / window.innerWidth) * 100;
            } else if (position === 'left') {
                newSize = (e.clientX / window.innerWidth) * 100;
            } else if (position === 'top') {
                newSize = (e.clientY / window.innerHeight) * 100;
            } else {
                newSize = ((window.innerHeight - e.clientY) / window.innerHeight) * 100;
            }
            setSize(Math.max(15, Math.min(85, newSize)));
        };

        const handleMouseUp = () => {
            isResizing.current = false;
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
        };

        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);
        return () => {
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
        };
    }, [position]);

    // ---------- מצב מזוער / סגור - הצ'אט מוצג רק כאייקון צף ----------
    if (isMinimized) {
        return (
            <div className="h-full w-full relative overflow-hidden">
                <div className="h-full w-full">{children}</div>
                <button
                    onClick={handleRestore}
                    className="absolute bottom-6 right-6 w-16 h-16 bg-blue-600 text-white rounded-full shadow-2xl flex items-center justify-center hover:scale-110 transition-all z-50 border-4 border-white"
                    title="פתח את הצ'אט"
                >
                    <MessageSquare size={28} />
                </button>
            </div>
        );
    }

    // ---------- חישוב גודל הצ'אט והמפה ----------
    // מגדירים את שניהם במפורש כדי שהסכום יהיה תמיד בדיוק 100% ולא יהיה כיסוי
    const effectiveSize = isMaximized ? 100 : size;
    const chatStyle: React.CSSProperties = isVertical
        ? { width: `${effectiveSize}%`, height: '100%' }
        : { width: '100%', height: `${effectiveSize}%` };
    const mapStyle: React.CSSProperties = isVertical
        ? { width: `${100 - effectiveSize}%`, height: '100%' }
        : { width: '100%', height: `${100 - effectiveSize}%` };

    // ---------- מיקום ידית שינוי הגודל ----------
    // אזור גרירה רחב (6px) על הגבול - שקוף לחלוטין, רק הסמן משתנה ל"גרירה"
    const resizeHandleClass = {
        left: 'right-0 top-0 bottom-0 w-1.5 cursor-ew-resize',
        right: 'left-0 top-0 bottom-0 w-1.5 cursor-ew-resize',
        top: 'bottom-0 left-0 right-0 h-1.5 cursor-ns-resize',
        bottom: 'top-0 left-0 right-0 h-1.5 cursor-ns-resize',
    }[position];

    // ---------- פאנל הצ'אט ----------
    // dir="rtl" כדי שהכותרת והודעות יוצגו נכון בעברית
    // (הלייאאוט החיצוני הוא LTR כדי שה-flex לא יתהפך)
    const ChatPanel = (
        <div
            dir="rtl"
            style={chatStyle}
            className="relative flex flex-col bg-white overflow-hidden flex-shrink-0"
        >
            {/* אזור גרירה - שקוף לחלוטין, רק הסמן משתנה */}
            {!isMaximized && (
                <div
                    onMouseDown={startResize}
                    className={`absolute z-30 ${resizeHandleClass}`}
                />
            )}

            {/* כותרת - דחוסה כדי להיכנס גם ברוחב 30% */}
            <div className="h-12 bg-slate-900 text-white flex items-center justify-between px-2 select-none border-b border-blue-400/30 flex-shrink-0 gap-1">
                {/* צד ימין: סטטוס + שם */}
                <div className="flex items-center gap-2 min-w-0">
                    <div className="w-2.5 h-2.5 bg-green-500 rounded-full flex-shrink-0" />
                    <span className="font-semibold text-sm truncate">סייען</span>
                </div>

                {/* אמצע: בורר מיקום - קומפקטי */}
                {!isMaximized && (
                    <div className="flex items-center gap-0.5 bg-slate-800 rounded p-0.5 flex-shrink-0">
                        <button
                            onClick={() => setPosition('left')}
                            className={`p-1 rounded ${position === 'left' ? 'bg-blue-600' : 'hover:bg-white/10'}`}
                            title="עגן שמאל"
                        >
                            <PanelLeft size={13} />
                        </button>
                        <button
                            onClick={() => setPosition('right')}
                            className={`p-1 rounded ${position === 'right' ? 'bg-blue-600' : 'hover:bg-white/10'}`}
                            title="עגן ימין"
                        >
                            <PanelRight size={13} />
                        </button>
                        <button
                            onClick={() => setPosition('top')}
                            className={`p-1 rounded ${position === 'top' ? 'bg-blue-600' : 'hover:bg-white/10'}`}
                            title="עגן למעלה"
                        >
                            <PanelTop size={13} />
                        </button>
                        <button
                            onClick={() => setPosition('bottom')}
                            className={`p-1 rounded ${position === 'bottom' ? 'bg-blue-600' : 'hover:bg-white/10'}`}
                            title="עגן למטה"
                        >
                            <PanelBottom size={13} />
                        </button>
                    </div>
                )}

                {/* צד שמאל: כפתורי חלון - קומפקטיים */}
                <div className="flex items-center gap-0.5 flex-shrink-0">
                    <button
                        onClick={handleMinimize}
                        className="p-1 hover:bg-white/10 rounded"
                        title="מזער (זוכר מיקום וגודל)"
                    >
                        <Minus size={15} />
                    </button>
                    <button
                        onClick={() => setIsMaximized(!isMaximized)}
                        className="p-1 hover:bg-white/10 rounded"
                        title={isMaximized ? 'שחזר גודל' : 'מסך מלא'}
                    >
                        {isMaximized ? <Minimize2 size={15} /> : <Maximize2 size={15} />}
                    </button>
                    <button
                        onClick={handleClose}
                        className="p-1 hover:bg-red-500 rounded"
                        title="סגור (איפוס תצוגה)"
                    >
                        <X size={15} />
                    </button>
                </div>
            </div>

            {/* תוכן הצ'אט - מציג את כל ההודעות מהסטייט */}
            <div className="flex-1 p-4 overflow-y-auto bg-slate-50/30 flex flex-col gap-3">
                {messages.map((msg) => (
                    <div
                        key={msg.id}
                        className={`p-3 rounded-2xl shadow-sm max-w-[90%] text-sm leading-relaxed ${msg.sender === 'bot'
                                ? 'bg-white border border-slate-200 rounded-tr-none self-start text-slate-700'
                                : 'bg-blue-600 rounded-tl-none self-end text-white'
                            }`}
                    >
                        {msg.text}
                    </div>
                ))}
            </div>

            {/* אזור הקלט - הטקסט נשמר בסטייט */}
            <div className="p-3 bg-white border-t border-slate-100 flex-shrink-0">
                <div className="flex gap-2 items-center bg-slate-100 rounded-xl px-2 py-1">
                    <input
                        type="text"
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        onKeyDown={handleInputKeyDown}
                        placeholder="איך אני יכול לעזור?"
                        className="flex-1 bg-transparent border-none py-2 text-sm outline-none text-slate-800 min-w-0"
                    />
                    <button
                        onClick={handleSend}
                        className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 flex-shrink-0 disabled:opacity-40 disabled:cursor-not-allowed"
                        disabled={!inputText.trim()}
                    >
                        <Send size={16} />
                    </button>
                </div>
            </div>
        </div>
    );

    // ---------- הלייאאוט הראשי - 2 פאנלים שמתחלקים ב-100% ----------
    // dir="ltr" על הקונטיינר מונע מ-RTL להפוך את סדר ה-flex (לא משפיע על טקסט בפנים)
    return (
        <div
            dir="ltr"
            className={`h-full w-full flex ${isVertical ? 'flex-row' : 'flex-col'} overflow-hidden`}
        >
            {chatFirst && ChatPanel}

            {/* הפאנל השני - המפה. גודל מפורש כדי שהצ'אט לא יכסה אותה */}
            {!isMaximized && (
                <div style={mapStyle} className="overflow-hidden flex-shrink-0">
                    {children}
                </div>
            )}

            {!chatFirst && ChatPanel}
        </div>
    );
};

export default ChatLayout;
