# Judge Latency Performance Notes

## The Issue

- Local judge latency has roughly doubled since early August started
- Degradation is concentrated in the 13:00-15:00 window, consistent every day
- About 3% of evaluation runs in that window now end in timeout errors
- Longer-context evaluations hit timeouts more frequently than short checks

## Operational Effects

- Morning and evening eval windows remain unaffected and perform normally
- The 13:00-15:00 slot has become unreliable for time-sensitive client work
- All evaluation batch types see the latency increase during those hours, not just specific models

## Debugging and Options

- Something is degrading the local compute box specifically during 13:00-15:00
- Options on the table: reschedule critical evals to morning or evening windows, increase the timeout threshold for that window, or investigate the underlying resource contention directly
- Decision depends on client SLAs and what debugging reveals about the resource situation