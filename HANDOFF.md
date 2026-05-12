# Zchat Frontend Mock - Handoff Document

## Overview
A standalone React chat panel that communicates with the Zchat backend API.
The app is designed to be embedded inside a parent app (the ecosystem) as a side panel.
It is **not** a full-page app — it has no map of its own. The parent app owns the map (MAPIT).

---

## Stack
- **React** 18.2.0
- **TypeScript**
- **Vite** 5 (build tool)
- **Tailwind CSS** v3 (styling)
- **Radix UI** (component primitives — matches the ecosystem design system)
- **Node** 18.15.0 / **npm** 9.5.0

---

## Running Locally
```bash
npm install
npm run dev
```
App runs at `http://localhost:5173`

> The mock backend (`zchat-mockapi`) must also be running at `http://localhost:8000`

---

## Project Structure
```
src/
├── api/
│   └── chat.ts              # All HTTP calls to the backend (/init, /chat)
├── components/
│   └── Chat/
│       ├── ChatPanel.tsx    # Main chat container
│       ├── MessageList.tsx  # Scrollable conversation (Radix ScrollArea)
│       ├── MessageBubble.tsx# Individual message — user bubble / assistant card
│       └── ChatInput.tsx    # Textarea + send button
├── contexts/
│   └── MapActionsContext.tsx# React context exposing mapActions to all components
├── mapActions/
│   └── index.ts            # MapActions interface + default no-op implementation
├── types/
│   └── index.ts            # Shared TypeScript types (Message, Entity, ChatResponse)
├── App.tsx                  # Root component — state, API calls, layout
├── main.tsx                 # Entry point
└── index.css                # Tailwind imports + global reset
```

---

## API Integration

### Base URL
```
http://localhost:8000
```
Replace with the real backend URL when deploying.

### Headers (sent on every request)
| Header | Value |
|--------|-------|
| `api-key` | Currently hardcoded mock value |
| `user-personal-number` | Currently hardcoded mock value |
| `Content-Type` | `application/json` |

### Endpoints

#### `POST /init`
Called once on app startup. Sends user metadata so the backend knows what data to serve.

#### `POST /chat`
Called on every message. Sends the user message + session ID + user metadata.
The metadata is sent with every request so the backend can filter data from the database accordingly.

### User Metadata
Defined once in `src/api/chat.ts` under `userMetadata` and spread into both `/init` and `/chat` requests:
```typescript
const userMetadata = {
  unit: '...',
  reality: '...',
  module: '...',
  role: '...',
  plan: '...',
  case: '...',
};
```
**When integrating with the parent app:** replace the hardcoded values in `userMetadata` with real values received from the parent app. This is the only place that needs to change.

### Session Management
- First message → backend generates a `session_id` and returns it
- All subsequent messages include that `session_id`
- Managed automatically in `App.tsx` via `useState`

---

## Map Integration (Pending)

The chat does not render a map. The parent app owns the map (MAPIT).
When the chat receives entities from the backend, it notifies the parent app via `mapActions`.

### MapActions Interface
Located at `src/mapActions/index.ts`:
```typescript
interface MapActions {
  drawEntities: (entities: Entity[]) => void; // draw entities on the map
  zoomToEntity: (entity: Entity) => void;     // zoom to a specific entity
  clearEntities: () => void;                  // clear all entities from the map
}
```

### Current Behavior (Mock Mode)
All three functions just `console.log` — no map interaction.

### When Integrating with the Parent App
Replace `defaultMapActions` in `src/App.tsx` with the real implementation provided by the parent app. The integration method (props, `window`, `postMessage`) is TBD and depends on how the parent app embeds the chat.

### Entity Format
Entities returned by the backend:
```typescript
interface Entity {
  layer: string | null;      // map layer identifier
  entity_id: string | null;  // unique entity ID
  geometry: string | null;   // WKT string, lat/lon (WGS84), e.g. POINT (31.35 34.31)
}
```
Supported geometry types: `POINT`, `LINESTRING`, `POLYGON`

---

## Key Design Decisions

### Metadata sent with every request
The backend uses `unit`, `reality`, `module`, `role`, `plan`, `case` to determine what data to retrieve from its database. These are sent in both `/init` and `/chat` requests.

### No map in this app
The chat is a panel widget. Map rendering is entirely the parent app's responsibility. The `mapActions` abstraction ensures the chat can trigger map behavior without knowing how the map works.

### Radix UI
Used to match the parent ecosystem's design system. Currently only `ScrollArea` is used — more Radix primitives can be added as the UI grows.

### RTL + Hebrew
The app is fully RTL (`dir="rtl"` on `<html>`) and all UI text is in Hebrew.

---

## Pending / Open Questions
- How does the parent app embed the chat? (props / `window` / `postMessage` / iframe)
- How does the parent app provide user metadata to the chat at startup?
- How does the parent app provide `mapActions` to the chat?
- What is the real backend URL?
- What is the real `api-key` format and how is it obtained?
