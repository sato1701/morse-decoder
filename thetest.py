import matplotlib.pyplot as plt

testdata = [range(10,20) for i in range(0, 10) ]
plt.pcolormesh(range(10), range(10), testdata)
plt.show()

# 音声の取り込み
#  同時に、開始日時も取得
# フーリエ解析
# ピーク周波数の検出
#  ピーク周波数の歪みがあるため、固定はできない
# 量子化（0/1）→トン・ツー・空白に分解
# 文章化
