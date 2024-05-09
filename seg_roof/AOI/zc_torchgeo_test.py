from torch.utils.data import DataLoader
from torchgeo.datasets import SpaceNet2
from torchgeo.samplers import RandomGeoSampler
from torchgeo.datasets import spacenet
# Take the union of all Landsat 7 and 8 imagery
spaceset2 = SpaceNet2(root="/mnt/data1/dzy_data/remote_sensing_data")

# Take the intersection of Landsat and CDL data

sampler = RandomGeoSampler(spaceset2, size=1000, length=512)
# Use the dataset and sampler as normal in a PyTorch DataLoader
dataloader = DataLoader(spaceset2, sampler=sampler, batch_size=32)
# for batch in dataloader:
#     print(batch)
