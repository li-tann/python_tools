import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

# 用处, 以x0,y0为中点, 螺旋查找数据

x_arr = [0]
y_arr = [0]
index = 0
x0 = 0
y0 = 0
step = 1
while True:
    x=x0
    y=y0
    x -= step
    x -= 1
    y -= 1
    num = np.arange(-1,step*4-1,1)
    for  n in num:
        if n < step:
            x +=1
            y +=1
        elif n < 2 * step:
            x +=1
            y -=1
        elif n < 3 * step:
            x -=1
            y -=1
        else: # n < 4 * step
            x -=1
            y +=1
        
        # x_arr[index] = x
        # y_arr[index] = y
        # index+=1
        x_arr.append(x)
        y_arr.append(y)
    
    step += 1
    if step >= 10:
        break

# print(x_arr)
# print(y_arr)

x_major_locator=MultipleLocator(1)
#把x轴的刻度间隔设置为1，并存在变量里
y_major_locator=MultipleLocator(1)
#把y轴的刻度间隔设置为10，并存在变量里
ax=plt.gca()
#ax为两条坐标轴的实例
ax.xaxis.set_major_locator(x_major_locator)
#把x轴的主刻度设置为1的倍数
ax.yaxis.set_major_locator(y_major_locator)
#把y轴的主刻度设置为10的倍数

ax.set_aspect(1)
# 坐标轴等比例

plt.plot(x_arr,y_arr,linestyle='--',marker='.')
plt.grid()
plt.show()

'''
// c++ 版代码

int x0 = 0, y0 = 0;

vector<int> x_arr, y_arr;
x_arr.push_back(x0);
y_arr.push_back(y0);

int step = 1;
do{
    int x = x0 - step, y = y0;
    x -= 1;
    y -= 1;
    for(int num = -1; num < 4 * step - 1; num++)
    {
        if(num < step){
            x += 1; y += 1;
        }
        else if(num < 2 * step){
            x += 1; y -= 1;
        }
        else if(num < 3 * step){
            x -= 1; y -= 1;
        }
        else{ // num < 4 * step
            x -= 1; y += 1;
        }
        x_arr.push_back(x);
        y_arr.push_back(y);
    }
    ++step;
}while(step < 10)


'''

