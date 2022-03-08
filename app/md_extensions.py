import markdown
import re
import xml.etree.ElementTree as etree

from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension


class MdAlerts(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(MdAlertsProcessor(md.parser), "box", 175)


def makeExtension(configs=[]):
    return MdAlerts()


class MdAlertsProcessor(BlockProcessor):
    RE_FENCE_START = r"^ *!{3,}(.*)\n"
    RE_FENCE_END = r"\n *!{3,}\s*$"

    def test(self, parent, block):
        return re.match(self.RE_FENCE_START, block)

    def run(self, parent, blocks):
        original_block = blocks[0]

        # get alert type if provided (defaults to info)
        match = re.match(self.RE_FENCE_START, blocks[0])
        type = match.groups()[0] if match.groups()[0] else "info"
        classes = f"alert alert-{type}"

        # replace the fence start
        blocks[0] = re.sub(self.RE_FENCE_START, "", blocks[0])

        # find block with ending fence
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_FENCE_END, block):
                # remove fence
                blocks[block_num] = re.sub(self.RE_FENCE_END, "", block)
                e = etree.dump(parent)
                # render fenced area inside a new div
                e = etree.SubElement(parent, "div")
                e.set("class", classes)
                e.set("role", "alert")
                # render raw_html for alert rext
                raw_html = (
                    markdown.markdown("\n".join(blocks[0 : block_num + 1]))
                    .removeprefix("<p>")
                    .removesuffix("</p>")
                )
                # set div text to rendered html
                e.text = raw_html
                # remove used blocks
                for _ in range(0, block_num + 1):
                    blocks.pop(0)
                return True

        # No closing marker!  Restore and do nothing
        blocks[0] = original_block
        return False
