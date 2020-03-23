import random
import time

start_time = time.time()
weight = [13,23,27,33,41,45,58,60]
price  = [15,30,40,60,70,80,85,90]
MAX_IN = 100
l_houseki = []

max_price = 0
max_i = 0

#要素の追加
#13個追加
new_weight = [5,10,15,20,25,30,35,40,50,55,65,70,75]
new_price  = [5,10,15,20,25,30,35,40,50,55,65,70,75]
weight += new_weight
price  += new_price
length = len(weight)
print("N: ",length)

#総当たり
#それぞれの宝石の配列に0か1を与える
for i in range(2**length):
    now_weight = 0
    total_price = 0
    bin_str = format(i,'021b')
    #配列に各宝石を割り当て,1ならtrue,0ならfalseとして扱う
    for n in range(length):
        if bin_str[n] == "1":
            now_weight += weight[n]
            total_price += price[n]
        if now_weight >= MAX_IN:
            break
        else:
            if total_price > max_price:
                max_price = total_price
                #この時のiの値を記録しておく
                max_i = i

#持っている宝石を配列で書き出す
max_bin_str = format(max_i,'021b')
for n in range(length):
    if max_bin_str[n] == "1":
        l_houseki.append(weight[n])

print("max_price: ",max_price)
print("jewelry's best weight: ",l_houseki)

end_time = time.time()
print("time: ",end_time - start_time)
