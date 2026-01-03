function Div(div)
  -- Process the main bibliography container
  if div.classes:includes('csl-bib-body') then
    
    -- First, walk the block to fix links and italics inside entries
    div = pandoc.walk_block(div, {
      Link = function(el)
        local url = el.target
        local content = pandoc.utils.stringify(el.content)
        return pandoc.RawInline('html', '<a href="' .. url .. '">' .. content .. '</a>')
      end,
      Emph = function(el)
        local content = pandoc.utils.stringify(el.content)
        return pandoc.RawInline('html', '<em>' .. content .. '</em>')
      end,
      Strong = function(el)
        local content = pandoc.utils.stringify(el.content)
        return pandoc.RawInline('html', '<strong>' .. content .. '</strong>')
      end
    })

    -- Now, iterate over the blocks (entries) and append a line break
    local new_blocks = {}
    for i, block in ipairs(div.content) do
      table.insert(new_blocks, block)
      -- If this block is a citation entry, add a raw HTML break after it
      if block.t == 'Div' and block.classes:includes('csl-entry') then
         table.insert(new_blocks, pandoc.RawBlock('html', '<br />'))
      end
    end
    div.content = new_blocks
    
    return div
  end
  return nil
end
