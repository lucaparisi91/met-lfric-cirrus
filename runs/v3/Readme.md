# Submitting lfric_atm jobs

This folder contains some scripts to run lfric_atm jobs on Cirrus. They are intended to be examples and a template to use when first submitting a job on Cirrus.

## Memory tracing

You can use heaptrack to generate memory profiles. On C896 this leads to 
- OOM if using heaptrack on all processess
- hanging at    context initialisation if only one of the cores in the model uses heaptrack. A an invalid allocation expection is thrown in this case, at least in the case when the servers are not run with heaptrack.

