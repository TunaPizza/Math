from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routes.linear_routes import router as linear_router
from routes.fraction_routes import router as fraction_router

app = FastAPI(title="プリント生成アプリ")

# ルート登録
app.include_router(linear_router, prefix="/linear", tags=["Linear"])
app.include_router(fraction_router, prefix="/fraction", tags=["Fraction"])

# ホームページ
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>プリント生成アプリ</title>
        <style>
            body { font-family: sans-serif; margin: 20px; }
            ul { list-style-type: none; padding-left: 0; }
            li { margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <h1>プリント生成アプリ</h1>
        <ul>
            <li><a href="/linear">一次関数プリントページ</a></li>
            <li><a href="/fraction">分数プリントページ</a></li>
        </ul>
        <p>今後ページを増やす場合は、<code>routes/</code> に追加し、ここで <code>include_router</code> するだけでOKです。</p>
    </body>
    </html>
    """
