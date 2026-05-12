import { BrowserRouter as Router } from 'react-router-dom';
import ChatWindow from './components/Chat/ChatWindow';
import MapWindow from './components/Chat/MapWindow';

const AppContent = () => {
  return (
    // עוטף חיצוני - רקע מדורג עדין שעוטף את כל העמוד
    <div
      className="h-screen w-screen overflow-hidden p-3 bg-gradient-to-br from-slate-200 via-slate-100 to-slate-200"
      dir="rtl"
    >
      {/* קונטיינר פנימי - עם פינות מעוגלות, צל וגבול שמנגיש את הגימור */}
      <div className="h-full w-full rounded-2xl shadow-2xl overflow-hidden border border-slate-300 bg-white">
        <ChatWindow>
          <MapWindow />
        </ChatWindow>
      </div>
    </div>
  );
};

export default function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}
