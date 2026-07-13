# Running VANTAGE on Windows 11 in VS Code — full walkthrough

This assumes a clean Windows 11 machine. If you already have Python and
Node installed, skip to step 3.

## 1. Install prerequisites

1. **Python 3.11+** — https://www.python.org/downloads/
   - During install, **tick "Add python.exe to PATH"**.
   - Verify: open a new terminal and run:
     ```powershell
     python --version
     ```
2. **Node.js 20 LTS** — https://nodejs.org
   - Verify:
     ```powershell
     node --version
     npm --version
     ```
3. **VS Code** — https://code.visualstudio.com
   - Recommended extensions (install from the Extensions panel, `Ctrl+Shift+X`):
     - *Python* (Microsoft)
     - *ES7+ React/Redux/React-Native snippets*
     - *Tailwind CSS IntelliSense*

## 2. Get the project onto your machine

Unzip the project folder anywhere, e.g. `C:\Projects\career-advisor-ai`.
Open it in VS Code: `File → Open Folder…` → select `career-advisor-ai`.

You should see:
```
career-advisor-ai/
├── backend/
├── frontend/
├── README.md
└── SETUP_WINDOWS.md
```

## 3. Start the backend (FastAPI)

Open a terminal in VS Code: **Terminal → New Terminal** (it opens in
PowerShell by default on Windows).

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
```

> If PowerShell blocks the activate script with an execution-policy error,
> run this once (in an admin PowerShell) and try again:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

```powershell
pip install -r requirements.txt
python run.py
```

You should see Uvicorn start on `http://127.0.0.1:8000`. Leave this
terminal running. Open `http://127.0.0.1:8000/docs` in a browser to confirm
the API is live and browse the interactive Swagger docs.

**Regenerating the datasets (optional):** the CSVs are already built and
committed, so this step isn't required. If you edit `build_occupations.py`
or `build_courses.py`, re-run them from `backend/app/data`:
```powershell
cd app\data
python build_occupations.py
python build_courses.py
```

## 4. Start the frontend (React + Vite)

Open a **second** VS Code terminal (`+` icon in the terminal panel, or
`Ctrl+Shift+5`) so the backend keeps running in the first one.

```powershell
cd frontend
npm install
npm run dev
```

Vite will print a local URL, typically `http://localhost:5173`. Open it in
your browser.

## 5. Use the app

1. Type skills into the "Your skills" field (autocompletes from the real
   skills taxonomy — try `Python`, `SQL`, `Linux`, `Machine Learning`…).
2. Optionally add interest tags and set years of experience.
3. Click **Compute my recommendations** — this calls the FastAPI backend
   live and streams back a freshly-computed hybrid recommendation.
4. Toggle light/dark mode with the sun/moon button, top right.

## 6. Common issues

| Symptom | Fix |
|---|---|
| Frontend shows "Couldn't reach the recommendation API" | Make sure the backend terminal is still running and shows `Uvicorn running on http://127.0.0.1:8000`. |
| `ModuleNotFoundError` in the backend | You likely didn't activate the venv — run `venv\Scripts\activate` again in that terminal before `python run.py`. |
| CORS error in the browser console | Confirm the frontend is running on port `5173` (the backend's `CORSMiddleware` in `app/main.py` currently allows exactly that origin — add yours to the list if you changed the port). |
| `npm install` fails on peer dependencies | Re-run with `npm install --legacy-peer-deps`. |
| Port 8000 or 5173 already in use | Stop whatever else is using it, or change the port: backend in `run.py` (`port=8000`), frontend with `npm run dev -- --port 5174` (and update `frontend/.env` → `VITE_API_URL`). |

## 7. Project structure recap

See the architecture table in `README.md` for what each file does.
