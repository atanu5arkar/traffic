Every client-key is mapped to a bucket.

A bucket has the following attributes:

- tokens: no. of tokens available at the moment
- size: total no. of tokens the bucket can hold
- rps: no. of tokens added per second
- last_used: last time the client made a request (epoch value)

A store is needed for the buckets. It must be in-memory for fast-access.

