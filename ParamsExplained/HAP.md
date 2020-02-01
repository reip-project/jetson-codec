## codec usage
[What is HAP?](https://hap.video/)
HAP is a mainly for high performance, high resolution movie playback on media servers, live video performance, and event visuals. Not using for this project.


## FFMpeg documentation

### Options
format integer
Specifies the Hap format to encode.

hap
hap_alpha
hap_q

Default value is hap.

### chunks integer
Specifies the number of chunks to split frames into, between 1 and 64. This permits multithreaded decoding of large frames, potentially at the cost of data-rate. The encoder may modify this value to divide frames evenly.

Default value is 1.

### compressor integer
Specifies the second-stage compressor to use. If set to none, chunks will be limited to 1, as chunked uncompressed frames offer no benefit.

none
snappy

Default value is snappy.
