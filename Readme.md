## Scaling with number of threads

Use `C1536` with a local volume of 16x16 .

nodes=192
tasks per node=288,12,72,144,(36 ?)

## Weak scaling

nodes=192,48,12

$N= 6* l_i^{2d_i}$

$N_X=(16*16*N/6)^{\frac{1}{2}}$