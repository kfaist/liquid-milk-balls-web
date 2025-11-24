# Production Deployment Guide - Mirror's Echo

This document describes the production-ready features added for TURN server support, Stripe payment integration, and enhanced WebRTC connectivity.

## 🆕 New Features

### 1. **TURN Server Support** (coturn)
Production-ready TURN server configuration using Docker Compose for reliable WebRTC connectivity behind NATs and firewalls.

### 2. **Stripe Payment Integration**
Exhibition License ($400) purchase via Stripe Checkout with server-side session creation.

### 3. **Enhanced WebRTC Client**
Updated WebRTC client that:
- Fetches time-limited TURN credentials automatically
- Integrates with the Mirror's Echo page API (`window.MIRRORS_ECHO`)
- Supports Connect/Disconnect buttons in the UI
- Works with the existing signaling server at `/signaling`

---

## 📋 Environment Variables

All sensitive configuration uses environment variables. **Never commit secrets to the repository.**

### Required for TURN Server

| Variable | Description | Example |
|----------|-------------|---------|
| `TURN_SECRET` | Shared secret for TURN credential generation (must match coturn config) | `abc123def456...` (use `openssl rand -hex 32`) |
| `TURN_SERVER_URL` | TURN server domain or IP address | `turn.yourdomain.com` or `203.0.113.42` |
| `TURN_TTL` | Credential lifetime in seconds (optional, default: 3600) | `3600` |

### Required for Stripe Payment

| Variable | Description | Example |
|----------|-------------|---------|
| `STRIPE_SECRET_KEY` | Stripe secret key (test or live) | `sk_test_...` or `sk_live_...` |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | `pk_test_...` or `pk_live_...` |
| `DOMAIN` | Full domain URL for payment redirects | `https://yourdomain.com` |

### Optional

| Variable | Description | Example |
|----------|-------------|---------|
| `PORT` | Server port (default: 3000) | `3000` |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret (for webhook verification) | `whsec_...` |

---

## 🚀 Deployment Instructions

### Step 1: Configure TURN Server (coturn)

#### 1.1 Generate TURN Secret

```bash
# Generate a strong random secret
openssl rand -hex 32
```

Save this secret - you'll need it for both coturn configuration and your application server.

#### 1.2 Update TURN Configuration

Edit `docker/coturn/turnserver.conf`:

```conf
# Replace REPLACE_WITH_YOUR_SECRET with your generated secret
static-auth-secret=YOUR_GENERATED_SECRET_HERE

# Replace turn.example.com with your actual domain
realm=turn.yourdomain.com

# Set your server's public IP address
external-ip=YOUR_PUBLIC_IP_ADDRESS
```

#### 1.3 Start coturn

```bash
cd docker/coturn
docker-compose up -d
```

#### 1.4 Verify coturn is running

```bash
docker-compose ps
docker-compose logs -f
```

You should see:
```
coturn    | Realm: turn.yourdomain.com
coturn    | Listening on port 3478
```

#### 1.5 Configure Firewall

Ensure these ports are open:
- **3478/UDP** - TURN/STUN UDP
- **3478/TCP** - TURN/STUN TCP
- **5349/TCP** - TURN TLS (if using TLS)
- **49152-65535/UDP** - TURN relay port range

Example for Ubuntu/Debian with `ufw`:
```bash
sudo ufw allow 3478/udp
sudo ufw allow 3478/tcp
sudo ufw allow 5349/tcp
sudo ufw allow 49152:65535/udp
```

---

### Step 2: Configure Application Server

#### 2.1 Install Dependencies

```bash
cd server
npm install
```

#### 2.2 Set Environment Variables

Create a `.env` file in the `server/` directory:

```bash
# TURN Server Configuration
TURN_SECRET=your_generated_secret_from_step_1
TURN_SERVER_URL=turn.yourdomain.com
TURN_TTL=3600

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_YOUR_TEST_KEY
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_TEST_KEY
DOMAIN=https://yourdomain.com

# Server Configuration
PORT=3000
```

**For Railway Deployment:**
Set environment variables in the Railway dashboard under "Variables".

**For Production:**
- Use `sk_live_...` and `pk_live_...` for Stripe live keys
- Ensure DOMAIN matches your production URL

#### 2.3 Start Server

**Development:**
```bash
cd server
npm start
```

**Production:**
```bash
NODE_ENV=production PORT=3000 node server/stripe-endpoints.js
```

**With PM2 (recommended for production):**
```bash
pm2 start server/stripe-endpoints.js --name mirrors-echo
pm2 save
pm2 startup
```

---

### Step 3: Deploy to Railway (Optional)

#### 3.1 Add Environment Variables

In Railway dashboard, add all required environment variables from Step 2.2.

#### 3.2 Deploy

Railway will automatically detect `package.json` and deploy your application.

#### 3.3 Configure TURN Server Domain

After deployment, update `TURN_SERVER_URL` to point to your TURN server's public IP or domain.

---

## 🧪 Testing Instructions

### Test 1: TURN Credentials Endpoint

```bash
curl http://localhost:3000/api/turn-credentials
```

**Expected Response:**
```json
{
  "username": "1700000000:mirrors-echo-user",
  "credential": "base64encodedhmac==",
  "ttl": 3600,
  "urls": [
    "turn:turn.yourdomain.com:3478?transport=udp",
    "turn:turn.yourdomain.com:3478?transport=tcp"
  ]
}
```

### Test 2: Stripe Configuration

```bash
curl http://localhost:3000/api/stripe-config
```

**Expected Response:**
```json
{
  "publishableKey": "pk_test_..."
}
```

### Test 3: Create Checkout Session

```bash
curl -X POST http://localhost:3000/api/create-checkout-session \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
{
  "sessionId": "cs_test_...",
  "checkoutUrl": "https://checkout.stripe.com/...",
  "publishableKey": "pk_test_..."
}
```

### Test 4: Full WebRTC Flow

1. **Start the server:**
   ```bash
   cd server
   npm start
   ```

2. **Open the application:**
   Navigate to `http://localhost:3000` in two separate browser windows (or devices).

3. **Start camera in first window:**
   - Click "Connect" button
   - Allow camera permissions
   - You should see your local camera feed

4. **Connect in second window:**
   - Click "Connect" button
   - Allow camera permissions
   - Both windows should now show local and remote streams

5. **Verify TURN is working:**
   - Open browser DevTools (F12)
   - Go to Console tab
   - Look for logs like:
     ```
     [WebRTC] TURN credentials received: {...}
     [WebRTC] Using TURN servers: ["turn:..."]
     [WebRTC] ✅ WebRTC connection established
     ```

6. **Check ICE candidate types:**
   - In Console, type: `window.MirrorsEchoWebRTC.getPeerConnection().getStats()`
   - Look for candidate pairs with type "relay" (indicates TURN is being used)

### Test 5: Stripe Payment Flow

1. **Open the application:**
   Navigate to `http://localhost:3000`

2. **Click "Purchase Exhibition License - $400"**

3. **Verify redirect to Stripe Checkout:**
   - You should be redirected to Stripe's checkout page
   - With test keys, you can use test card: `4242 4242 4242 4242`
   - Any future date for expiry, any CVC

4. **Complete test payment:**
   - Fill in test card details
   - Click "Pay"
   - You should be redirected to `/payment-success.html`

---

## 🔒 Security Checklist

- [ ] Generated strong random secret for TURN (32+ characters)
- [ ] TURN secret is stored in environment variables, not committed
- [ ] Stripe keys are test keys for development, live keys for production
- [ ] All environment variables are set in deployment platform (Railway, etc.)
- [ ] Firewall rules are configured to allow TURN server ports
- [ ] TLS/HTTPS is enabled for production deployment
- [ ] coturn external-ip is set to correct public IP
- [ ] Server domain matches DOMAIN environment variable
- [ ] Stripe webhook secret is configured if using webhooks

---

## 📁 File Structure

```
liquid-milk-balls-web/
├── docker/
│   └── coturn/
│       ├── docker-compose.yml          # Coturn Docker setup
│       └── turnserver.conf             # Coturn configuration template
├── server/
│   ├── package.json                    # Server dependencies
│   ├── stripe-endpoints.js             # Main server with Stripe & signaling
│   └── turn-credentials.js             # TURN credential generation
├── index.html                          # Main page (updated with webrtc-client.js)
├── webrtc-client.js                    # Enhanced WebRTC client
└── README-updates.md                   # This file
```

---

## 🔧 Troubleshooting

### TURN Server Issues

**Problem:** TURN credentials endpoint returns 500 error

**Solution:** Check that `TURN_SECRET` environment variable is set:
```bash
echo $TURN_SECRET
```

**Problem:** WebRTC still not connecting behind NAT

**Solution:** 
1. Verify coturn is running: `docker-compose ps`
2. Check firewall rules allow TURN ports
3. Verify external-ip is set correctly in turnserver.conf
4. Test connectivity: `nc -zv YOUR_TURN_SERVER 3478`

### Stripe Issues

**Problem:** Payment button doesn't work

**Solution:**
1. Check browser console for errors
2. Verify STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY are set
3. Ensure keys match (both test or both live, not mixed)

**Problem:** Redirect after payment goes to wrong URL

**Solution:** Update DOMAIN environment variable to match your deployment URL

### WebRTC Issues

**Problem:** Camera doesn't start

**Solution:**
1. Ensure you're using HTTPS or localhost
2. Check browser permissions for camera
3. Verify no other app is using the camera

**Problem:** Remote stream doesn't appear

**Solution:**
1. Check browser console for errors
2. Verify signaling WebSocket is connected
3. Check ICE connection state in DevTools

---

## 📞 Support

For issues or questions:
- Email: kristabluedoor@gmail.com
- GitHub Issues: https://github.com/kfaist/liquid-milk-balls-web/issues

---

## 📝 License

GNU AGPL-3.0-or-later

Commercial licensing available - contact kristabluedoor@gmail.com

---

## 🎯 Quick Start Commands

```bash
# 1. Generate TURN secret
openssl rand -hex 32

# 2. Update turnserver.conf with your secret and domain

# 3. Start coturn
cd docker/coturn && docker-compose up -d

# 4. Set environment variables
export TURN_SECRET=your_secret
export TURN_SERVER_URL=turn.yourdomain.com
export STRIPE_SECRET_KEY=sk_test_...
export STRIPE_PUBLISHABLE_KEY=pk_test_...
export DOMAIN=http://localhost:3000

# 5. Install dependencies and start server
cd server
npm install
npm start

# 6. Open browser
open http://localhost:3000
```

**Test WebRTC:**
- Open in two browser windows
- Click "Connect" in both
- Verify local and remote streams appear

**Test Stripe:**
- Click "Purchase Exhibition License - $400"
- Use test card: 4242 4242 4242 4242
- Verify redirect to Stripe and back
