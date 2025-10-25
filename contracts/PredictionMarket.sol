// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./interfaces/IERC20.sol";

/**
 * @title PredictionMarket
 * @notice Individual prediction market contract for binary outcomes
 * @dev Manages staking, position tokens, and market resolution
 */
contract PredictionMarket {
    // Market states
    enum MarketState { Active, Resolved, Cancelled }
    
    // Market metadata
    uint256 public immutable marketId;
    string public title;
    string public description;
    string public category;
    uint256 public endTime;
    uint256 public minStake;
    uint256 public maxStake;
    address public creator;
    
    // Position tokens
    address public yesBtcToken;
    address public noBtcToken;
    
    // Market state
    MarketState public state;
    bool public outcome; // true = YES, false = NO
    uint256 public totalYesStake;
    uint256 public totalNoStake;
    uint256 public totalStake;
    
    // Governance
    address public oracle;
    uint256 public protocolFeePercentage;
    address public factory;
    
    // User stakes
    mapping(address => uint256) public yesStakes;
    mapping(address => uint256) public noStakes;
    mapping(address => bool) public hasClaimed;
    
    // Events
    event StakePlaced(
        address indexed user,
        bool position,
        uint256 amount,
        uint256 timestamp
    );
    event MarketResolved(bool outcome, uint256 timestamp);
    event RewardClaimed(address indexed user, uint256 amount);
    event MarketCancelled(uint256 timestamp);
    
    // Modifiers
    modifier onlyOracle() {
        require(msg.sender == oracle, "Not oracle");
        _;
    }
    
    modifier onlyFactory() {
        require(msg.sender == factory, "Not factory");
        _;
    }
    
    modifier marketActive() {
        require(state == MarketState.Active, "Market not active");
        require(block.timestamp < endTime, "Market ended");
        _;
    }
    
    modifier marketResolved() {
        require(state == MarketState.Resolved, "Market not resolved");
        _;
    }
    
    /**
     * @notice Initialize prediction market
     */
    constructor(
        uint256 _marketId,
        string memory _title,
        string memory _description,
        string memory _category,
        uint256 _endTime,
        uint256 _minStake,
        uint256 _maxStake,
        address _yesBtcToken,
        address _noBtcToken,
        address _oracle,
        uint256 _protocolFeePercentage,
        address _creator
    ) {
        marketId = _marketId;
        title = _title;
        description = _description;
        category = _category;
        endTime = _endTime;
        minStake = _minStake;
        maxStake = _maxStake;
        yesBtcToken = _yesBtcToken;
        noBtcToken = _noBtcToken;
        oracle = _oracle;
        protocolFeePercentage = _protocolFeePercentage;
        creator = _creator;
        factory = msg.sender;
        state = MarketState.Active;
    }
    
    /**
     * @notice Place a stake on YES or NO position
     * @param _position True for YES, False for NO
     */
    function stake(bool _position) external payable marketActive {
        require(msg.value >= minStake, "Stake below minimum");
        require(msg.value <= maxStake, "Stake above maximum");
        
        if (_position) {
            yesStakes[msg.sender] += msg.value;
            totalYesStake += msg.value;
        } else {
            noStakes[msg.sender] += msg.value;
            totalNoStake += msg.value;
        }
        
        totalStake += msg.value;
        
        // Mint position tokens (1:1 with stake)
        // In production, this would interact with HTS tokens
        
        emit StakePlaced(msg.sender, _position, msg.value, block.timestamp);
    }
    
    /**
     * @notice Resolve the market with final outcome
     * @param _outcome True for YES, False for NO
     */
    function resolve(bool _outcome) external onlyOracle {
        require(state == MarketState.Active, "Market not active");
        require(block.timestamp >= endTime, "Market not ended");
        
        state = MarketState.Resolved;
        outcome = _outcome;
        
        emit MarketResolved(_outcome, block.timestamp);
    }
    
    /**
     * @notice Claim rewards after market resolution
     */
    function claimReward() external marketResolved {
        require(!hasClaimed[msg.sender], "Already claimed");
        
        uint256 userStake = outcome ? yesStakes[msg.sender] : noStakes[msg.sender];
        require(userStake > 0, "No winning stake");
        
        uint256 winningPool = outcome ? totalYesStake : totalNoStake;
        uint256 losingPool = outcome ? totalNoStake : totalYesStake;
        
        // Calculate reward: user's share of winning pool + proportional share of losing pool
        uint256 reward = userStake + (userStake * losingPool) / winningPool;
        
        // Deduct protocol fee
        uint256 protocolFee = (reward * protocolFeePercentage) / 10000;
        uint256 netReward = reward - protocolFee;
        
        hasClaimed[msg.sender] = true;
        
        // Transfer reward
        (bool success, ) = msg.sender.call{value: netReward}("");
        require(success, "Transfer failed");
        
        emit RewardClaimed(msg.sender, netReward);
    }
    
    /**
     * @notice Cancel market (emergency only)
     */
    function cancel() external onlyFactory {
        require(state == MarketState.Active, "Market not active");
        state = MarketState.Cancelled;
        emit MarketCancelled(block.timestamp);
    }
    
    /**
     * @notice Refund stakes if market is cancelled
     */
    function refund() external {
        require(state == MarketState.Cancelled, "Market not cancelled");
        require(!hasClaimed[msg.sender], "Already refunded");
        
        uint256 totalUserStake = yesStakes[msg.sender] + noStakes[msg.sender];
        require(totalUserStake > 0, "No stake to refund");
        
        hasClaimed[msg.sender] = true;
        
        (bool success, ) = msg.sender.call{value: totalUserStake}("");
        require(success, "Refund failed");
    }
    
    /**
     * @notice Get market info
     */
    function getMarketInfo() external view returns (
        string memory _title,
        string memory _category,
        uint256 _endTime,
        MarketState _state,
        uint256 _totalYesStake,
        uint256 _totalNoStake,
        uint256 _totalStake
    ) {
        return (
            title,
            category,
            endTime,
            state,
            totalYesStake,
            totalNoStake,
            totalStake
        );
    }
    
    /**
     * @notice Get user position
     */
    function getUserPosition(address _user) external view returns (
        uint256 _yesStake,
        uint256 _noStake,
        bool _hasClaimed
    ) {
        return (
            yesStakes[_user],
            noStakes[_user],
            hasClaimed[_user]
        );
    }
    
    /**
     * @notice Calculate current odds
     */
    function getOdds() external view returns (uint256 yesOdds, uint256 noOdds) {
        if (totalStake == 0) {
            return (5000, 5000); // 50/50 if no stakes
        }
        
        yesOdds = (totalYesStake * 10000) / totalStake;
        noOdds = (totalNoStake * 10000) / totalStake;
        
        return (yesOdds, noOdds);
    }
    
    /**
     * @notice Calculate potential payout for a stake
     */
    function calculatePayout(bool _position, uint256 _amount) external view returns (uint256) {
        uint256 winningPool = _position ? totalYesStake : totalNoStake;
        uint256 losingPool = _position ? totalNoStake : totalYesStake;
        
        if (winningPool == 0) {
            return _amount; // Return stake if no competition
        }
        
        uint256 newWinningPool = winningPool + _amount;
        uint256 reward = _amount + (_amount * losingPool) / newWinningPool;
        uint256 protocolFee = (reward * protocolFeePercentage) / 10000;
        
        return reward - protocolFee;
    }
}
