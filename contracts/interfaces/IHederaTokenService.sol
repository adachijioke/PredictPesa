// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title IHederaTokenService
 * @notice Interface for Hedera Token Service (HTS) precompiled contract
 * @dev Hedera-specific token operations at address 0x167
 */
interface IHederaTokenService {
    // Token creation structures
    struct HederaToken {
        string name;
        string symbol;
        address treasury;
        string memo;
        bool tokenSupplyType;
        int64 maxSupply;
        bool freezeDefault;
        TokenKey[] tokenKeys;
        Expiry expiry;
    }
    
    struct TokenKey {
        uint256 keyType;
        KeyValue key;
    }
    
    struct KeyValue {
        bool inheritAccountKey;
        address contractId;
        bytes ed25519;
        bytes ECDSA_secp256k1;
        address delegatableContractId;
    }
    
    struct Expiry {
        int64 second;
        address autoRenewAccount;
        int64 autoRenewPeriod;
    }
    
    struct FixedFee {
        int64 amount;
        address tokenId;
        bool useHbarsForPayment;
        bool useCurrentTokenForPayment;
        address feeCollector;
    }
    
    struct FractionalFee {
        int64 numerator;
        int64 denominator;
        int64 minimumAmount;
        int64 maximumAmount;
        bool netOfTransfers;
        address feeCollector;
    }
    
    struct RoyaltyFee {
        int64 numerator;
        int64 denominator;
        int64 amount;
        address tokenId;
        bool useHbarsForPayment;
        address feeCollector;
    }
    
    /**
     * @notice Create a fungible token
     */
    function createFungibleToken(
        HederaToken memory token,
        int64 initialTotalSupply,
        int32 decimals
    ) external payable returns (int256 responseCode, address tokenAddress);
    
    /**
     * @notice Create a non-fungible token
     */
    function createNonFungibleToken(
        HederaToken memory token
    ) external payable returns (int256 responseCode, address tokenAddress);
    
    /**
     * @notice Mint tokens
     */
    function mintToken(
        address token,
        int64 amount,
        bytes[] memory metadata
    ) external returns (int256 responseCode, int64 newTotalSupply, int64[] memory serialNumbers);
    
    /**
     * @notice Burn tokens
     */
    function burnToken(
        address token,
        int64 amount,
        int64[] memory serialNumbers
    ) external returns (int256 responseCode, int64 newTotalSupply);
    
    /**
     * @notice Associate token with account
     */
    function associateToken(
        address account,
        address token
    ) external returns (int256 responseCode);
    
    /**
     * @notice Associate multiple tokens with account
     */
    function associateTokens(
        address account,
        address[] memory tokens
    ) external returns (int256 responseCode);
    
    /**
     * @notice Dissociate token from account
     */
    function dissociateToken(
        address account,
        address token
    ) external returns (int256 responseCode);
    
    /**
     * @notice Transfer tokens
     */
    function transferToken(
        address token,
        address sender,
        address recipient,
        int64 amount
    ) external returns (int256 responseCode);
    
    /**
     * @notice Transfer NFT
     */
    function transferNFT(
        address token,
        address sender,
        address recipient,
        int64 serialNumber
    ) external returns (int256 responseCode);
    
    /**
     * @notice Get token info
     */
    function getTokenInfo(
        address token
    ) external returns (int256 responseCode, HederaToken memory tokenInfo);
    
    /**
     * @notice Get fungible token info
     */
    function getFungibleTokenInfo(
        address token
    ) external returns (int256 responseCode, HederaToken memory tokenInfo, int32 decimals);
    
    /**
     * @notice Approve token allowance
     */
    function approve(
        address token,
        address spender,
        uint256 amount
    ) external returns (int256 responseCode);
    
    /**
     * @notice Get token allowance
     */
    function allowance(
        address token,
        address owner,
        address spender
    ) external returns (int256 responseCode, uint256 allowance);
    
    /**
     * @notice Check if token is frozen
     */
    function isFrozen(
        address token,
        address account
    ) external returns (int256 responseCode, bool frozen);
    
    /**
     * @notice Check if token KYC is granted
     */
    function isKyc(
        address token,
        address account
    ) external returns (int256 responseCode, bool kycGranted);
    
    /**
     * @notice Delete token
     */
    function deleteToken(
        address token
    ) external returns (int256 responseCode);
    
    /**
     * @notice Update token info
     */
    function updateTokenInfo(
        address token,
        HederaToken memory tokenInfo
    ) external returns (int256 responseCode);
    
    /**
     * @notice Update token keys
     */
    function updateTokenKeys(
        address token,
        TokenKey[] memory keys
    ) external returns (int256 responseCode);
}
