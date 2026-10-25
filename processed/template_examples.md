# Template Examples

This page demonstrates the various Markdown features available in this template.

## Code Blocks

Standard Python block:

```python
def hello_world():
    print("Hello, World!")
```

Console block (using `console` language):

```
$ uv pip install requests
```

Displaying a file title:

`python title="example.py" import os print(os.getcwd())`

## Admonitions (Note Blocks)

Admonition blocks highlight contextual guidance, warnings, and implementation notes across documentation pages.

### Note

- !!! note
  This is a standard **Note** block. It uses the custom Deep Purple border color we configured.

### Important

- !!! important
  This is an **Important** block.

### Warning

- !!! warning
  This is a **Warning** block.

### Tip

- !!! tip
  This is a **Tip** block.

## Images

Standard image syntax (ensure assets are in `docs/assets/`):

<figure>
<img src="assets/logo_dark.jpeg" alt="Logo" />
<figcaption aria-hidden="true">Logo</figcaption>
</figure>

## Links

- [Internal Link to Home](index.md)

## Formatting

**Bold Text** and *Italic Text*.

`Inline code` style.

> Blockquotes are styled like this.
