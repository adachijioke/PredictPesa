// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title Oracle
 * @notice Decentralized oracle system for market resolution
 * @dev Integrates with Hedera Consensus Service for data verification
 */
contract Oracle {
    // Oracle data source
    struct DataSource {
        address provider;
        string name;
        bool isVerified;
        uint256 successfulReports;
        uint256 totalReports;
        uint256 reputationScore;
    }
    
    // Market resolution data
    struct ResolutionData {
        uint256 marketId;
        bool outcome;
        uint256 confidence;
        uint256 timestamp;
        address[] sources;
        bool isFinalized;
        uint256 yesVotes;
        uint256 noVotes;
    }
    
    // Dispute data
    struct Dispute {
        uint256 marketId;
        address disputer;
        bool proposedOutcome;
        string evidence;
        uint256 timestamp;
        bool isResolved;
    }
    
    // State variables
    address public owner;
    address public marketFactory;
    uint256 public minConfidence;
    uint256 public minSources;
    uint256 public disputePeriod;
    
    // Data tracking
    mapping(address => DataSource) public dataSources;
    mapping(uint256 => ResolutionData) public resolutions;
    mapping(uint256 => Dispute[]) public disputes;
    mapping(uint256 => mapping(address => bool)) public hasReported;
    
    address[] public verifiedSources;
    
    // Events
    event DataSourceAdded(address indexed provider, string name);
    event DataSourceVerified(address indexed provider);
    event DataSourceRemoved(address indexed provider);
    event DataSubmitted(
        uint256 indexed marketId,
        address indexed source,
        bool outcome,
        uint256 confidence
    );
    event MarketResolved(uint256 indexed marketId, bool outcome, uint256 confidence);
    event DisputeRaised(
        uint256 indexed marketId,
        address indexed disputer,
        bool proposedOutcome
    );
    event DisputeResolved(uint256 indexed marketId, bool finalOutcome);
    
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    modifier onlyVerifiedSource() {
        require(dataSources[msg.sender].isVerified, "Not verified source");
        _;
    }
    
    modifier onlyFactory() {
        require(msg.sender == marketFactory, "Not factory");
        _;
    }
    
    /**
     * @notice Initialize oracle contract
     */
    constructor(
        address _marketFactory,
        uint256 _minConfidence,
        uint256 _minSources,
        uint256 _disputePeriod
    ) {
        owner = msg.sender;
        marketFactory = _marketFactory;
        minConfidence = _minConfidence; // e.g., 9500 for 95%
        minSources = _minSources; // e.g., 3
        disputePeriod = _disputePeriod; // e.g., 72 hours
    }
    
    /**
     * @notice Add a new data source
     */
    function addDataSource(address _provider, string memory _name) external onlyOwner {
        require(_provider != address(0), "Invalid provider");
        require(!dataSources[_provider].isVerified, "Already exists");
        
        dataSources[_provider] = DataSource({
            provider: _provider,
            name: _name,
            isVerified: false,
            successfulReports: 0,
            totalReports: 0,
            reputationScore: 100
        });
        
        emit DataSourceAdded(_provider, _name);
    }
    
    /**
     * @notice Verify a data source
     */
    function verifyDataSource(address _provider) external onlyOwner {
        require(dataSources[_provider].provider != address(0), "Source does not exist");
        require(!dataSources[_provider].isVerified, "Already verified");
        
        dataSources[_provider].isVerified = true;
        verifiedSources.push(_provider);
        
        emit DataSourceVerified(_provider);
    }
    
    /**
     * @notice Remove a data source
     */
    function removeDataSource(address _provider) external onlyOwner {
        require(dataSources[_provider].isVerified, "Source not verified");
        
        dataSources[_provider].isVerified = false;
        
        // Remove from verified sources array
        for (uint256 i = 0; i < verifiedSources.length; i++) {
            if (verifiedSources[i] == _provider) {
                verifiedSources[i] = verifiedSources[verifiedSources.length - 1];
                verifiedSources.pop();
                break;
            }
        }
        
        emit DataSourceRemoved(_provider);
    }
    
    /**
     * @notice Submit market outcome data
     */
    function submitData(
        uint256 _marketId,
        bool _outcome,
        uint256 _confidence,
        string memory _evidence
    ) external onlyVerifiedSource {
        require(!hasReported[_marketId][msg.sender], "Already reported");
        require(_confidence >= minConfidence, "Confidence too low");
        
        ResolutionData storage resolution = resolutions[_marketId];
        
        // Initialize if first report
        if (resolution.timestamp == 0) {
            resolution.marketId = _marketId;
            resolution.timestamp = block.timestamp;
        }
        
        // Record vote
        if (_outcome) {
            resolution.yesVotes++;
        } else {
            resolution.noVotes++;
        }
        
        resolution.sources.push(msg.sender);
        hasReported[_marketId][msg.sender] = true;
        
        // Update source stats
        dataSources[msg.sender].totalReports++;
        
        emit DataSubmitted(_marketId, msg.sender, _outcome, _confidence);
        
        // Check if we can finalize
        if (resolution.sources.length >= minSources && !resolution.isFinalized) {
            _finalizeResolution(_marketId);
        }
    }
    
    /**
     * @notice Finalize market resolution
     */
    function _finalizeResolution(uint256 _marketId) internal {
        ResolutionData storage resolution = resolutions[_marketId];
        
        // Determine outcome by majority vote
        bool finalOutcome = resolution.yesVotes > resolution.noVotes;
        uint256 totalVotes = resolution.yesVotes + resolution.noVotes;
        uint256 majorityVotes = finalOutcome ? resolution.yesVotes : resolution.noVotes;
        
        // Calculate confidence
        uint256 confidence = (majorityVotes * 10000) / totalVotes;
        
        resolution.outcome = finalOutcome;
        resolution.confidence = confidence;
        resolution.isFinalized = true;
        
        // Update successful reports for sources that voted correctly
        for (uint256 i = 0; i < resolution.sources.length; i++) {
            address source = resolution.sources[i];
            bool sourceVote = i < resolution.yesVotes;
            
            if (sourceVote == finalOutcome) {
                dataSources[source].successfulReports++;
                dataSources[source].reputationScore += 10;
            } else {
                if (dataSources[source].reputationScore > 10) {
                    dataSources[source].reputationScore -= 10;
                }
            }
        }
        
        emit MarketResolved(_marketId, finalOutcome, confidence);
    }
    
    /**
     * @notice Raise a dispute for market resolution
     */
    function raiseDispute(
        uint256 _marketId,
        bool _proposedOutcome,
        string memory _evidence
    ) external payable {
        require(resolutions[_marketId].isFinalized, "Market not resolved");
        require(
            block.timestamp <= resolutions[_marketId].timestamp + disputePeriod,
            "Dispute period ended"
        );
        require(msg.value >= 0.01 ether, "Insufficient dispute stake");
        
        disputes[_marketId].push(Dispute({
            marketId: _marketId,
            disputer: msg.sender,
            proposedOutcome: _proposedOutcome,
            evidence: _evidence,
            timestamp: block.timestamp,
            isResolved: false
        }));
        
        emit DisputeRaised(_marketId, msg.sender, _proposedOutcome);
    }
    
    /**
     * @notice Resolve a dispute (governance function)
     */
    function resolveDispute(
        uint256 _marketId,
        uint256 _disputeIndex,
        bool _isValid
    ) external onlyOwner {
        Dispute storage dispute = disputes[_marketId][_disputeIndex];
        require(!dispute.isResolved, "Already resolved");
        
        dispute.isResolved = true;
        
        if (_isValid) {
            // Update resolution
            resolutions[_marketId].outcome = dispute.proposedOutcome;
            
            // Refund disputer
            (bool success, ) = dispute.disputer.call{value: 0.01 ether}("");
            require(success, "Refund failed");
            
            emit DisputeResolved(_marketId, dispute.proposedOutcome);
        }
    }
    
    /**
     * @notice Get resolution data for a market
     */
    function getResolution(uint256 _marketId) external view returns (
        bool outcome,
        uint256 confidence,
        bool isFinalized,
        uint256 sourceCount
    ) {
        ResolutionData memory resolution = resolutions[_marketId];
        return (
            resolution.outcome,
            resolution.confidence,
            resolution.isFinalized,
            resolution.sources.length
        );
    }
    
    /**
     * @notice Get data source info
     */
    function getDataSource(address _provider) external view returns (
        string memory name,
        bool isVerified,
        uint256 successfulReports,
        uint256 totalReports,
        uint256 reputationScore
    ) {
        DataSource memory source = dataSources[_provider];
        return (
            source.name,
            source.isVerified,
            source.successfulReports,
            source.totalReports,
            source.reputationScore
        );
    }
    
    /**
     * @notice Get number of verified sources
     */
    function getVerifiedSourceCount() external view returns (uint256) {
        return verifiedSources.length;
    }
    
    /**
     * @notice Get dispute count for a market
     */
    function getDisputeCount(uint256 _marketId) external view returns (uint256) {
        return disputes[_marketId].length;
    }
    
    /**
     * @notice Update oracle parameters
     */
    function updateParameters(
        uint256 _minConfidence,
        uint256 _minSources,
        uint256 _disputePeriod
    ) external onlyOwner {
        minConfidence = _minConfidence;
        minSources = _minSources;
        disputePeriod = _disputePeriod;
    }
}
