from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/success", response_class=HTMLResponse)
async def payment_success(request: Request, session_id: str):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Successful</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f0f2f5;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .card {{
                background: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
                max-width: 500px;
                width: 100%;
            }}
            h1 {{
                color: #2ecc71;
                margin-bottom: 1rem;
            }}
            p {{
                color: #555;
                margin-bottom: 1.5rem;
            }}
            .session-box {{
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 1rem;
                border-radius: 5px;
                word-break: break-all;
                font-family: monospace;
                margin-bottom: 1rem;
                color: #333;
            }}
            .btn {{
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1rem;
                transition: background-color 0.2s;
            }}
            .btn:hover {{
                background-color: #0056b3;
            }}
            .btn:active {{
                transform: translateY(1px);
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Payment Successful! 🎉</h1>
            <p>Thank you for your payment. Your booking is being processed.</p>
            <p>Please copy your Session ID below to confirm your booking:</p>
            
            <div class="session-box" id="sessionId">{session_id}</div>
            
            <button class="btn" onclick="copyToClipboard()">Copy Session ID</button>
            
            <p id="toast" style="color: #2ecc71; margin-top: 1rem; opacity: 0; transition: opacity 0.3s;">Copied to clipboard!</p>
        </div>

        <script>
            function copyToClipboard() {{
                const sessionId = document.getElementById('sessionId').innerText;
                navigator.clipboard.writeText(sessionId).then(() => {{
                    const toast = document.getElementById('toast');
                    toast.style.opacity = '1';
                    setTimeout(() => {{
                        toast.style.opacity = '0';
                    }}, 2000);
                }}).catch(err => {{
                    console.error('Failed to copy: ', err);
                }});
            }}
        </script>
    </body>
    </html>
    """
    return html_content
