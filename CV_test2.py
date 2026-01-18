'''
Áp dụng bộ lọc kernel vào ma trận 
'''

import numpy as np
import matplotlib.pyplot as plt

image = np.array([
    [0,0,0,0,0],
    [0,0,1,1,1],
    [0,0,1,1,1],
    [0,0,1,1,1],
    [0,0,0,0,0]
], dtype=np.float32)    # này là ma trận input 

kernel = np.array([
    [0, 1, 0],
    [0, 0, 0],
    [0,-1, 0]
], dtype=np.float32)    # bộ lọc kernel của mình 

def convolution2d(image, kernel):
    h, w = image.shape  # số pixel cao, rộng của input - 5 
    kh, kw = kernel.shape   # của bộ lọc - 3 

    # Xoay kernel
    # kernel_rot = np.flipud(np.fliplr(kernel))

    # khi mà dùng kernel thì output bị nhỏ hơn input trái phải trên dưới 
    pad_h = 1 # trái phải 
    pad_w = 1 # trên dưới 
    padded_image = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant') # mình sẽ extend cái input ra bằng những cột 0 
    output = np.zeros_like(image)

    # Convolution (tích chập)
    for i in range(h):
        for j in range(w):
            region = padded_image[i:i+kh, j:j+kw]   # chạy kernel từ pixel số 0 đến pixel số 3x3 rồi nhích 1 pixel 
            output[i, j] = np.sum(region * kernel)
    return output

output = convolution2d(image, kernel)   # gọi hàm vừa viết và lưu vào biến output 

fig, axs = plt.subplots(1, 3, figsize=(12, 4)) # fig gồm 1 hàng, 3 đồ thị axs 0, 1, 2

axs[0].imshow(image, cmap='gray')
axs[0].set_title("Input Image")
axs[0].axis('off')

axs[1].imshow(kernel, cmap='gray')
axs[1].set_title("Kernel")
axs[1].axis('off')

axs[2].imshow(output, cmap='gray')
axs[2].set_title("Output")
axs[2].axis('off')

plt.tight_layout()
plt.show()
