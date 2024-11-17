from . import misc, base
from .. import helpers
from .. import objects


class LayoutParser(base.BaseParser):
    def __init__(self, layouts):
        super().__init__(layouts)

        self._ask_indices = []
        self._max_ask_layout_index = None
        self.layouts = []

    def parse(self):
        """Begins the parsing chain and returns the final list of parsed objects"""
        while self.next():
            if self.current["type"] == "ask":
                # We assume that if we got a layout type of "ask", it'd be the first element in the list.
                indices = [i for i in self.current["blocks"]]

                if attribution := self.current.get("attribution"):
                    attribution = misc.parse_attribution(attribution)

                self.layouts.append(
                    objects.layouts.AskLayout(indices, attribution=attribution),
                )

                self._ask_indices.extend(indices)
            elif self.current["type"] == "rows":
                rows = []
                truncate_after = self.get_or("truncateAfter", "truncate_after")

                for row in self.current["display"]:
                    indices = [index for index in row["blocks"] if index not in self._ask_indices]
                    if indices:
                        # Which display mode should we use?
                        if mode := row.get("mode"):
                            if mode["type"] == "carousel":
                                mode = objects.layouts.DisplayMode.CAROUSEL
                            else:
                                mode = objects.layouts.DisplayMode.UNSUPPORTED
                        else:
                            mode = objects.layouts.DisplayMode.WEIGHTED

                        rows.append(
                            objects.layouts.RowLayout(
                                ranges=indices,
                                display_mode=mode,
                            )
                        )

                self.layouts.append(objects.layouts.Rows(rows=rows, truncate_after=truncate_after))

        return self.layouts
