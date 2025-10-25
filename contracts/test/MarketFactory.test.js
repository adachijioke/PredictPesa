const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("MarketFactory", function () {
  let marketFactory;
  let oracle;
  let owner;
  let addr1;
  let addr2;

  const PROTOCOL_FEE = 10; // 0.1%
  const MIN_CONFIDENCE = 9500;
  const MIN_SOURCES = 3;
  const DISPUTE_PERIOD = 72 * 60 * 60;

  beforeEach(async function () {
    [owner, addr1, addr2] = await ethers.getSigners();

    // Deploy Oracle first
    const Oracle = await ethers.getContractFactory("Oracle");
    oracle = await Oracle.deploy(
      owner.address, // Temporary factory address
      MIN_CONFIDENCE,
      MIN_SOURCES,
      DISPUTE_PERIOD
    );
    await oracle.waitForDeployment();

    // Deploy MarketFactory
    const MarketFactory = await ethers.getContractFactory("MarketFactory");
    marketFactory = await MarketFactory.deploy(
      await oracle.getAddress(),
      PROTOCOL_FEE
    );
    await marketFactory.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      expect(await marketFactory.owner()).to.equal(owner.address);
    });

    it("Should set the correct oracle address", async function () {
      expect(await marketFactory.oracle()).to.equal(await oracle.getAddress());
    });

    it("Should set the correct protocol fee", async function () {
      expect(await marketFactory.protocolFeePercentage()).to.equal(PROTOCOL_FEE);
    });

    it("Should initialize market count to 0", async function () {
      expect(await marketFactory.marketCount()).to.equal(0);
    });
  });

  describe("Market Creation", function () {
    it("Should create a new market", async function () {
      const title = "Will Bitcoin reach $100k in 2025?";
      const description = "Bitcoin price prediction for 2025";
      const category = "crypto";
      const endTime = Math.floor(Date.now() / 1000) + 86400; // 1 day from now
      const minStake = ethers.parseEther("0.001");
      const maxStake = ethers.parseEther("1.0");

      await expect(
        marketFactory.createMarket(
          title,
          description,
          category,
          endTime,
          minStake,
          maxStake
        )
      ).to.emit(marketFactory, "MarketCreated");

      expect(await marketFactory.marketCount()).to.equal(1);
    });

    it("Should fail with invalid end time", async function () {
      const pastTime = Math.floor(Date.now() / 1000) - 3600; // 1 hour ago

      await expect(
        marketFactory.createMarket(
          "Test Market",
          "Description",
          "test",
          pastTime,
          ethers.parseEther("0.001"),
          ethers.parseEther("1.0")
        )
      ).to.be.revertedWith("Invalid end time");
    });

    it("Should fail with invalid stake limits", async function () {
      const endTime = Math.floor(Date.now() / 1000) + 86400;

      await expect(
        marketFactory.createMarket(
          "Test Market",
          "Description",
          "test",
          endTime,
          ethers.parseEther("1.0"),
          ethers.parseEther("0.001")
        )
      ).to.be.revertedWith("Invalid stake limits");
    });

    it("Should track category market count", async function () {
      const category = "sports";
      const endTime = Math.floor(Date.now() / 1000) + 86400;

      await marketFactory.createMarket(
        "Market 1",
        "Description",
        category,
        endTime,
        ethers.parseEther("0.001"),
        ethers.parseEther("1.0")
      );

      expect(await marketFactory.getCategoryMarketCount(category)).to.equal(1);

      await marketFactory.createMarket(
        "Market 2",
        "Description",
        category,
        endTime,
        ethers.parseEther("0.001"),
        ethers.parseEther("1.0")
      );

      expect(await marketFactory.getCategoryMarketCount(category)).to.equal(2);
    });
  });

  describe("Oracle Management", function () {
    it("Should update oracle address", async function () {
      const newOracle = addr1.address;

      await expect(marketFactory.updateOracle(newOracle))
        .to.emit(marketFactory, "OracleUpdated")
        .withArgs(await oracle.getAddress(), newOracle);

      expect(await marketFactory.oracle()).to.equal(newOracle);
    });

    it("Should fail to update oracle with zero address", async function () {
      await expect(
        marketFactory.updateOracle(ethers.ZeroAddress)
      ).to.be.revertedWith("Invalid oracle address");
    });

    it("Should fail to update oracle from non-owner", async function () {
      await expect(
        marketFactory.connect(addr1).updateOracle(addr2.address)
      ).to.be.revertedWith("Not owner");
    });
  });

  describe("Protocol Fee Management", function () {
    it("Should update protocol fee", async function () {
      const newFee = 20; // 0.2%

      await expect(marketFactory.updateProtocolFee(newFee))
        .to.emit(marketFactory, "ProtocolFeeUpdated")
        .withArgs(PROTOCOL_FEE, newFee);

      expect(await marketFactory.protocolFeePercentage()).to.equal(newFee);
    });

    it("Should fail to set fee above maximum", async function () {
      await expect(
        marketFactory.updateProtocolFee(1001) // > 10%
      ).to.be.revertedWith("Fee too high");
    });

    it("Should fail to update fee from non-owner", async function () {
      await expect(
        marketFactory.connect(addr1).updateProtocolFee(20)
      ).to.be.revertedWith("Not owner");
    });
  });

  describe("Market Retrieval", function () {
    it("Should get market address by ID", async function () {
      const endTime = Math.floor(Date.now() / 1000) + 86400;

      await marketFactory.createMarket(
        "Test Market",
        "Description",
        "test",
        endTime,
        ethers.parseEther("0.001"),
        ethers.parseEther("1.0")
      );

      const marketAddress = await marketFactory.getMarket(0);
      expect(marketAddress).to.not.equal(ethers.ZeroAddress);
    });

    it("Should return zero address for non-existent market", async function () {
      const marketAddress = await marketFactory.getMarket(999);
      expect(marketAddress).to.equal(ethers.ZeroAddress);
    });
  });
});
