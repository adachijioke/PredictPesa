# 🚀 PredictPesa Quick Start Guide

Get PredictPesa up and running in 5 minutes!

## 📋 Prerequisites

- Node.js 18+
- Python 3.9+
- Hedera testnet account ([Get one free](https://portal.hedera.com))

## 🏃 Quick Setup

### 1. Clone & Install

```bash
# Clone repository
git clone https://github.com/yourusername/predictpesa.git
cd predictpesa

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .

# Install contract dependencies
cd ../contracts
npm install
```

### 2. Configure Environment

**Backend** (`backend/.env`):
```bash
cd backend
cp .env.example .env
# Edit .env and add:
# - GROQ_API_KEY (get from https://console.groq.com)
# - HEDERA_ACCOUNT_ID
# - HEDERA_PRIVATE_KEY
```

**Contracts** (`contracts/.env`):
```bash
cd ../contracts
cp .env.example .env
# Edit .env and add your Hedera credentials
```

### 3. Deploy Smart Contracts

```bash
cd contracts

# Compile contracts
npm run compile

# Run tests (optional)
npm test

# Deploy to Hedera testnet
npm run deploy:testnet

# Save the deployed contract addresses!
```

### 4. Update Backend Configuration

```bash
cd ../backend
# Edit .env and add deployed contract addresses:
# MARKET_FACTORY_CONTRACT=0x...
# ORACLE_CONTRACT=0x...
```

### 5. Start Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python simple_server.py
# Backend runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Frontend runs on http://localhost:8080
```

### 6. Open Application

Visit **http://localhost:8080** in your browser!

## 🎯 What's Next?

### Create Your First Market

1. Navigate to the Markets page
2. Click "Create Market"
3. Fill in market details
4. Submit transaction
5. Wait for confirmation

### Place Your First Stake

1. Browse available markets
2. Select a market
3. Choose YES or NO
4. Enter stake amount
5. Confirm transaction

### Interact with Contracts

```bash
cd contracts
node scripts/interact.js
```

## 📦 Deploy to Production

### Frontend (Vercel)

```bash
cd frontend

# Build for production
npm run build

# Deploy to Vercel
# 1. Push to GitHub
# 2. Import in Vercel dashboard
# 3. Vercel auto-deploys!
```

### Backend (Docker)

```bash
cd backend

# Build Docker image
docker build -t predictpesa-backend .

# Run container
docker run -p 8000:8000 predictpesa-backend
```

### Contracts (Mainnet)

```bash
cd contracts

# Update .env for mainnet
HEDERA_NETWORK=mainnet
HEDERA_JSON_RPC_URL=https://mainnet.hashio.io/api

# Deploy
npm run deploy:mainnet
```

## 🐛 Troubleshooting

**Port already in use?**
```bash
# Frontend: Edit vite.config.ts, change port
# Backend: Set PORT=8001 in .env
```

**Contract deployment fails?**
```bash
# Check HBAR balance
# Verify network connectivity
# Ensure correct private key format
```

**Frontend can't connect to backend?**
```bash
# Check VITE_API_URL in frontend/.env
# Ensure backend is running
# Check CORS settings
```

## 📚 Documentation

- **Contracts**: [contracts/README.md](contracts/README.md)
- **Deployment**: [contracts/DEPLOYMENT_GUIDE.md](contracts/DEPLOYMENT_GUIDE.md)
- **Backend**: [backend/README_backend.md](backend/README_backend.md)
- **Full Guide**: [README.md](README.md)

## 🆘 Get Help

- **Discord**: [Join community](https://discord.gg/predictpesa)
- **Email**: dev@predictpesa.com
- **Issues**: [GitHub Issues](https://github.com/predictpesa/issues)

---

**Happy predicting!** 🎲✨
