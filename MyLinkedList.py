class Element:
    def __init__(self, data=None, nextE=None):
        self.data = data
        self.nextE = nextE


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self):
        res = "["

        start = self.head
        if start is None:
            res += "]"
            return res

        res += "{"
        res += str(start.data)
        nextVal = start.nextE

        while nextVal is not None:
            res += "},\n{"
            res += str(nextVal.data)
            nextVal = nextVal.nextE

        res += "}]"
        return res

    def get(self, e):
        if self.head is None:
            return None

        elif self.size == 1 and self.head.data != e.data:
            return None

        else:
            start = self.head
            while start.nextE is not None:
                if start.data == e.data:
                    return start
                start = start.nextE
            return None

    def delete(self, e):
        el = self.head
        prev = None

        if el.data == e.data and self.size == 1:
            self.head = None
            self.size = 0

        elif el.data == e.data and self.size > 1:
            self.head = el.nextE
            self.size -= 1

        else:
            prev = el
            el = el.nextE

            while el.data != e.data:
                prev = el
                el = el.nextE

            prev.nextE = el.nextE
            self.size -= 1

    def append(self, e, func=None):
        if self.head is None:
            self.head = e
            self.size = 1
            return

        el = self.head

        if func is None:
            if el.data >= e.data:
                e.nextE = el
                self.head = e
                self.size += 1
                return

            while el.nextE is not None:
                if el.nextE.data >= e.data:
                    break
                el = el.nextE

            e.nextE = el.nextE
            el.nextE = e
            self.size += 1

        else:
            if func(el.data, e.data):
                e.nextE = el
                self.head = e
                self.size += 1
                return

            while el.nextE is not None:
                if func(el.nextE.data, e.data):
                    break
                el = el.nextE

            e.nextE = el.nextE
            el.nextE = e
            self.size += 1
