from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# Mount a static directory to serve HTML files and images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route to serve index.html
@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        file_path = Path("static/index.html")
        return HTMLResponse(content=file_path.read_text())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Index file not found")

# Route to serve the static image "rain.gif"
@app.get("/rain.gif", response_class=FileResponse, name="get_rain_gif")
async def read_rain_gif():
    try:
        file_path = Path("static/rain.gif")
        return FileResponse(path=file_path, media_type="image/gif")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Rain GIF not found")

# Run the app with Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
