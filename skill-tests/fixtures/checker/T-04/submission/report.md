Task: T-04
Type: missing resource
Tried: looked for inputs/rates.csv in the task folder, the project root and the shared inputs folder. It is not present anywhere. The task record gives no rates, and no other file lists them.
Smallest unblocking step: finance supplies inputs/rates.csv (columns: region, rate).
Proposed narrower task: implement compute_tax against a rates table passed in as an argument, with the file loader left as a stub. That can pass on its own and is ready for the real file.
