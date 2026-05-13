import React from 'react'
import { MapPin, Compass } from 'lucide-react'

/**
 * ============================================================
 * MapWindow - תצוגת מפה (תמונה סטטית)
 * ============================================================
 *
 * כרגע: תמונת מפה סטטית (לא אינטראקטיבית, לא זזה).
 *
 * **כדי להחליף את התמונה בעתיד:**
 *   פשוט שנה את הקבוע MAP_IMAGE_URL למטה.
 *   אם תרצה מפה אינטראקטיבית - תוכל להחליף את ה-<img> ב-<iframe>.
 */

// ============================================================
// כתובת התמונה - **שנה כאן כדי להחליף**
// ============================================================
// תמונת מפה / תצלום אווירי. אפשר להחליף בכל URL של תמונה.
const MAP_IMAGE_URL =
    'https://images.unsplash.com/photo-1524661135-423995f22d0b?w=1600&q=80&auto=format';

const MapWindow: React.FC = () => {
    return (
        <div className="h-full w-full relative overflow-hidden bg-stone-200">
            {/* תמונת המפה - סטטית, ממלאת את כל האזור */}
            <img
                src={MAP_IMAGE_URL}
                alt="מפה"
                className="absolute inset-0 w-full h-full object-cover select-none"
                draggable={false}
            />

            {/* שכבת overlay עדינה לתחושה של עומק */}
            <div className="absolute inset-0 bg-gradient-to-br from-transparent via-transparent to-stone-900/10 pointer-events-none" />

            {/* באנר עליון-ימני - אזור התצוגה */}
            <div className="absolute top-3 right-3 bg-white/95 backdrop-blur-sm rounded-lg shadow-lg ring-1 ring-stone-200/80 px-3 py-2 pointer-events-none">
                <div className="flex items-center gap-2">
                    <MapPin size={14} className="text-amber-600" strokeWidth={2} fill="currentColor" />
                    <div className="flex flex-col">
                        <span className="text-[12px] font-medium text-stone-800 tracking-wide leading-tight">
                            אזור התצוגה
                        </span>
                        <span className="text-[9px] text-stone-500 font-mono tracking-wider mt-0.5">
                            32.0853, 34.7818
                        </span>
                    </div>
                </div>
            </div>

            {/* באנר תחתון-שמאלי - Workspace */}
            <div className="absolute bottom-3 left-3 bg-[#0f1419]/85 backdrop-blur-sm text-stone-100 rounded-lg shadow-lg px-3 py-1.5 pointer-events-none">
                <div className="flex items-center gap-1.5">
                    <Compass size={12} strokeWidth={1.5} className="text-amber-400" />
                    <span className="text-[10px] tracking-[0.2em] uppercase font-light">
                        Workspace
                    </span>
                </div>
            </div>
        </div>
    )
}

export default MapWindow;
