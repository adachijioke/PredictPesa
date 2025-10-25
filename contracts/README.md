# PredictPesa Smart Contracts

Smart contracts for the PredictPesa prediction market platform built on Hedera blockchain.

## 📋 Overview

This directory contains the Solidity smart contracts that power PredictPesa's decentralized prediction market infrastructure on Hedera.

### Core Contracts

- **MarketFactory.sol** - Factory contract for creating and managing prediction markets
- **PredictionMarket.sol** - Individual market contract handling stakes and resolutions
- **Oracle.sol** - Decentralized oracle system for market resolution with dispute mechanism
- **AMMPool.sol** - Automated Market Maker for secondary trading of position tokens

### Interfaces

- **IERC20.sol** - Standard ERC20 token interface
- **IHederaTokenService.sol** - Hedera Token Service (HTS) precompile interface

## 🏗️ Architecture

```
┌─────────────────┐
│ MarketFactory   │ ──► Creates markets
└────────┬────────┘
         │
         ├──► PredictionMarket (Market 1)
         ├──► PredictionMarket (Market 2)
         └──► PredictionMarket (Market N)
              │
              ├──► yesBTC Token (HTS)
              ├──► noBTC Token (HTS)
              └──► AMMPool (Secondary Trading)
                   
┌─────────────────┐
│     Oracle      │ ──► Resolves markets
└─────────────────┘      with multi-source data
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Hedera testnet account with HBAR

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env
# Edit .env with your Hedera credentials
```

### Environment Variables

Create a `.env` file with:

```env
HEDERA_ACCOUNT_ID=0.0.YOUR_ACCOUNT_ID
HEDERA_PRIVATE_KEY=your-private-key-here
HEDERA_JSON_RPC_URL=https://testnet.hashio.io/api
HEDERA_MAINNET_RPC_URL=https://mainnet.hashio.io/api
```

### Compile Contracts

```bash
npm run compile
```

### Run Tests

```bash
npm test
```

### Deploy to Hedera Testnet

```bash
npm run deploy:testnet
```

### Deploy to Hedera Mainnet

```bash
npm run deploy:mainnet
```

## 📝 Contract Details

### MarketFactory

Creates and manages prediction markets with the following features:

- **Market Creation**: Deploy new prediction markets with custom parameters
- **Token Integration**: Automatic creation of yesBTC/noBTC position tokens via HTS
- **Fee Management**: Configurable protocol fees
- **Oracle Integration**: Connects markets to oracle for resolution

**Key Functions:**
- `createMarket()` - Create a new prediction market
- `resolveMarket()` - Resolve market outcome (oracle only)
- `getMarket()` - Get market address by ID
- `updateOracle()` - Update oracle address (owner only)

### PredictionMarket

Individual market contract managing:

- **Staking**: Users can stake on YES or NO outcomes
- **Position Tokens**: Mint yesBTC/noBTC tokens representing positions
- **Resolution**: Oracle-based outcome determination
- **Rewards**: Proportional distribution to winners
- **Refunds**: Handle cancelled markets

**Key Functions:**
- `stake()` - Place a stake on YES or NO
- `claimReward()` - Claim winnings after resolution
- `refund()` - Get refund if market cancelled
- `getOdds()` - Get current market odds
- `calculatePayout()` - Calculate potential payout

### Oracle

Decentralized oracle system with:

- **Multi-Source Data**: Aggregate data from multiple verified sources
- **Reputation System**: Track source accuracy and reliability
- **Dispute Mechanism**: Allow challenges to resolutions
- **Confidence Scoring**: Require minimum confidence threshold

**Key Functions:**
- `submitData()` - Submit market outcome data (verified sources only)
- `raiseDispute()` - Challenge a market resolution
- `resolveDispute()` - Resolve disputes (governance)
- `addDataSource()` - Add new data source (owner only)
- `verifyDataSource()` - Verify data source (owner only)

### AMMPool

Automated Market Maker for position token trading:

- **Liquidity Pools**: Constant product formula (x * y = k)
- **Swaps**: Trade yesBTC ↔ noBTC tokens
- **Liquidity Provision**: Add/remove liquidity and earn fees
- **Fee Structure**: 0.3% swap fee

**Key Functions:**
- `addLiquidity()` - Provide liquidity to pool
- `removeLiquidity()` - Remove liquidity from pool
- `swap()` - Swap position tokens
- `getAmountOut()` - Get quote for swap
- `getPrice()` - Get current token prices

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
npm test

# Run with coverage
npm run coverage

# Run specific test file
npx hardhat test test/MarketFactory.test.js
```

## 🔐 Security

### Audits

- [ ] Internal security review
- [ ] External audit by [Audit Firm]
- [ ] Bug bounty program

### Best Practices

- All contracts use Solidity 0.8.20+ (overflow protection)
- ReentrancyGuard on critical functions
- Access control with modifiers
- Input validation on all public functions
- Emergency pause mechanisms

## 📊 Gas Optimization

Contracts are optimized for gas efficiency:

- Efficient storage packing
- Minimal storage reads/writes
- Batch operations where possible
- Event emission for off-chain indexing

## 🌐 Hedera Integration

### Hedera Token Service (HTS)

Position tokens (yesBTC/noBTC) are created using HTS for:

- Native Hedera token features
- Lower gas costs
- Built-in compliance features
- Seamless integration with Hedera ecosystem

### Hedera Consensus Service (HCS)

Oracle data can be verified via HCS for:

- Immutable audit trail
- Timestamped data feeds
- Decentralized consensus
- Low-cost data anchoring

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📞 Support

- Documentation: [docs.predictpesa.com](https://docs.predictpesa.com)
- Discord: [Join our community](https://discord.gg/predictpesa)
- Email: dev@predictpesa.com

---

**Built with ❤️ for Africa on Hedera**
