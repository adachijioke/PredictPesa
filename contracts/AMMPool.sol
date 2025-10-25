// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./interfaces/IERC20.sol";

/**
 * @title AMMPool
 * @notice Automated Market Maker for prediction market position tokens
 * @dev Enables secondary trading of yesBTC/noBTC tokens with constant product formula
 */
contract AMMPool {
    // Pool state
    address public tokenA; // yesBTC
    address public tokenB; // noBTC
    uint256 public reserveA;
    uint256 public reserveB;
    uint256 public totalLiquidity;
    
    // LP token tracking
    mapping(address => uint256) public liquidityBalance;
    
    // Fee configuration
    uint256 public constant FEE_PERCENTAGE = 30; // 0.3% fee
    uint256 public constant FEE_DENOMINATOR = 10000;
    
    // Events
    event LiquidityAdded(
        address indexed provider,
        uint256 amountA,
        uint256 amountB,
        uint256 liquidity
    );
    event LiquidityRemoved(
        address indexed provider,
        uint256 amountA,
        uint256 amountB,
        uint256 liquidity
    );
    event Swap(
        address indexed user,
        address indexed tokenIn,
        address indexed tokenOut,
        uint256 amountIn,
        uint256 amountOut
    );
    
    /**
     * @notice Initialize AMM pool
     */
    constructor(address _tokenA, address _tokenB) {
        require(_tokenA != address(0) && _tokenB != address(0), "Invalid tokens");
        tokenA = _tokenA;
        tokenB = _tokenB;
    }
    
    /**
     * @notice Add liquidity to the pool
     */
    function addLiquidity(
        uint256 _amountA,
        uint256 _amountB
    ) external returns (uint256 liquidity) {
        require(_amountA > 0 && _amountB > 0, "Invalid amounts");
        
        // Transfer tokens to pool
        IERC20(tokenA).transferFrom(msg.sender, address(this), _amountA);
        IERC20(tokenB).transferFrom(msg.sender, address(this), _amountB);
        
        // Calculate liquidity tokens to mint
        if (totalLiquidity == 0) {
            // Initial liquidity
            liquidity = sqrt(_amountA * _amountB);
        } else {
            // Proportional liquidity
            uint256 liquidityA = (_amountA * totalLiquidity) / reserveA;
            uint256 liquidityB = (_amountB * totalLiquidity) / reserveB;
            liquidity = liquidityA < liquidityB ? liquidityA : liquidityB;
        }
        
        require(liquidity > 0, "Insufficient liquidity minted");
        
        // Update state
        liquidityBalance[msg.sender] += liquidity;
        totalLiquidity += liquidity;
        reserveA += _amountA;
        reserveB += _amountB;
        
        emit LiquidityAdded(msg.sender, _amountA, _amountB, liquidity);
        
        return liquidity;
    }
    
    /**
     * @notice Remove liquidity from the pool
     */
    function removeLiquidity(
        uint256 _liquidity
    ) external returns (uint256 amountA, uint256 amountB) {
        require(_liquidity > 0, "Invalid liquidity");
        require(liquidityBalance[msg.sender] >= _liquidity, "Insufficient balance");
        
        // Calculate token amounts to return
        amountA = (_liquidity * reserveA) / totalLiquidity;
        amountB = (_liquidity * reserveB) / totalLiquidity;
        
        require(amountA > 0 && amountB > 0, "Insufficient liquidity burned");
        
        // Update state
        liquidityBalance[msg.sender] -= _liquidity;
        totalLiquidity -= _liquidity;
        reserveA -= amountA;
        reserveB -= amountB;
        
        // Transfer tokens back
        IERC20(tokenA).transfer(msg.sender, amountA);
        IERC20(tokenB).transfer(msg.sender, amountB);
        
        emit LiquidityRemoved(msg.sender, amountA, amountB, _liquidity);
        
        return (amountA, amountB);
    }
    
    /**
     * @notice Swap tokens using constant product formula
     */
    function swap(
        address _tokenIn,
        uint256 _amountIn,
        uint256 _minAmountOut
    ) external returns (uint256 amountOut) {
        require(_amountIn > 0, "Invalid input amount");
        require(
            _tokenIn == tokenA || _tokenIn == tokenB,
            "Invalid input token"
        );
        
        bool isTokenA = _tokenIn == tokenA;
        address tokenOut = isTokenA ? tokenB : tokenA;
        uint256 reserveIn = isTokenA ? reserveA : reserveB;
        uint256 reserveOut = isTokenA ? reserveB : reserveA;
        
        // Transfer input tokens
        IERC20(_tokenIn).transferFrom(msg.sender, address(this), _amountIn);
        
        // Calculate output amount with fee
        uint256 amountInWithFee = _amountIn * (FEE_DENOMINATOR - FEE_PERCENTAGE);
        amountOut = (amountInWithFee * reserveOut) / 
                    (reserveIn * FEE_DENOMINATOR + amountInWithFee);
        
        require(amountOut >= _minAmountOut, "Insufficient output amount");
        require(amountOut < reserveOut, "Insufficient liquidity");
        
        // Update reserves
        if (isTokenA) {
            reserveA += _amountIn;
            reserveB -= amountOut;
        } else {
            reserveB += _amountIn;
            reserveA -= amountOut;
        }
        
        // Transfer output tokens
        IERC20(tokenOut).transfer(msg.sender, amountOut);
        
        emit Swap(msg.sender, _tokenIn, tokenOut, _amountIn, amountOut);
        
        return amountOut;
    }
    
    /**
     * @notice Get quote for swap
     */
    function getAmountOut(
        address _tokenIn,
        uint256 _amountIn
    ) external view returns (uint256 amountOut) {
        require(_amountIn > 0, "Invalid input amount");
        require(
            _tokenIn == tokenA || _tokenIn == tokenB,
            "Invalid input token"
        );
        
        bool isTokenA = _tokenIn == tokenA;
        uint256 reserveIn = isTokenA ? reserveA : reserveB;
        uint256 reserveOut = isTokenA ? reserveB : reserveA;
        
        uint256 amountInWithFee = _amountIn * (FEE_DENOMINATOR - FEE_PERCENTAGE);
        amountOut = (amountInWithFee * reserveOut) / 
                    (reserveIn * FEE_DENOMINATOR + amountInWithFee);
        
        return amountOut;
    }
    
    /**
     * @notice Get current pool price
     */
    function getPrice() external view returns (uint256 priceAtoB, uint256 priceBtoA) {
        require(reserveA > 0 && reserveB > 0, "No liquidity");
        
        priceAtoB = (reserveB * 1e18) / reserveA;
        priceBtoA = (reserveA * 1e18) / reserveB;
        
        return (priceAtoB, priceBtoA);
    }
    
    /**
     * @notice Get pool reserves
     */
    function getReserves() external view returns (uint256 _reserveA, uint256 _reserveB) {
        return (reserveA, reserveB);
    }
    
    /**
     * @notice Get user liquidity balance
     */
    function getLiquidityBalance(address _user) external view returns (uint256) {
        return liquidityBalance[_user];
    }
    
    /**
     * @notice Calculate square root (Babylonian method)
     */
    function sqrt(uint256 x) internal pure returns (uint256 y) {
        uint256 z = (x + 1) / 2;
        y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
    }
}
