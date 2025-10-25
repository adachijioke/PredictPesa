const hre = require("hardhat");
const { ethers } = require("hardhat");

/**
 * Interactive script to interact with deployed PredictPesa contracts
 * Usage: node scripts/interact.js
 */

async function main() {
  console.log("🔗 PredictPesa Contract Interaction Script\n");

  // Load deployment info
  const fs = require("fs");
  const path = require("path");
  
  const deploymentsDir = path.join(__dirname, "..", "deployments");
  const files = fs.readdirSync(deploymentsDir).filter(f => f.endsWith('.json'));
  
  if (files.length === 0) {
    console.log("❌ No deployment found. Please deploy contracts first.");
    return;
  }
  
  // Get latest deployment
  const latestDeployment = files.sort().reverse()[0];
  const deploymentPath = path.join(deploymentsDir, latestDeployment);
  const deployment = JSON.parse(fs.readFileSync(deploymentPath, 'utf8'));
  
  console.log("📋 Using deployment:", latestDeployment);
  console.log("Network:", deployment.network);
  console.log("Deployed at:", deployment.timestamp, "\n");

  const [signer] = await ethers.getSigners();
  console.log("👤 Interacting as:", signer.address, "\n");

  // Get contract instances
  const marketFactoryAddress = deployment.contracts.MarketFactory.address;
  const oracleAddress = deployment.contracts.Oracle.address;

  const MarketFactory = await ethers.getContractFactory("MarketFactory");
  const marketFactory = MarketFactory.attach(marketFactoryAddress);

  const Oracle = await ethers.getContractFactory("Oracle");
  const oracle = Oracle.attach(oracleAddress);

  // Example 1: Create a new market
  console.log("=" .repeat(60));
  console.log("📊 EXAMPLE 1: Create a New Prediction Market");
  console.log("=" .repeat(60));

  const marketTitle = "Will Bitcoin reach $100,000 by end of 2025?";
  const marketDescription = "This market resolves to YES if Bitcoin (BTC) trades at or above $100,000 USD on any major exchange before December 31, 2025 23:59:59 UTC.";
  const category = "crypto";
  const endTime = Math.floor(Date.now() / 1000) + (365 * 24 * 60 * 60); // 1 year from now
  const minStake = ethers.parseEther("0.001"); // 0.001 HBAR
  const maxStake = ethers.parseEther("10"); // 10 HBAR

  console.log("\n📝 Market Details:");
  console.log("   Title:", marketTitle);
  console.log("   Category:", category);
  console.log("   End Time:", new Date(endTime * 1000).toISOString());
  console.log("   Min Stake:", ethers.formatEther(minStake), "HBAR");
  console.log("   Max Stake:", ethers.formatEther(maxStake), "HBAR");

  try {
    console.log("\n🚀 Creating market...");
    const tx = await marketFactory.createMarket(
      marketTitle,
      marketDescription,
      category,
      endTime,
      minStake,
      maxStake
    );
    
    console.log("⏳ Transaction submitted:", tx.hash);
    const receipt = await tx.wait();
    console.log("✅ Market created! Gas used:", receipt.gasUsed.toString());

    // Get market ID from event
    const event = receipt.logs.find(log => {
      try {
        return marketFactory.interface.parseLog(log).name === "MarketCreated";
      } catch {
        return false;
      }
    });

    if (event) {
      const parsedEvent = marketFactory.interface.parseLog(event);
      const marketId = parsedEvent.args.marketId;
      const marketAddress = parsedEvent.args.marketAddress;
      
      console.log("   Market ID:", marketId.toString());
      console.log("   Market Address:", marketAddress);
    }
  } catch (error) {
    console.log("❌ Error creating market:", error.message);
  }

  // Example 2: Get market count
  console.log("\n" + "=" .repeat(60));
  console.log("📈 EXAMPLE 2: Get Market Statistics");
  console.log("=" .repeat(60));

  try {
    const totalMarkets = await marketFactory.getMarketCount();
    console.log("\n📊 Total Markets:", totalMarkets.toString());

    const cryptoMarkets = await marketFactory.getCategoryMarketCount("crypto");
    console.log("   Crypto Markets:", cryptoMarkets.toString());

    const sportsMarkets = await marketFactory.getCategoryMarketCount("sports");
    console.log("   Sports Markets:", sportsMarkets.toString());
  } catch (error) {
    console.log("❌ Error getting stats:", error.message);
  }

  // Example 3: Oracle data source management
  console.log("\n" + "=" .repeat(60));
  console.log("🔮 EXAMPLE 3: Oracle Data Source Management");
  console.log("=" .repeat(60));

  try {
    const verifiedSourceCount = await oracle.getVerifiedSourceCount();
    console.log("\n📡 Verified Data Sources:", verifiedSourceCount.toString());

    // Example: Add a data source (owner only)
    const newSourceAddress = "0x1234567890123456789012345678901234567890";
    const sourceName = "Chainlink Price Feed";
    
    console.log("\n📝 To add a new data source:");
    console.log("   Address:", newSourceAddress);
    console.log("   Name:", sourceName);
    console.log("   (Run as owner to execute)");
  } catch (error) {
    console.log("❌ Error with oracle:", error.message);
  }

  // Example 4: Get market info
  console.log("\n" + "=" .repeat(60));
  console.log("🔍 EXAMPLE 4: Query Market Information");
  console.log("=" .repeat(60));

  try {
    const marketCount = await marketFactory.getMarketCount();
    
    if (marketCount > 0) {
      const marketAddress = await marketFactory.getMarket(0);
      console.log("\n📊 Market #0:");
      console.log("   Address:", marketAddress);

      // Get market contract instance
      const PredictionMarket = await ethers.getContractFactory("PredictionMarket");
      const market = PredictionMarket.attach(marketAddress);

      const marketInfo = await market.getMarketInfo();
      console.log("   Title:", marketInfo._title);
      console.log("   Category:", marketInfo._category);
      console.log("   End Time:", new Date(Number(marketInfo._endTime) * 1000).toISOString());
      console.log("   State:", ["Active", "Resolved", "Cancelled"][marketInfo._state]);
      console.log("   Total YES Stake:", ethers.formatEther(marketInfo._totalYesStake), "HBAR");
      console.log("   Total NO Stake:", ethers.formatEther(marketInfo._totalNoStake), "HBAR");
      console.log("   Total Stake:", ethers.formatEther(marketInfo._totalStake), "HBAR");

      // Get current odds
      const odds = await market.getOdds();
      console.log("   YES Odds:", (Number(odds.yesOdds) / 100).toFixed(2), "%");
      console.log("   NO Odds:", (Number(odds.noOdds) / 100).toFixed(2), "%");
    } else {
      console.log("\n⚠️  No markets created yet.");
    }
  } catch (error) {
    console.log("❌ Error querying market:", error.message);
  }

  console.log("\n" + "=" .repeat(60));
  console.log("✨ Interaction complete!");
  console.log("=" .repeat(60) + "\n");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Script failed:", error);
    process.exit(1);
  });
