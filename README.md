Every client-key is mapped to a bucket.

A bucket has the following attributes:

- tokens: no. of tokens available at the moment
- size: total no. of tokens the bucket can hold
- rps: no. of tokens added per second
- last_used: last time the client made a request (epoch)

A store is needed for the buckets. It must be in-memory for fast-access: REDIS.

GET /limit
- Headers: x-client-key
- Responds with ALLOW or DENY with std rate-limit headers: limit, remaining, and reset

Limits are configurable on a per-client basis. Such configs are persisted in a database. A MongoDB collection with a unique index on the client field suffices for the purpose.

POST /limit/set
- Headers: x-client-key
- Body: rps, burst_size

