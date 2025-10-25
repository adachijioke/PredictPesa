require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    hederaTestnet: {
      url: process.env.HEDERA_JSON_RPC_URL || "https://testnet.hashio.io/api",
      accounts: process.env.HEDERA_PRIVATE_KEY ? [process.env.HEDERA_PRIVATE_KEY] : [],
      chainId: 296,
      gas: 3000000,
      gasPrice: 50000000000 // 50 gwei
    },
    hederaMainnet: {
      url: process.env.HEDERA_MAINNET_RPC_URL || "https://mainnet.hashio.io/api",
      accounts: process.env.HEDERA_PRIVATE_KEY ? [process.env.HEDERA_PRIVATE_KEY] : [],
      chainId: 295,
      gas: 3000000,
      gasPrice: 50000000000
    },
    localhost: {
      url: "http://127.0.0.1:8545",
      chainId: 31337
    }
  },
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  },
  etherscan: {
    apiKey: {
      hederaTestnet: "test",
      hederaMainnet: "test"
    },
    customChains: [
      {
        network: "hederaTestnet",
        chainId: 296,
        urls: {
          apiURL: "https://testnet.mirrornode.hedera.com/api/v1",
          browserURL: "https://hashscan.io/testnet"
        }
      },
      {
        network: "hederaMainnet",
        chainId: 295,
        urls: {
          apiURL: "https://mainnet.mirrornode.hedera.com/api/v1",
          browserURL: "https://hashscan.io/mainnet"
        }
      }
    ]
  },
  mocha: {
    timeout: 40000
  }
};
