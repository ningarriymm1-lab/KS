from flask import Flask, render_template_string
from js import Response

app = Flask(__name__)
app.secret_key = "YOUR_SUPER_SECRET_KEY_HERE"

# หน้าเว็บหลักของแอปพลิเคชัน
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask on Cloudflare Workers</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-2xl shadow-lg max-w-md w-full text-center">
        <h1 class="text-2xl font-bold text-blue-600 mb-4">🚀 Flask บน Cloudflare</h1>
        <p class="text-gray-600 mb-6">ระบบจัดการและฐานข้อมูลของคุณพร้อมทำงานบน Serverless แล้วครับ!</p>
        <div class="p-4 bg-blue-50 rounded-lg text-blue-800 text-sm font-medium">
            สถานะระบบ: ออนไลน์ (Online) 🟢
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HOME_TEMPLATE)

# ฟังก์ชันเชื่อมต่อคำขอจาก Cloudflare Workers เข้ากับ Flask
async def on_fetch(request, env, ctx):
    # จำลองการแปลง HTTP Request จาก Cloudflare ให้ Flask ประมวลผล
    # (สามารถขยายส่วนนี้เพิ่มเติมหากต้องการดึงค่า Environment Variables จาก `env`)
    with app.test_request_context(
        path=request.url,
        method=request.method,
        headers=dict(request.headers.entries()) if hasattr(request, "headers") else {}
    ):
        try:
            response = app.full_dispatch_request()
            return Response.new(
                response.get_data(),
                status=response.status_code,
                headers=dict(response.headers)
            )
        except Exception as e:
            return Response.new(f"Internal Server Error: {str(e)}", status=500)
