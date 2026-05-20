"""
驅動開發與通訊協議
1. 在樹莓派配置 I2C 環境
2. 設定感測器寄存器 (LED 電流、採樣率、脈衝寬度) — 由 max30102.py setup() 完成
3. 穩定讀取紅光 (Red) 與紅外光 (IR) 的原始數值
還需要資料品質檢查、濾波、計算心率/血氧
"""
import time
from max30102 import MAX30102

# 感測器規格 (由 max30102.py setup() 寫死)
SAMPLE_RATE_HZ = 100          # 採樣率 (DSP 的 fs 可以用這個)
SAMPLES_PER_BATCH = 100       # 一次取得 100 筆 ≈ 1 秒
FINGER_THRESHOLD = 10000      # 紅光 > 此值 → 判定為手指接觸中


try:
    m = MAX30102(channel=1, address=0x57)
    print("MAX30102 初始化成功")
    print("請將手指輕輕放在感測器上...")

    while True:
        # 批次讀 100 筆，回傳兩個 list
        red_buf, ir_buf = m.read_sequential(amount=SAMPLES_PER_BATCH)

        # 逐筆過濾顯示：每筆獨立判斷手指有沒有接觸
        # 手指接觸時紅光 > 10000，未接觸時 < 10000，FINGER_THRESHOLD=10000 為安全門檻
        printed_any = False
        for red, ir in zip(red_buf, ir_buf):
            if red < FINGER_THRESHOLD:
                continue
            print("紅光: {} | 紅外線: {}".format(red, ir))
            printed_any = True

        # 整批 100 筆都沒手指 → 顯示等待訊息
        if not printed_any:
            print("等待手指...", end="\r")

except KeyboardInterrupt:
    print("\n使用者中斷")
except Exception as e:
    print("錯誤: {}".format(e))
