import json
from datetime import datetime

# 手续费比例
fee_rate = 0.04
LAMPORTS_PER_SOL = 1e9  # 1 SOL = 1e9 lamports

# 你的玩家ID
player_id = "A9NBEQeCYzvqidFnh7UVZsBrW2T5df4cqnBjxCBQRJ88"

# 读取 JSON 文件
with open("data1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

total_profit = 0
total_fee = 0
rounds = 0
win_count = 0
lose_count = 0

# 今天的日期字符串（UTC）
today_str = datetime.utcnow().strftime("%Y-%m-%d")

# 遍历 payload 数组
for idx, round_data in enumerate(data.get("payload", [])):
    created_at = round_data.get("createdAt", "")
    if not created_at.startswith(today_str):  # 只统计今天的数据
        continue

    if "players" not in round_data or player_id not in round_data["players"]:
        continue

    player_data = round_data["players"][player_id]

    # 转换金额（SOL）
    bet_amount = float(player_data.get("lamports", 0)) / LAMPORTS_PER_SOL
    reward = float(player_data.get("reward", 0)) / LAMPORTS_PER_SOL

    # 手续费
    fee = bet_amount * fee_rate
    total_fee += fee

    if reward == 0:  # 输
        total_profit -= (bet_amount + fee)
        lose_count += 1
    else:  # 赢
        profit_only = reward - bet_amount
        total_profit += profit_only - fee
        win_count += 1

    rounds += 1

# 把数据存储到 JSON 中
result = {
    "total_profit": total_profit,
    "total_fee": total_fee,
    "rounds": rounds,
    "win_count": win_count,
    "lose_count": lose_count,
    "win_rate": (win_count / rounds * 100) if rounds > 0 else 0,
    "today": today_str
}

# 输出 JSON 文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print(f"数据已保存到 data.json: {result}")
