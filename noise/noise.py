import time
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

start_time = time.time()
noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)
noise4 = PerlinNoise(octaves=24)

xpix, ypix = 200, 200
pic = []
for i in range(ypix):
    row = []
    for j in range(xpix):
        noise_val = noise1([i / xpix, j / ypix])
        noise_val += 0.5 * noise2([i / xpix, j / ypix])
        noise_val += 0.25 * noise3([i / xpix, j / ypix])
        noise_val += 0.125 * noise4([i / xpix, j / ypix])
        row.append(noise_val)
    pic.append(row)

[print(i) for i in pic]
plt.imshow(pic, cmap='gray')
plt.show()
print(time.time()-start_time)