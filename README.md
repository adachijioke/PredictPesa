# 🌍 PredictPesa
### Africa's Premier DeFi-Native, Bitcoin-Powered Prediction Market Platform

[![Hedera](https://img.shields.io/badge/Built%20on-Hedera-40E0D0?style=for-the-badge&logo=hedera&logoColor=white)](https://hedera.com)
[![Bitcoin](https://img.shields.io/badge/Powered%20by-Bitcoin-F7931A?style=for-the-badge&logo=bitcoin&logoColor=white)](https://bitcoin.org)
[![Python](https://img.shields.io/badge/Backend-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

> **"Stake Bitcoin. Forecast Everything. Trade Your Belief."**

PredictPesa is a revolutionary DeFi-native, AI-powered prediction market protocol built on Hedera that transforms predictions into tradeable financial primitives. Users across Africa and globally can stake Bitcoin to forecast real-world outcomes—elections, FX rates, sports, food prices, rainfall, and more—while earning yield-bearing position tokens that integrate seamlessly with the broader DeFi ecosystem.

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution Overview](#-solution-overview)
- [Technical Architecture](#-technical-architecture)
- [Project Structure](#-project-structure)
- [Backend](#-backend)
- [Frontend](#-frontend)
- [Getting Started](#-getting-started)
- [API Endpoints](#-api-endpoints)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌍 Problem Statement

Africa's $40B+ betting market is dominated by centralized platforms with:
- **Opaque odds** and unfair house edges
- **Limited payout options** and currency restrictions  
- **No asset composability** - winnings can't be invested or used as collateral
- **Censorship risks** and regulatory uncertainties
- **Lack of local relevance** - few markets about African events

Meanwhile, global prediction markets like Polymarket and Augur have:
- **High barriers to entry** (complex UX, gas fees)
- **USD-centric design** limiting emerging market access
- **Western-focused events** with minimal African representation

## 💡 Solution Overview

PredictPesa creates the world's first **Bitcoin-native prediction market protocol** specifically designed for emerging markets, with these breakthrough innovations:

### 🔥 Core Innovations

**1. DeFi-Native Architecture**
- Every prediction creates tradeable **HTS tokens** (yesBTC/noBTC)
- Position tokens are **yield-bearing** and **composable** with other DeFi protocols
- **AMM-style liquidity pools** for each market enable secondary trading
- **Synthetic instruments** can be created from bundled positions

**2. Bitcoin-First Design**
- All positions staked in **BTC** (not stablecoins or fiat)
- Leverages Africa's **high Bitcoin adoption** (Nigeria #2 globally)
- **Hedge against local currency devaluation** while forecasting
- **Diaspora-friendly** for remittance and investment flows

**3. Mobile-Optimized UX**
- **Gasless transactions** via Hedera's sponsored transactions
- **USSD-style interface** familiar to mobile money users
- **Offline browsing** capabilities for low-bandwidth regions
- **Progressive Web App** with native mobile experience

**4. AI-Powered Market Curation**
- **Natural language market creation** ("Will Nigeria devalue naira in Q4?")
- **Trending topic suggestions** based on social signals and news
- **Price discovery optimization** for fair market odds
- **Local relevance scoring** prioritizing African events

---

## 🏗️ Technical Architecture

### Blockchain Infrastructure
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Hedera EVM    │    │ Hedera Token     │    │ Hedera Consensus│
│                 │    │ Service (HTS)    │    │ Service (HCS)   │
│ Smart Contracts │◄──►│                  │◄──►│                 │
│ Market Logic    │    │ Position Tokens  │    │ Oracle Data     │
│ AMM Pools       │    │ yesBTC/noBTC     │    │ Result Feeds    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Core Smart Contracts

**MarketFactory.sol**
- Creates new prediction markets
- Manages market categories and metadata
- Handles market resolution logic

**PredictionPool.sol** 
- AMM-style liquidity management
- Position token minting/burning
- Yield distribution mechanisms

**Oracle.sol**
- Integrates with Hedera Consensus Service
- Aggregates multiple data sources
- Handles dispute resolution

**PositionToken.sol** (HTS)
- ERC-20 compatible position tokens
- Yield accrual mechanisms
- Cross-market composability

### AI Components

**Market Suggestion Engine**
- NLP processing of news feeds and social media
- Trending topic identification and scoring
- Local relevance filtering and categorization

**Price Discovery System**
- Bayesian probability modeling
- Initial market calibration
- Liquidity optimization algorithms

---

## 📂 Project Structure

The project is organized into two main components:

```
predictpesa/
├── backend/           # Python FastAPI backend
│   ├── predictpesa/   # Core application code
│   ├── tests/         # Test suites
│   └── ...
├── frontend/          # React/TypeScript frontend
│   ├── src/           # Source code
│   ├── public/        # Static assets
│   └── ...
└── README.md          # This file
```

---

## 🔧 Backend

The backend is built with Python using FastAPI, SQLAlchemy, and integrates with Hedera's blockchain services.

### Core Models

- **User**: Account management and authentication
- **Market**: Prediction market definitions and states
- **MarketOutcome**: Possible outcomes for markets
- **Stake**: User positions in markets
- **OracleData**: External data sources for market resolution
- **OracleSource**: Verified data providers
- **Transaction**: On-chain transaction records

### Key Features

- **Complete API**: RESTful endpoints for all platform functionality
- **AI Integration**: Groq LLM integration for market analysis
- **Blockchain Integration**: Hedera Smart Contract Service and Token Service
- **Comprehensive Testing**: 100% test coverage of models and core infrastructure

### Environment Setup

The backend requires the following environment variables:
```
GROQ_API_KEY=your-groq-api-key
HEDERA_ACCOUNT_ID=your-hedera-account-id
HEDERA_PRIVATE_KEY=your-hedera-private-key
SECRET_KEY=your-jwt-secret-key
```

---

## 🎨 Frontend

The frontend is built with React, TypeScript, and Vite, featuring a modern UI with Tailwind CSS and Shadcn UI components.

### Key Features

- **Modern React/TypeScript**: Built with the latest React 18 and TypeScript
- **Responsive Design**: Mobile-first approach for African markets
- **Web3 Integration**: Wallet connection for blockchain interactions
- **Interactive Markets**: Real-time market data visualization
- **Portfolio Management**: Track and manage prediction positions

### Pages

- **Home**: Landing page with platform introduction
- **Markets**: Browse and filter available prediction markets
- **Market Detail**: Individual market view with staking interface
- **Dashboard**: User overview and analytics
- **Portfolio**: User's active positions and history
- **Profile**: User account management
- **Rewards**: Platform rewards and incentives

### Tech Stack

- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: Shadcn UI (Radix UI primitives)
- **State Management**: React Query
- **Routing**: React Router
- **Charts**: Recharts
- **Form Handling**: React Hook Form with Zod validation

---

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+
- Git

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Start development server
python simple_server.py
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Visit `http://localhost:5173` to see the frontend application.

---

## 📡 API Endpoints

The backend provides the following key API endpoints:

- **GET /**: Root endpoint with welcome message
- **GET /health**: Health check for monitoring
- **GET /api/v1/markets**: List available prediction markets
- **GET /api/v1/ai/analyze**: AI-powered market analysis

For detailed API documentation, run the backend server and visit `/docs`.

---

## 🧪 Testing

### Backend Testing

```bash
# Run all tests
python -m pytest tests/test_models.py tests/test_simple_api.py tests/test_core_config.py -v

# Run specific test suites
python -m pytest tests/test_models.py -v  # Model tests
python -m pytest tests/test_core_config.py -v  # Core config tests
python -m pytest tests/test_simple_api.py -v  # API tests

# Basic functionality test
python test_basic.py
```

### Frontend Testing

```bash
# Run tests
cd frontend
npm test

# Run with coverage
npm test -- --coverage
```

---

## 📦 Deployment

### Backend Deployment

The backend can be deployed using Docker:

```bash
# Build Docker image
docker build -t predictpesa-backend ./backend

# Run container
docker run -p 8000:8000 -e PORT=8000 predictpesa-backend
```

### Frontend Deployment

The frontend can be built for production:

```bash
cd frontend
npm run build
```

The output will be in the `frontend/dist` directory, ready to be served by any static file server.

---

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<p align="center">
  <b>PredictPesa</b><br>
  <i>Stake Bitcoin. Forecast Everything. Trade Your Belief.</i><br>
  Built with ❤️ for Africa
</p>
