Labeled slider + live readout for photo zoom/position/darken, title size, animation speed.

```jsx
<RangeRow label="Zoom" value={zoom} min={100} max={260} onChange={setZoom} display={(zoom/100).toFixed(1)} />
```
