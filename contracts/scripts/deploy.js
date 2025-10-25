const hre = require("hardhat");
const { ethers } = require("hardhat");

async function main() {
  console.log("🚀 Starting PredictPesa contract deployment on Hedera...\n");

  // Get deployer account
  const [deployer] = await ethers.getSigners();
  console.log("📝 Deploying contracts with account:", deployer.address);
  
  const balance = await ethers.provider.getBalance(deployer.address);
  console.log("💰 Account balance:", ethers.formatEther(balance), "HBAR\n");

  // Deploy Oracle contract
  console.log("📜 Deploying Oracle contract...");
  const Oracle = await ethers.getContractFactory("Oracle");
  
  const minConfidence = 9500; // 95%
  const minSources = 3;
  const disputePeriod = 72 * 60 * 60; // 72 hours in seconds
  
  // We'll set factory address after deploying MarketFactory
  const tempFactoryAddress = deployer.address;
  
  const oracle = await Oracle.deploy(
    tempFactoryAddress,
    minConfidence,
    minSources,
    disputePeriod
  );
  await oracle.waitForDeployment();
  const oracleAddress = await oracle.getAddress();
  
  console.log("✅ Oracle deployed to:", oracleAddress);
  console.log("   - Min Confidence:", minConfidence / 100, "%");
  console.log("   - Min Sources:", minSources);
  console.log("   - Dispute Period:", disputePeriod / 3600, "hours\n");

  // Deploy MarketFactory contract
  console.log("📜 Deploying MarketFactory contract...");
  const MarketFactory = await ethers.getContractFactory("MarketFactory");
  
  const protocolFeePercentage = 10; // 0.1% in basis points
  
  const marketFactory = await MarketFactory.deploy(
    oracleAddress,
    protocolFeePercentage
  );
  await marketFactory.waitForDeployment();
  const factoryAddress = await marketFactory.getAddress();
  
  console.log("✅ MarketFactory deployed to:", factoryAddress);
  console.log("   - Protocol Fee:", protocolFeePercentage / 100, "%\n");

  // Update Oracle with correct factory address
  console.log("🔄 Updating Oracle with MarketFactory address...");
  // Note: You would need to add a setFactory function to Oracle contract
  // or redeploy Oracle with correct factory address
  console.log("⚠️  Manual step: Update Oracle factory address to:", factoryAddress, "\n");

  // Deploy sample AMM Pool (optional)
  console.log("📜 Deploying sample AMMPool contract...");
  const AMMPool = await ethers.getContractFactory("AMMPool");
  
  // Create dummy token addresses for demonstration
  const dummyTokenA = "0x0000000000000000000000000000000000000001";
  const dummyTokenB = "0x0000000000000000000000000000000000000002";
  
  const ammPool = await AMMPool.deploy(dummyTokenA, dummyTokenB);
  await ammPool.waitForDeployment();
  const ammPoolAddress = await ammPool.getAddress();
  
  console.log("✅ AMMPool deployed to:", ammPoolAddress);
  console.log("   - Token A:", dummyTokenA);
  console.log("   - Token B:", dummyTokenB, "\n");

  // Summary
  console.log("=" .repeat(60));
  console.log("🎉 DEPLOYMENT SUMMARY");
  console.log("=" .repeat(60));
  console.log("Network:", hre.network.name);
  console.log("Deployer:", deployer.address);
  console.log("\n📋 Contract Addresses:");
  console.log("   Oracle:        ", oracleAddress);
  console.log("   MarketFactory: ", factoryAddress);
  console.log("   AMMPool:       ", ammPoolAddress);
  console.log("=" .repeat(60));

  // Save deployment info
  const deploymentInfo = {
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: {
      Oracle: {
        address: oracleAddress,
        minConfidence,
        minSources,
        disputePeriod
      },
      MarketFactory: {
        address: factoryAddress,
        protocolFeePercentage
      },
      AMMPool: {
        address: ammPoolAddress,
        tokenA: dummyTokenA,
        tokenB: dummyTokenB
      }
    }
  };

  const fs = require("fs");
  const path = require("path");
  
  const deploymentsDir = path.join(__dirname, "..", "deployments");
  if (!fs.existsSync(deploymentsDir)) {
    fs.mkdirSync(deploymentsDir);
  }
  
  const filename = `${hre.network.name}-${Date.now()}.json`;
  const filepath = path.join(deploymentsDir, filename);
  
  fs.writeFileSync(filepath, JSON.stringify(deploymentInfo, null, 2));
  console.log("\n💾 Deployment info saved to:", filepath);

  // Verification instructions
  if (hre.network.name !== "localhost" && hre.network.name !== "hardhat") {
    console.log("\n🔍 To verify contracts on Hashscan, run:");
    console.log(`   npx hardhat verify --network ${hre.network.name} ${oracleAddress} "${tempFactoryAddress}" ${minConfidence} ${minSources} ${disputePeriod}`);
    console.log(`   npx hardhat verify --network ${hre.network.name} ${factoryAddress} "${oracleAddress}" ${protocolFeePercentage}`);
    console.log(`   npx hardhat verify --network ${hre.network.name} ${ammPoolAddress} "${dummyTokenA}" "${dummyTokenB}"`);
  }

  console.log("\n✨ Deployment complete!\n");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  });
