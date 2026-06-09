# Order-Matching-Engine
A high-performance, O(1) Central Limit Order Book (CLOB) matching engine core implemented in Python with strict price-time priority.

# High-Performance CLOB Matching Engine Core

A lightweight, optimized Central Limit Order Book (CLOB) matching engine core implemented in Python. This project simulates a live financial exchange executing trades with strict **Price-Time Priority (FIFO)**.

> ⚠️ **Disclaimer & Educational Scope**
> This project is designed strictly as a conceptual prototype for educational study and algorithmic analysis. It is **not** a production-grade, ultra-low-latency High-Frequency Trading (HFT) engine. Production HFT systems require sub-microsecond execution speeds and bare-metal memory management, making compiled languages like C++, C, or Rust the industry standard. 
> 
> The purpose of this repository is to demonstrate how to architect complex financial data workflows, master multi-layered nested state manipulation, and optimize data traversal using algorithmic shortcuts in Python.

## 🛠️ Tech Stack & Key Concepts Used
* **Python 3.x**: Core programming language.
* **Nested Hash-Maps (Dictionaries)**: Used to achieve $O(1)$ direct-path memory lookups for order book depth.
* **Dynamic Key Snapping**: Utilized built-in `min()` and `max()` functions to target critical market execution points instantly without traversing data.
* **Control Flow Automation**: Implemented a dynamic `while` loop architecture bound to state-driven `if/elif/else` blocks to automate multi-stage order execution.
---

## 🏗️ Architecture & Data Structure Design

To mimic real-world financial systems, the engine organizes market depth using a nested data layout. Every bracket access peels back a structural layer like a nesting doll:

```text
Market Engine (Dict)
 ├── "BUY" Drawer (Dict)  ──> [Price Key] ──> List of Orders ──> [{"ID": 101, "qty": 10}]
 └── "SELL" Drawer (Dict) ──> [Price Key] ──> List of Orders ──> [{"ID": 203, "qty": 25}]

Instead of running slow search loops to find specific orders, the code uses a descending path ladder to instantly modify data deep within the system:
Trading_market[side][best_price][0]["qty"]

🧠 Core Algorithm Logic (process_new_order)
When a new order walks into the engine, it automatically executes the following pipeline:

Dynamic Mapping: The algorithm determines its own_side and opposite_side dynamically based on whether the incoming order is a BUY or SELL.

The Execution Loop: A while loop checks if the incoming order still has remaining quantity and ensures opposing orders exist in the market.

Target Price Snapping:

If matching a Buyer, it instantly snaps the lowest selling price using min().

If matching a Seller, it instantly snaps the highest buying price using max().

Guard Gate Check: It verifies if a trade is legally allowed. If prices cross cleanly, it accesses index 0 of the target price list (FIFO priority).

The Subtraction Matrix:

Partial Fill (Opposing Order is Larger): The target order's inventory decreases. The incoming order hits 0 quantity, terminating the loop.

Market Sweep (Incoming Order is Larger): The target order is wiped out and surgically popped from index 0. If that price level becomes empty, the folder key is deleted from the dictionary to optimize memory. The loop continues to the next available price point.

Remainder Booking: Any remaining quantity left over on the incoming order is safely saved down into its respective side of the order book.

🚧 Challenges Faced & Engineering Solutions
Building this engine required breaking through several complex programming paradigms. Below are the key roadblocks encountered during development and how they were solved:

1. The Multi-Bracket Syntax Confusion
The Problem: Navigating a list of dictionaries inside another nested dictionary made the bracket syntax (["SELL"][price][0]["qty"]) incredibly mind-boggling, resulting in broken lookups and errors.

The Solution: We broke down the data structure into separate lines of code, creating temporary variable references (e.g., current_match = market[side][price][0]). This isolated the layers, proving that dictionaries want names (keys) while lists want positions (indices).

2. The Directionless Math Trap (abs())
The Problem: When subtracting quantities to calculate remaining balances, numbers naturally went negative if the buyer wanted less than the seller offered. Attempting to fix this using the absolute value function abs() stripped away critical context—making it impossible for the engine to know which side of the market actually held the leftover quantity.

The Solution: We threw out abs() and replaced it with a pre-comparison conditional matrix (if sell > buy / elif buy > sell). This allowed the engine to precisely track who was satisfied, who had leftovers, and who needed to be deleted from the database.

3. Hardcoded Execution vs. Universal Side Logic
The Problem: The initial prototype worked perfectly for incoming buyers but completely broke when a seller entered the market because string keys like "SELL" and mathematical constraints like min() were hardcoded inside the core loop.

The Solution: We refactored the function to assign pointer states (opposite_side / own_side) right at startup. We then split the price lookup logic dynamically using an if/else gateway for min() and max(), scaling the script into a universal matching engine capable of handling any order type.
