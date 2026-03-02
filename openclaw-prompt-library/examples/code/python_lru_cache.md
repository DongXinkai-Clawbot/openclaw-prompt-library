# 代码生成示例：LRU Cache

## 输入提示词

```
你是一位资深 Python 工程师。创建一个 LRU 缓存类。

要求：
- 语言：Python
- 使用 collections.OrderedDict 或自定义双向链表
- 操作：get / put
- 时间复杂度：O(1)
- 容量可配置
- 包含 hit/miss 统计
- 包含类型注解
- 包含 docstring
```

## 生成的代码

```python
from collections import OrderedDict
from typing import TypeVar, Optional

T = TypeVar('T')


class LRUCache:
    """
    LRU (Least Recently Used) Cache 实现
    
    Attributes:
        capacity: 缓存容量
        _cache: 内部 OrderedDict 存储
        hits: 缓存命中次数
        misses: 缓存未命中次数
    
    Example:
        >>> cache = LRUCache(2)
        >>> cache.put(1, 1)
        >>> cache.put(2, 2)
        >>> cache.get(1)
        1
    """
    
    def __init__(self, capacity: int) -> None:
        """
        初始化 LRU 缓存
        
        Args:
            capacity: 缓存容量，必须大于 0
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self._cache: OrderedDict = OrderedDict()
        self.hits: int = 0
        self.misses: int = 0
    
    def get(self, key: int) -> int:
        """
        获取缓存中的值
        
        Args:
            key: 缓存键
            
        Returns:
            缓存值，如果不存在返回 -1
        """
        if key in self._cache:
            self.hits += 1
            # 移动到末尾（最近使用）
            self._cache.move_to_end(key)
            return self._cache[key]
        self.misses += 1
        return -1
    
    def put(self, key: int, value: int) -> None:
        """
        设置缓存键值对
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        if key in self._cache:
            # 更新已有键值对
            self._cache.move_to_end(key)
        self._cache[key] = value
        
        # 超过容量，删除最旧的（最前面的）
        if len(self._cache) > self.capacity:
            self._cache.popitem(last=False)
    
    def get_stats(self) -> dict:
        """获取缓存统计信息"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.2%}",
            "size": len(self._cache),
            "capacity": self.capacity
        }
    
    def __repr__(self) -> str:
        return f"LRUCache({self.capacity}, size={len(self._cache)})"


# 单元测试
import unittest

class TestLRUCache(unittest.TestCase):
    def test_basic_operations(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        self.assertEqual(cache.get(1), 1)  # hit
        self.assertEqual(cache.get(2), 2)  # hit
        cache.put(3, 3)  # 触发删除 (1)
        self.assertEqual(cache.get(1), -1)  # miss
        self.assertEqual(cache.get(3), 3)  # hit
    
    def test_update_existing_key(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(1, 10)  # 更新已存在的键
        self.assertEqual(cache.get(1), 10)
        self.assertEqual(cache.get(2), 2)
    
    def test_capacity_constraint(self):
        cache = LRUCache(3)
        for i in range(5):
            cache.put(i, i * 10)
        self.assertEqual(len(cache._cache), 3)
        # 最旧的键应该被删除
        self.assertEqual(cache.get(0), -1)
        self.assertEqual(cache.get(1), -1)


if __name__ == "__main__":
    unittest.main()
```

## 关键改进点

1. **O(1) 时间复杂度** - 使用 OrderedDict 的 move_to_end
2. **类型注解完整** - 提高代码可读性和 IDE 支持
3. **错误处理** - 容量必须为正数
4. **统计功能** - 方便监控缓存性能
5. **完整测试** - 覆盖基本操作、更新、容量约束
