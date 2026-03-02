# Crypto 示例：DeFi 跨平台Swap

## 输入提示词

```
创建 DeFi 跨平台swap脚本：

协议：Uniswap V3 → Curve
操作：ETH → USDC → DAI → ETH (三角套利)

参数：
- 输入金额：1 ETH
- 滑点容忍：0.5%
- 截止时间：300秒

要求：
- 交易签名
- Gas 估算
- 每步结果验证
- 完整错误处理
```

## 生成的脚本框架

```python
"""
DeFi 三角套利脚本
⚠️ 风险提示：套利存在智能合约风险、滑点风险、MEV风险
"""

import asyncio
from typing import Dict, List
from dataclasses import dataclass
from decimal import Decimal

# 假设使用 web3.py
from web3 import Web3
from eth_account import Account
from uniswap import Uniswap
from curve import Curve


@dataclass
class SwapStep:
    """单步Swap信息"""
    protocol: str      # Uniswap/Curve
    token_in: str     # 输入代币
    token_out: str    # 输出代币
    amount_in: float  # 输入数量
    expected_out: float  # 预期输出
    actual_out: float   # 实际输出
    gas_used: int       # 消耗Gas
    tx_hash: str        # 交易哈希


class TriangularArbitrage:
    """三角套利机器人"""
    
    def __init__(self, private_key: str, rpc_url: str):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = Account.from_key(private_key)
        
        # 初始化协议
        self.uniswap = Uniswap(
            address=self.account.address,
            private_key=private_key,
            version=3
        )
        self.curve = Curve(self.account.address)
        
        # 配置
        self.slippage_tolerance = 0.005  # 0.5%
        self.deadline = 300  # 300秒
        
        # 代币地址 (示例)
        self.TOKENS = {
            "ETH": "0x0000000000000000000000000000000000000000",
            "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "DAI": "0x6B175474E89094C44Da98b954EesadCDEF9bd056",
        }
    
    async def get_prices(self) -> Dict:
        """获取各交易对价格"""
        # 简化示例 - 实际需要调用各协议合约
        prices = {
            "ETH-USDC": {"uniswap": 3500.0, "curve": 3498.0},
            "USDC-DAI": {"uniswap": 1.001, "curve": 1.0005},
            "DAI-ETH": {"uniswap": 0.000285, "curve": 0.000286},
        }
        return prices
    
    async def calculate_arbitrage(self, amount_in: float) -> Dict:
        """计算套利路径和利润"""
        prices = await self.get_prices()
        
        # 路径: ETH → USDC → DAI → ETH
        # 第1步: ETH → USDC (Uniswap)
        eth_to_usdc = amount_in * prices["ETH-USDC"]["uniswap"]
        
        # 第2步: USDC → DAI (Curve)
        usdc_to_dai = eth_to_usdc * prices["USDC-DAI"]["curve"]
        
        # 第3步: DAI → ETH (Curve)
        dai_to_eth = usdc_to_dai * prices["DAI-ETH"]["curve"]
        
        profit = dai_to_eth - amount_in
        profit_percentage = (profit / amount_in) * 100
        
        return {
            "input": amount_in,
            "output": dai_to_eth,
            "profit": profit,
            "profit_percentage": profit_percentage,
            "viable": profit > 0  # 减去Gas后是否有利可图
        }
    
    async def execute_arbitrage(self, amount_in: float) -> List[SwapStep]:
        """执行套利交易"""
        steps = []
        
        try:
            # Step 1: ETH → USDC (Uniswap V3)
            usdc_amount = await self._swap_uniswap(
                token_in=self.TOKENS["ETH"],
                token_out=self.TOKENS["USDC"],
                amount_in=amount_in
            )
            steps.append(SwapStep(
                protocol="Uniswap V3",
                token_in="ETH",
                token_out="USDC",
                amount_in=amount_in,
                expected_out=amount_in * 3500,
                actual_out=usdc_amount,
                gas_used=0,  # 需从交易回执获取
                tx_hash=""
            ))
            
            # Step 2: USDC → DAI (Curve)
            dai_amount = await self._swap_curve(
                token_in=self.TOKENS["USDC"],
                token_out=self.TOKENS["DAI"],
                amount_in=usdc_amount
            )
            steps.append(SwapStep(
                protocol="Curve",
                token_in="USDC",
                token_out="DAI",
                amount_in=usdc_amount,
                expected_out=usdc_amount * 1.001,
                actual_out=dai_amount,
                gas_used=0,
                tx_hash=""
            ))
            
            # Step 3: DAI → ETH (Curve)
            final_eth = await self._swap_curve(
                token_in=self.TOKENS["DAI"],
                token_out=self.TOKENS["ETH"],
                amount_in=dai_amount
            )
            steps.append(SwapStep(
                protocol="Curve",
                token_in="DAI",
                token_out="ETH",
                amount_in=dai_amount,
                expected_out=dai_amount * 0.000286,
                actual_out=final_eth,
                gas_used=0,
                tx_hash=""
            ))
            
        except Exception as e:
            print(f"❌ 套利失败: {e}")
            # 可以在此添加回滚逻辑
            
        return steps
    
    async def _swap_uniswap(self, token_in: str, token_out: str, amount_in: float) -> float:
        """Uniswap Swap"""
        # 实际实现需要:
        # 1. 获取quote
        # 2. 构建交易
        # 3. 签名发送
        # 4. 等待确认
        pass
    
    async def _swap_curve(self, token_in: str, token_out: str, amount_in: float) -> float:
        """Curve Swap"""
        pass


# 使用示例
async def main():
    # 初始化 (请使用环境变量!)
    private_key = "0x..."  # ⚠️ 危险：实际使用请用环境变量
    arbitrage = TriangularArbitrage(
        private_key=private_key,
        rpc_url="https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"
    )
    
    # 检查套利机会
    amount = 1.0  # 1 ETH
    result = await arbitrage.calculate_arbitrage(amount)
    
    print(f"📊 套利分析:")
    print(f"   输入: {result['input']} ETH")
    print(f"   输出: {result['output']:.4f} ETH")
    print(f"   利润: {result['profit']:.4f} ETH ({result['profit_percentage']:.2f}%)")
    
    if result['viable']:
        print("✅ 套利机会存在，执行交易...")
        # 实际执行前需要考虑Gas成本
        steps = await arbitrage.execute_arbitrage(amount)
        for step in steps:
            print(f"   ✓ {step.protocol}: {step.token_in} → {step.token_out}")


if __name__ == "__main__":
    asyncio.run(main())
```

## ⚠️ 重要安全提示

1. **智能合约风险** - 可能存在漏洞
2. **滑点风险** - 价格变动可能导致损失
3. **MEV风险** - 套利者可能被夹
4. **Gas成本** - 高Gas可能吃掉利润
5. **测试网先行** - 先在测试网验证
