import random
import time
import numpy as np

start_time = time.time()
weight_price = np.array([[13,23,27,33,41,45,58,60],[15,30,40,60,70,80,85,90]])
MAX_IN = 100

max_price = 0
max_i = 0

#要素の追加
#13個追加
new_weight_price = np.array([[5,10,15,20,25,30,35,40,50,55,65,70,75],[5,10,15,20,25,30,35,40,50,55,65,70,75]])
weight_price = np.concatenate([weight_price,new_weight_price],1)

length = len(weight_price[0])
print("N: ",length)

#総当たり
#それぞれの宝石の配列に0か1を与える
for i in range(2**length):
    now_weight = 0
    total_price = 0
    bin_str = format(i,'021b')
    array_bin= np.array([bin_str.split(),bin_str.split()])
    print(array_bin)

    #配列に各宝石を割り当て,1ならtrue,0ならfalseとして扱う
    l_houseki = weight_price * array_bin

    if now_weight <= MAX_IN:
        if total_price > max_price:
            max_price = total_price
            #この時のiの値を記録しておく
            max_i = i

#持っている宝石を配列で書き出す
max_array_bin = format(max_i,'021b')
for n in range(length):
    if max_array_bin[n] == "1":
        l_houseki.append(weight[n])

print("max_price: ",max_price)
print("jewelry's best weight: ",l_houseki)

end_time = time.time()
print("time: ",end_time - start_time)
