Selectable pill used for template pickers and the green-word/accent-word pickers in the Studio.

```jsx
<Chip active={tpl === 'cover'} onClick={() => setTpl('cover')}>Cover</Chip>
```

Renders filled in the active series' signature color when `active`; otherwise a dark outline pill.
