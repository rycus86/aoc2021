from shared.utils import *


class Day09(Solution):
    entries: list[int]
    gaps: list[int]

    def setup(self):
        self.entries = list()
        self.gaps = list()

        fs = self.input
        while len(fs) >= 2:
            self.entries.append(int(fs[0]))
            self.gaps.append(int(fs[1]))
            fs = fs[2:]

        if fs:
            self.entries.append(int(fs[0]))
            self.gaps.append(0)

    def part_1(self):
        fs = list()
        entries = list(enumerate(self.entries))
        gaps = list(self.gaps)

        while entries:
            e_idx, entry = entries.pop(0)
            fs.append((e_idx, entry))

            if not gaps or not entries:
                break

            while entries:
                gap = gaps.pop(0)
                l_idx, last_entry = entries[-1]

                if last_entry <= gap:
                    # the whole entry fits and (maybe) leaves some space
                    entries.pop(-1)
                    fs.append((l_idx, last_entry))
                    if last_entry < gap:
                        gaps.insert(0, gap - last_entry)
                    else:
                        break

                elif last_entry > gap:
                    # some fits, but some will need more space
                    fs.append((l_idx, gap))
                    entries[-1] = (l_idx, last_entry - gap)
                    break

        start, total = 0, 0
        for item_id, count in fs:
            total += sum((start + s) * item_id for s in range(count))
            start += count

        return total

    def part_2(self):
        from dataclasses import dataclass

        @dataclass
        class Item:
            id: int
            count: int
            gap: int

            def __repr__(self):
                return str(self.id) * self.count + '.' * self.gap

        items = list()
        for idx, (e, g) in enumerate(zip(self.entries, self.gaps)):
            items.append(Item(idx, e, g))

        for m_item in reversed(list(items)):
            if m_item.count <= 0:
                continue

            m_idx = items.index(m_item)

            for t_idx, t_item in enumerate(items[:m_idx]):
                if t_item.gap >= m_item.count:
                    items.pop(m_idx)

                    n_item = Item(m_item.id, m_item.count, t_item.gap - m_item.count)
                    if t_idx == m_idx - 1:
                        # if it's the previous item, we turn into gaps too
                        n_item.gap += m_item.count + m_item.gap
                    items[m_idx - 1].gap += m_item.count + m_item.gap
                    t_item.gap = 0
                    items.insert(t_idx + 1, n_item)

                    break

        start, total = 0, 0
        for item in items:
            total += sum((start + s) * item.id for s in range(item.count))
            start += item.count + item.gap

        return total


Day09(__file__).solve()
