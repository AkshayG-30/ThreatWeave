# NF-UNSW-NB15-v2 Dataset Profile

- **File**: NF-UNSW-NB15-v2.csv
- **Size**: 421.40 MB
- **Rows**: 2390275
- **Columns**: 45

## Columns and Types
- `IPV4_SRC_ADDR` (object): 0 missing values
- `L4_SRC_PORT` (int64): 0 missing values
- `IPV4_DST_ADDR` (object): 0 missing values
- `L4_DST_PORT` (int64): 0 missing values
- `PROTOCOL` (int64): 0 missing values
- `L7_PROTO` (float64): 0 missing values
- `IN_BYTES` (int64): 0 missing values
- `IN_PKTS` (int64): 0 missing values
- `OUT_BYTES` (int64): 0 missing values
- `OUT_PKTS` (int64): 0 missing values
- `TCP_FLAGS` (int64): 0 missing values
- `CLIENT_TCP_FLAGS` (int64): 0 missing values
- `SERVER_TCP_FLAGS` (int64): 0 missing values
- `FLOW_DURATION_MILLISECONDS` (int64): 0 missing values
- `DURATION_IN` (int64): 0 missing values
- `DURATION_OUT` (int64): 0 missing values
- `MIN_TTL` (int64): 0 missing values
- `MAX_TTL` (int64): 0 missing values
- `LONGEST_FLOW_PKT` (int64): 0 missing values
- `SHORTEST_FLOW_PKT` (int64): 0 missing values
- `MIN_IP_PKT_LEN` (int64): 0 missing values
- `MAX_IP_PKT_LEN` (int64): 0 missing values
- `SRC_TO_DST_SECOND_BYTES` (float64): 0 missing values
- `DST_TO_SRC_SECOND_BYTES` (float64): 0 missing values
- `RETRANSMITTED_IN_BYTES` (int64): 0 missing values
- `RETRANSMITTED_IN_PKTS` (int64): 0 missing values
- `RETRANSMITTED_OUT_BYTES` (int64): 0 missing values
- `RETRANSMITTED_OUT_PKTS` (int64): 0 missing values
- `SRC_TO_DST_AVG_THROUGHPUT` (int64): 0 missing values
- `DST_TO_SRC_AVG_THROUGHPUT` (int64): 0 missing values
- `NUM_PKTS_UP_TO_128_BYTES` (int64): 0 missing values
- `NUM_PKTS_128_TO_256_BYTES` (int64): 0 missing values
- `NUM_PKTS_256_TO_512_BYTES` (int64): 0 missing values
- `NUM_PKTS_512_TO_1024_BYTES` (int64): 0 missing values
- `NUM_PKTS_1024_TO_1514_BYTES` (int64): 0 missing values
- `TCP_WIN_MAX_IN` (int64): 0 missing values
- `TCP_WIN_MAX_OUT` (int64): 0 missing values
- `ICMP_TYPE` (int64): 0 missing values
- `ICMP_IPV4_TYPE` (int64): 0 missing values
- `DNS_QUERY_ID` (int64): 0 missing values
- `DNS_QUERY_TYPE` (int64): 0 missing values
- `DNS_TTL_ANSWER` (int64): 0 missing values
- `FTP_COMMAND_RET_CODE` (float64): 0 missing values
- `Label` (int64): 0 missing values
- `Attack` (object): 0 missing values

## Label Distribution
- 0: 2295222
- 1: 95053

## Attack Categories
- Benign: 2295222
- Fuzzers: 22310
- Exploits: 31551
- Reconnaissance: 12779
- Generic: 16560
- DoS: 5794
- Shellcode: 1427
- Backdoor: 2169
- Worms: 164
- Analysis: 2299
