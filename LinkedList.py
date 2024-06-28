class Node:
    def __init__(self,data):
        self.previous = None
        self.data = data
        self.next = None
    
    def Switch(self,other) -> None:
        self.data,other.data = other.data,self.data

    def Connect(self) -> None:
        if self.previous and self.next:
            self.previous.next, self.next.previous = self.next, self.previous
        elif self.previous and not self.next:
            self.previous.next = None
        elif not self.previous and self.next:
            self.next.previous = None

class LinkedList:

    def __init__(self, *args):
        self.head = None
        self.tail = None
        self.len = 0
        
        for arg in args:
            self.append(arg)

    def __mul__(self, other):
        if isinstance(other, int):
            newList : LinkedList = LinkedList()
            current = self.head
            for i in range(self.len * other):
                if current is None:
                    current = self.head
                newList.append(current.data)
                current = current.next
            return newList
        raise Exception("Incorrect type")

    def __imul__(self, other):
        return self.__mul__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self,other):
        if type(other)!=type(self):
            raise Exception("TypeError: add operation not suited for "+str(type(other))+" and "+str(type(self)))

        self.tail.next = other.head
        
        newList : LinkedList = LinkedList()

        current = self.head
        while current:
            newList.append(current.data)
            current = current.next

        newList.len = self.len + other.len

        return newList

    def __len__(self):
        return self.len
    
    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next

    def __getitem__(self, index):
        if index == 0:
            return self.head
        elif index == -1:
            return self.tail

        if index > self.len:
            raise IndexError("Index out of range")        
        
        current = self.head.next
        count = 1
        while current:
            if count == index:
                return current
            current = current.next
            count += 1
    
    def __setitem__(self, index, data):
        self[index].data = data
        
    def __delitem__(self, key):
        self[key - 1].next, self[key + 1].previous = self[key + 1], self[key - 1]
    
    def __hash__(self) -> str:
        return hash((item for item in self))

    def __contains__(self, value) -> bool:
        current = self.head
        while current:
            if current.data == value:
                return True
        return False

    def __reversed__(self) -> object:
        current = self.tail
        newList = LinkedList()
        while current:
            newList.append(current.data)
            current = current.previous
            
        return newList
    
    def index(self, data) -> int:
        if self.head.data == data:
            return 0

        k = 1
        current = self.head.next
        while current:
            if current.data == data:
                return k
            
            current = current.next
            k += 1

        raise Exception("Data is not in the list")
    
    def pop(self, index=-1) -> Node:
        if self.len - index == 1 or index == -1:
            self.tail.previous.next = None
            self.len -= 1
            return self.tail

        match index:
            case 0:
                head = self.head
                self.head = self.head.next
                self.len -= 1
                return head
            case _:
                k = 1
                current = self.head.next
                while current:
                    if k == index:
                        current.Connect()
                        self.len -= 1
                        return current
                    current = current.next
                    k += 1
                raise IndexError("Index not in list")

    def print(self) -> None:
        if self.head:
            current=self.head
            print("[",end="")
        else:
            raise Exception("Linked list is empty")
        while current:
            if not current.next:
                print(str(current.data)+"]*")
                return
            print(str(current.data)+",",end="")
            current = current.next
    
    def append(self,data) -> None:
        node = Node(data)

        if self.head:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
            node.previous = current
        else:
            self.head = node

        self.tail = node
        self.len += 1

    def remove(self,data) -> None:
        current = self.head

        while current:
            if current.data == data:
                current.Connect()
                self.len -= 1
                return
            current = current.next

        raise Exception("Can't remove data as it is not existant")
    
    def insert(self,index,data) -> None:
        node=Node(data)
        if index==0:
            node.next,self.head.previous=self.head,node
            self.head=node
            self.len += 1
            return
        
        k=1
        current=self.head.next
        previous=current.previous
        while k!=index:
            previous=current
            current=current.next
            k+=1
        node.next=current
        current.previous=node
        previous.next,node.previous=node,previous
        self.len += 1

    def clear(self) -> None:
        self.head = None
        self.tail = None
        self.len = 0

    def sort(self) -> None:
        for i in range(self.len):
            current=self.head
            while current.next:
                if current.data>current.next.data:
                    current.Switch(current.next)
                current=current.next
    
    def count(self,x) -> int:
        current = self.head
        k = 0
        while current:
            if current.data == x:
                k += 1
            current = current.next
        return k

    def function(self, f) -> None:
        current = self.head
        while current:
            current.data = f(current.data)
            current = current.next
    
    def reverse(self) -> None:
        if len(self) <= 1:
            return
        if len(self) == 2:
            self.head.data, self.tail.data = self.tail.data, self.head.data
            return
        
        current = self.tail
        while current:
            current.next, current.previous = current.previous, current.next
            current = current.next
        self.head, self.tail = self.tail, self.head

    def push(self, data) -> None:
        if self.len == 0:
            self.head = Node(data)
            return
        
        node = Node(data)
        self.head.previous = node
        node.next = self.head
        self.head = node
        self.len += 1
        
    def copy(self) -> object:
        newList = LinkedList()
        if len(self) == 0:
            return newList

        current = self.head
        while current:
            dataCurrent = current.data
            newList.append(dataCurrent)
            current = current.next
        return newList

    def extend(self, other) -> None:
        if isinstance(other, LinkedList):
            self.tail.next = other.head
            self.tail = other.tail
            self.len += other.len
        elif isinstance(other, (tuple, list)):
            for item in other:
                self.append(item)
