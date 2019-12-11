from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = EmbeddingComposite(DWaveSampler())

a = dict()
for i in range(1,8):
  for j in range(i+1,8):
    a.update({(i,j):i*j})

#response = sampler.sample_ising({}, a, num_reads=100)
#response = sampler.sample_ising({}, a, num_reads=100, chain_strength=100)
response = sampler.sample_ising({}, a, num_reads=100, chain_strength=100, postprocess='optimization')



print(response)

