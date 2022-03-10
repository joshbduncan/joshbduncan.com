import re
import xml.etree.ElementTree as etree

from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension


class MarkdownAlerts(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(
            MarkdownAlertsProcessor(md.parser), "box", 175
        )


class MarkdownAlertsProcessor(BlockProcessor):
    RE_FENCE_START = r"^!{4}(.*)\n"
    RE_FENCE_END = r"\n!{4}\s*$"

    def test(self, parent, block):
        """Test to make sure fenced text is found in block

        Fenced block must be as follows:

        !!!!type(optional)
        Markdown content to be rendered inside...
        !!!!

        """
        return re.match(self.RE_FENCE_START, block)

    def run(self, parent, blocks):
        """Run the regex on the block and construct the callout div"""
        original_block = blocks[0]

        # get callout type if provided
        classes = ["callout"]
        match = re.match(self.RE_FENCE_START, blocks[0])
        if match.groups()[0]:
            # grab the matched type and strip any spaces
            type = match.groups()[0].replace(" ", "-")
            classes.append(f"callout-{type}")

        # replace the fence start
        blocks[0] = re.sub(self.RE_FENCE_START, "", blocks[0])

        # find block with ending fence
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_FENCE_END, block):
                # remove fence
                blocks[block_num] = re.sub(self.RE_FENCE_END, "", block)
                # render fenced text inside a new div
                e = etree.SubElement(parent, "div")
                e.set("class", " ".join(classes))
                e.set("role", "comment")
                # parse block text that goes into new div
                self.parser.parseBlocks(e, blocks[0 : block_num + 1])
                # remove used blocks
                for _ in range(0, block_num + 1):
                    blocks.pop(0)
                return True

        # no closing fence found so reset everything
        blocks[0] = original_block
        return False
