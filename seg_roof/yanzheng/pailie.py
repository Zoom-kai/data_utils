import itertools
import torch

# mylist = list(itertools.combinations([248, 249, 250, 251, 252, 248, 249, 250, 251, 252, 248, 249, 250, 251, 252], 3))
# print(mylist)

a = torch.randint(245, 252, [10, 10])
b = torch.tensor([248, 249, 250, 251])

b = b.unsqueeze(1)
print(a, b)
print(a[0][1] in b)

