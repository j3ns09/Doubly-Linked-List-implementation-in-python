class Node:
    def __init__(self,data):
        self.previous = None
        self.data = data
        self.next = None

    def switch(self,other) -> None:
        self.data, other.data = other.data, self.data

    def disconnect(self) -> None:
        if self.previous and self.next:
            self.previous.next, self.next.previous = self.next, self.previous
        elif self.previous and not self.next:
            self.previous.next = None
        elif not self.previous and self.next:
            self.next.previous = None

    def connect(self, other: object) -> None:
        if isinstance(other, Node):
            self.next = other
            other.previous = self

    def __repr__(self) -> str:
        return f"Node: data={self.data}, next={bool(self.next)}"

    def __str__(self) -> str:
        return str(self.data)

class LinkedList:
    def __init__(self, *args):
        self.head : Node | None = None
        self.tail : Node | None = None
        self.len : int = 0

        for arg in args:
            self.append(arg)

    def __del_first(self) -> None:
        if self.len == 0:
            return
        if self.len < 2:
            self.clear()
        else:
            self.head : Node = self.head.next
            self.head.previous = None
            self.len -= 1

    def __del_last(self) -> None:
        if self.len == 0:
            return
        if self.len < 2:
            self.clear()
        else:
            self.tail : Node = self.tail.previous
            self.tail.next = None
            self.len -= 1

    def __setitem__(self, index : int, data) -> None:
        if index > self.len:
            raise IndexError("Index out of range")
        self[index].data = data

    def __delitem__(self, key : int) -> None:
        if key == 0:
            self.__del_first()
            return
        if key == -1:
            self.__del_last()
            return

        self[key].disconnect()
        self.len -= 1

    def __mul__(self, other : object) -> object:
        if isinstance(other, int):
            new_list : LinkedList = LinkedList()
            current : Node | None = self.head
            for _ in range(self.len * other):
                if current is None:
                    current = self.head
                new_list.append(current.data)
                current = current.next
            return new_list
        raise TypeError("Incorrect type")

    def __imul__(self, other : object) -> object:
        return self.__mul__(other)

    def __rmul__(self, other : object) -> object:
        return self.__mul__(other)

    def __add__(self, other : object) -> object:
        if not isinstance(other, LinkedList):
            raise TypeError("can't add type "+str(type(other))+" and type "+str(type(self))+" using + operator")

        self.tail.next = other.head

        new_list : LinkedList = self.deepcopy()

        new_list.len = self.len + other.len

        self.tail.next = None

        return new_list

    def __eq__(self, value: object) -> bool:
        if isinstance(value, (list, tuple)):
            k : int = 0
            for node in self:
                if node.data != value[k]:
                    return False
                k += 1
            return True
        if isinstance(value, LinkedList):
            if self.len != value.len:
                return False

            current_l1 : Node = self.head
            current_l2 : Node = value.head

            while current_l1 or current_l2:
                if current_l1.data != current_l2.data:
                    return False
                current_l1 = current_l1.next
                current_l2 = current_l2.next
            return True
        raise TypeError("can't compare type LinkedList and", str(type(value)))

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)

    def __len__(self) -> int:
        return self.len

    def __iter__(self) -> object:
        current : Node | None = self.head
        while current:
            yield current
            current = current.next

    def __getitem__(self, index : int) -> Node:
        if self.len < 1 or index > self.len - 1:
            raise IndexError("list index out of range")

        if index == 0:
            return self.head
        if index == -1:
            return self.tail

        if index < -1:
            index = self.len + index

        if self.len - index < self.len//2:
            current : Node = self.tail
            for _ in range(self.len - 1 - index):
                current = current.previous
            return current

        current = self.head.next
        for _ in range(1, index):
            current = current.next
        return current

    def __hash__(self) -> str:
        return hash((item for item in self))

    def __contains__(self, value) -> bool:
        if not self.head:
            return False
        current : Node = self.head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False

    def __reversed__(self) -> object:
        current = self.tail
        new_list = LinkedList()
        while current:
            new_list.append(current.data)
            current = current.previous

        return new_list

    def __str__(self) -> str:
        final_string : str = "["
        if not self.head:
            final_string += "]*"
        else:
            current : Node = self.head
            while current:
                if not current.next:
                    final_string = final_string + str(current.data)+"]*"
                    break
                final_string = final_string + str(current.data)+","
                current = current.next
        return final_string

    def __repr__(self) -> str:
        return self.__str__()

    def append(self, data) -> None:
        node : Node = Node(data)

        if self.head:
            self.tail.next = node
            node.previous = self.tail
        else:
            self.head = node

        self.tail = node
        self.len += 1

    def remove(self, data) -> None:
        if not self.head:
            raise ValueError("LinkedList.remove(data): List is empty")

        current : Node = self.head

        while current:
            if current.data == data:
                current.disconnect()
                self.len -= 1
                return
            current = current.next

        raise ValueError("""LinkedList.remove(data): 
                         Can't remove node as the data is not held by any node""")

    def insert(self,index : int,data) -> None:
        if index > self.len:
            raise IndexError("LinkedList.insert(index, data): list index out of range")

        node : Node = Node(data)
        if index == 0:
            node.next, self.head.previous = self.head, node
            self.head = node
            self.len += 1
            return
        if index == self.len:
            self.tail.next = node
            self.tail = node
            self.len += 1
            return

        k : int = 1
        current = self.head.next
        previous = current.previous
        while k != index:
            previous = current
            current = current.next
            k += 1
        node.next = current
        current.previous = node
        previous.next, node.previous = node, previous
        self.len += 1

    def clear(self) -> None:
        self.head = None
        self.tail = None
        self.len = 0

    def sort(self) -> None:
        # O(n²) complexity
        for _ in range(self.len):
            current : Node = self.head
            while current.next:
                if current.data > current.next.data:
                    current.switch(current.next)
                current = current.next

    def efficient_sort(self) -> None:
        # O(nlog(n) + 2n)
        # = O(nlog(n))

        sorted_l = [node.data for node in self]
        sorted_l.sort()

        current = self.head
        for value in sorted_l:
            current.data = value
            current = current.next

    def function(self, f) -> None:
        if not self.head:
            raise ValueError("LinkedList.function(f): List is empty")

        current : Node = self.head
        while current:
            current.data = f(current.data)
            current = current.next

    def reverse(self) -> None:
        if len(self) <= 1:
            return
        if len(self) == 2:
            self.head.data, self.tail.data = self.tail.data, self.head.data
            return

        current : Node = self.tail
        while current:
            current.next, current.previous = current.previous, current.next
            current = current.next
        self.head, self.tail = self.tail, self.head

    def push(self, data) -> None:
        if not self.head:
            self.head = Node(data)
            return

        node : Node = Node(data)
        self.head.previous = node
        node.next = self.head
        self.head = node
        self.len += 1

    def extend(self, other) -> None:
        if isinstance(other, LinkedList):
            self.tail.connect(other.head)
            self.tail = other.tail
            self.len += other.len


        elif isinstance(other, (tuple, list)):
            for item in other:
                self.append(item)

    def shallowcopy(self) -> object:
        return self

    def deepcopy(self) -> object:
        new_list : LinkedList = LinkedList()
        if not self.head:
            return new_list

        for node in self:
            data_current = node.data
            new_list.append(data_current)
        return new_list

    def count(self, data) -> int:
        if not self.head:
            return 0

        k : int = 0
        for node in self:
            if node.data == data:
                k += 1
        return k

    def index(self, data) -> int:
        if not self.head:
            raise ValueError("LinkedList.index(data): Linked List is empty")

        if self.head.data == data:
            return 0

        k : int = 0
        for node in self:
            if node.data == data:
                return k
            k += 1

        raise ValueError("LinkedList.index(data): data is not in the list")

    def pop(self, index : int = -1) -> Node:
        if self.len - index == 1 or index == -1:
            tail = self.tail
            self.__del_last()
            return tail

        match index:
            case 0:
                head = self.head
                self.__del_first()
                return head
            case _:
                k : int = 1
                current = self.head.next
                while current:
                    if k == index:
                        current.previous.connect(current.next)
                        self.len -= 1
                        return current
                    current = current.next
                    k += 1
                raise IndexError("LinkedList.pop(index): list index out of range")

    def find(self, target) -> bool:
        for node in self:
            if node.data == target:
                return True
        return False
