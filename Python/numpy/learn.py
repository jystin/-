from torch.utils.tensorboard import SummaryWriter
import numpy as np
 
np.random.seed(20221104)
writer = SummaryWriter('test_1104', max_queue=100)
# add_image
img = np.random.rand(3, 100, 100)
for i in range(100):
    writer.add_image('Image', img, i)
    if i % 10 == 0:  # 每 10 步刷新一次
        writer.flush()