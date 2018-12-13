class Node:
    def __init__(self,data):
        self.__data = data
        self.__next = None
        self.__prev = None
    
    def set_data(self,data):
        self.__data = data

    def get_data(self):
        return self.__data

    def set_next(self,node):
        self.__next = node

    def set_prev(self,node):
        self.__prev = node
    
    def get_next(self):
        return self.__next

    def get_prev(self):
        return self.__prev    
    
class Q_DLinkedList:
    def __init__(self):
        self.__head = None
        self.__tail = None


    def empty(self):
        return self.__head == self.__tail == None


    def full(self):
        return False


    def enqueue(self,data):
        new_node=Node(data)
        if(self.__head is None):
            self.__head=self.__tail = new_node
        else:
            new_node.set_next(self.__head)
            self.__head.set_prev(new_node)
            self.__head = new_node


    def dequeue(self):
        if self.empty():
            return None
        temp_node = self.__tail     
        if self.__tail == self.__head:
            self.__head = self.__tail = None        
        else:
            self.__tail.get_prev().set_next(None)
            self.__tail = self.__tail.get_prev()
        return temp_node.get_data()


    def __str__(self):
        if self.empty():
            return '\nQueue is Empty'
        temp=self.__head
        msg=[]
        while(temp is not None):
           msg.append(str(temp.get_data()))
           temp=temp.get_next()
        msg=" --> ".join(msg)
        msg="\nQueue : "+ msg
        return msg

queue = Q_DLinkedList()

while(True):
    print('\n\tMenu')
    print('\nN. En-Queue')
    print('\nD. De-Queue')
    print('\nF. Queue Full')
    print('\nE. Check Empty')
    print('\nP. Print Queue')
    print('\nQ. Quit')
    ch = input('\nChoice : ')
    ch = ch.upper()
    if ch == 'N':
        data = input('\nEnter data to En-Queue : ')
        queue.enqueue(data)
        print(queue)
    if ch == 'D':
        data = queue.dequeue()
        print('\nData De-queued : {}'.format(data))
        print(queue)
    if ch == 'F':
        if queue.full():
            print('\nQueue Full')
        else:
            print('\nQueue not Full')
    if ch == 'E':
        if queue.empty():
            print('\nQueue Empty')
        else:
            print('\nQueue not Empty')
    if ch == 'P':
        print(queue)
    if ch == 'Q':
        break