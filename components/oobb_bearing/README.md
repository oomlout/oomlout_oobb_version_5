# oobb_bearing

Lookup-bearing wrapper for the CSV data under `data/bearing`.

Use `bearing_size` to select a row from the bearing tables, then the component emits a matching `opsc` bearing object with `id`, `od`, and `depth` filled from that row.

`clearance` defaults to `0` and is forwarded to the legacy bearing object as `clearance_bearing`.

