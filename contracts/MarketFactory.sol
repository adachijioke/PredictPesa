// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./PredictionMarket.sol";
import "./interfaces/IHederaTokenService.sol";

/**
 * @title MarketFactory
 * @notice Factory contract for creating and managing prediction markets on Hedera
 * @dev Integrates with Hedera Token Service (HTS) for position tokens
 */
contract MarketFactory {
    // Hedera Token Service interface
    IHederaTokenService internal constant HTS = IHederaTokenService(0x0000000000000000000000000000000000000167);
    
    // State variables
    address public owner;
    address public oracle;
    uint256 public marketCount;
    uint256 public protocolFeePercentage; // In basis points (100 = 1%)
    
    // Market tracking
    mapping(uint256 => address) public markets;
    mapping(address => bool) public isMarket;
    mapping(string => uint256) public categoryMarketCount;
    
    // Events
    event MarketCreated(
        uint256 indexed marketId,
        address indexed marketAddress,
        string title,
        string category,
        uint256 endTime,
        address creator
    );
    event OracleUpdated(address indexed oldOracle, address indexed newOracle);
    event ProtocolFeeUpdated(uint256 oldFee, uint256 newFee);
    event MarketResolved(uint256 indexed marketId, bool outcome);
    
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    modifier onlyOracle() {
        require(msg.sender == oracle, "Not oracle");
        _;
    }
    
    /**
     * @notice Initialize the factory contract
     * @param _oracle Address of the oracle contract
     * @param _protocolFeePercentage Protocol fee in basis points
     */
    constructor(address _oracle, uint256 _protocolFeePercentage) {
        require(_oracle != address(0), "Invalid oracle address");
        require(_protocolFeePercentage <= 1000, "Fee too high"); // Max 10%
        
        owner = msg.sender;
        oracle = _oracle;
        protocolFeePercentage = _protocolFeePercentage;
    }
    
    /**
     * @notice Create a new prediction market
     * @param _title Market title
     * @param _description Market description
     * @param _category Market category
     * @param _endTime Market end timestamp
     * @param _minStake Minimum stake amount
     * @param _maxStake Maximum stake amount
     * @return marketId The ID of the created market
     */
    function createMarket(
        string memory _title,
        string memory _description,
        string memory _category,
        uint256 _endTime,
        uint256 _minStake,
        uint256 _maxStake
    ) external returns (uint256 marketId) {
        require(_endTime > block.timestamp, "Invalid end time");
        require(_minStake > 0 && _maxStake > _minStake, "Invalid stake limits");
        require(bytes(_title).length > 0, "Empty title");
        
        marketId = marketCount++;
        
        // Create position tokens using HTS
        (address yesBtcToken, address noBtcToken) = _createPositionTokens(
            _title,
            marketId
        );
        
        // Deploy new market contract
        PredictionMarket market = new PredictionMarket(
            marketId,
            _title,
            _description,
            _category,
            _endTime,
            _minStake,
            _maxStake,
            yesBtcToken,
            noBtcToken,
            oracle,
            protocolFeePercentage,
            msg.sender
        );
        
        address marketAddress = address(market);
        markets[marketId] = marketAddress;
        isMarket[marketAddress] = true;
        categoryMarketCount[_category]++;
        
        emit MarketCreated(
            marketId,
            marketAddress,
            _title,
            _category,
            _endTime,
            msg.sender
        );
        
        return marketId;
    }
    
    /**
     * @notice Create position tokens for a market using Hedera Token Service
     * @param _marketTitle Market title for token naming
     * @param _marketId Market ID
     * @return yesBtcToken Address of YES position token
     * @return noBtcToken Address of NO position token
     */
    function _createPositionTokens(
        string memory _marketTitle,
        uint256 _marketId
    ) internal returns (address yesBtcToken, address noBtcToken) {
        // Create YES token
        string memory yesName = string(abi.encodePacked("YES-", _marketTitle));
        string memory yesSymbol = string(abi.encodePacked("YES", _uint2str(_marketId)));
        
        // Create NO token
        string memory noName = string(abi.encodePacked("NO-", _marketTitle));
        string memory noSymbol = string(abi.encodePacked("NO", _uint2str(_marketId)));
        
        // Note: In production, integrate with actual HTS token creation
        // For now, return placeholder addresses
        // This would use HTS precompile to create fungible tokens
        
        yesBtcToken = address(uint160(uint256(keccak256(abi.encodePacked(yesName, block.timestamp)))));
        noBtcToken = address(uint160(uint256(keccak256(abi.encodePacked(noName, block.timestamp)))));
        
        return (yesBtcToken, noBtcToken);
    }
    
    /**
     * @notice Resolve a market with outcome
     * @param _marketId Market ID to resolve
     * @param _outcome True for YES, False for NO
     */
    function resolveMarket(uint256 _marketId, bool _outcome) external onlyOracle {
        address marketAddress = markets[_marketId];
        require(marketAddress != address(0), "Market does not exist");
        
        PredictionMarket market = PredictionMarket(marketAddress);
        market.resolve(_outcome);
        
        emit MarketResolved(_marketId, _outcome);
    }
    
    /**
     * @notice Update oracle address
     * @param _newOracle New oracle address
     */
    function updateOracle(address _newOracle) external onlyOwner {
        require(_newOracle != address(0), "Invalid oracle address");
        address oldOracle = oracle;
        oracle = _newOracle;
        emit OracleUpdated(oldOracle, _newOracle);
    }
    
    /**
     * @notice Update protocol fee percentage
     * @param _newFee New fee in basis points
     */
    function updateProtocolFee(uint256 _newFee) external onlyOwner {
        require(_newFee <= 1000, "Fee too high"); // Max 10%
        uint256 oldFee = protocolFeePercentage;
        protocolFeePercentage = _newFee;
        emit ProtocolFeeUpdated(oldFee, _newFee);
    }
    
    /**
     * @notice Get market address by ID
     * @param _marketId Market ID
     * @return Market contract address
     */
    function getMarket(uint256 _marketId) external view returns (address) {
        return markets[_marketId];
    }
    
    /**
     * @notice Get total number of markets
     * @return Total market count
     */
    function getMarketCount() external view returns (uint256) {
        return marketCount;
    }
    
    /**
     * @notice Get market count by category
     * @param _category Category name
     * @return Market count in category
     */
    function getCategoryMarketCount(string memory _category) external view returns (uint256) {
        return categoryMarketCount[_category];
    }
    
    /**
     * @notice Convert uint to string
     * @param _i Number to convert
     * @return String representation
     */
    function _uint2str(uint256 _i) internal pure returns (string memory) {
        if (_i == 0) {
            return "0";
        }
        uint256 j = _i;
        uint256 len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint256 k = len;
        while (_i != 0) {
            k = k - 1;
            uint8 temp = (48 + uint8(_i - _i / 10 * 10));
            bytes1 b1 = bytes1(temp);
            bstr[k] = b1;
            _i /= 10;
        }
        return string(bstr);
    }
}
