# Template Examples

This page demonstrates the various Markdown features available in this template.

## Code Blocks

Standard Python block:

```python
def hello_world():
    print("Hello, World!")
```

Console block (using `console` language):

```console
$ uv pip install requests
```

Displaying a file title:

```python title="example.py"
import os
print(os.getcwd())
```

## Admonitions (Note Blocks)

### Note
!!! note
    This is a standard **Note** block. It uses the custom Deep Purple border color we configured.

### Important
!!! important
    This is an **Important** block.

### Warning
!!! warning
    This is a **Warning** block.

### Tip
!!! tip
    This is a **Tip** block.

## Images

Standard image syntax (ensure assets are in `docs/assets/`):

![Logo](assets/logo-letter.svg)

## Links

- [Internal Link to Home](index.md)
- [External Link to Astral](https://astral.sh)

## Formatting

**Bold Text** and *Italic Text*.

`Inline code` style.

> Blockquotes are styled like this.
