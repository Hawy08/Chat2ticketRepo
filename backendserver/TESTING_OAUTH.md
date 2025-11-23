# Testing Google OAuth Workflow with WatsonX Orchestrate

## Overview
The OAuth endpoints work independently of WhatsApp, so you can test them with WatsonX Orchestrate or any HTTP client.

## Endpoints for Testing

### 1. Initiate OAuth Flow
**POST** `/auth/google/login/whatsapp`

**Query Parameters:**
- `whatsapp_user_id` (required): Test user identifier (e.g., "test_user_123")
- `booking_id` (optional): Booking ID if testing with a booking

**Example Request:**
```bash
curl -X POST "http://localhost:8000/auth/google/login/whatsapp?whatsapp_user_id=test_user_123&booking_id=1"
```

**Response:**
```json
{
  "url": "https://accounts.google.com/o/oauth2/auth?...",
  "state": "abc123...",
  "message": "Click this link to authorize Google access..."
}
```

### 2. Check OAuth Status (Webhook)
**GET** `/auth/google/status/{whatsapp_user_id}`

**Example Request:**
```bash
curl "http://localhost:8000/auth/google/status/test_user_123"
```

**Response (Pending):**
```json
{
  "status": "pending",
  "whatsapp_user_id": "test_user_123",
  "booking_id": 1,
  "created_at": "2024-01-01T12:00:00",
  "completed_at": null,
  "has_tokens": false
}
```

**Response (Completed):**
```json
{
  "status": "completed",
  "whatsapp_user_id": "test_user_123",
  "booking_id": 1,
  "created_at": "2024-01-01T12:00:00",
  "completed_at": "2024-01-01T12:05:00",
  "has_tokens": true
}
```

### 3. Check Status by State Token
**GET** `/auth/google/status?state={state_token}`

**Example Request:**
```bash
curl "http://localhost:8000/auth/google/status?state=abc123..."
```

## Testing with WatsonX Orchestrate

### Step 1: Configure HTTP Action in WatsonX Orchestrate
1. Add an **HTTP Request** action to your flow
2. Set method to **POST**
3. URL: `http://your-server:8000/auth/google/login/whatsapp`
4. Add query parameters:
   - `whatsapp_user_id`: Use a variable like `{{$user_id}}` or hardcode `test_user_123`
   - `booking_id`: Optional, use `{{$booking_id}}` if available

### Step 2: Extract OAuth URL
1. Parse the response JSON
2. Extract the `url` field
3. Store it in a variable (e.g., `{{$oauth_url}}`)

### Step 3: Send URL to User (Simulated)
In testing, you can:
- Log the URL to console
- Display it in WatsonX Orchestrate's test interface
- Copy it manually to test in browser

### Step 4: Poll for Completion
Add a **Loop** or **Wait** action that:
1. Calls `GET /auth/google/status/{whatsapp_user_id}` every few seconds
2. Checks if `status == "completed"`
3. Proceeds when completed

### Example WatsonX Orchestrate Flow:
```
1. User says "I want to connect Google"
2. HTTP POST → /auth/google/login/whatsapp
3. Extract {{$oauth_url}} from response
4. Send message: "Click here: {{$oauth_url}}"
5. Wait 5 seconds
6. HTTP GET → /auth/google/status/{{$user_id}}
7. If status != "completed", go back to step 5
8. Send message: "Google connected successfully!"
```

## Manual Testing Steps

1. **Start your server:**
   ```bash
   python main.py
   ```

2. **Initiate OAuth:**
   ```bash
   curl -X POST "http://localhost:8000/auth/google/login/whatsapp?whatsapp_user_id=test123"
   ```

3. **Copy the URL** from the response and open it in a browser

4. **Complete OAuth** in the browser (Google login)

5. **Check status:**
   ```bash
   curl "http://localhost:8000/auth/google/status/test123"
   ```

6. **Verify** status changes from "pending" to "completed"

## Testing Scenarios

### Scenario 1: Basic OAuth Flow
- User ID: `test_user_1`
- No booking
- Expected: OAuth completes, tokens stored

### Scenario 2: OAuth with Booking
- User ID: `test_user_2`
- Booking ID: `1` (must exist in database)
- Expected: OAuth completes, calendar event created, email sent

### Scenario 3: Status Polling
- Start OAuth
- Poll status endpoint every 2 seconds
- Verify status transitions: `pending` → `completed`

### Scenario 4: Error Handling
- Try to check status for non-existent user
- Expected: `{"status": "not_found"}`

## Notes for Production

When you connect to WhatsApp:
- The `whatsapp_user_id` will be the actual WhatsApp phone number
- WatsonX Orchestrate will automatically handle the flow
- The endpoints remain the same, just with real user IDs

## FastAPI Interactive Docs

You can also test using FastAPI's built-in docs:
- Visit: `http://localhost:8000/docs`
- Find the `/auth/google/login/whatsapp` endpoint
- Click "Try it out" and test directly

