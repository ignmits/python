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
    
class DLinkedList:
    def __init__(self):
        self.__head = None
        self.__tail = None


    def get_head(self):
        return self.__head


    def get_tail(self):
        return self.__tail


    def add(self,data):
        new_node=Node(data)
        if(self.__head is None):
            self.__head=self.__tail = new_node
        else:
            new_node.set_prev(self.__tail)
            self.__tail.set_next(new_node)
            self.__tail=new_node

    def delete(self,data):
        if self.__head == self.__tail == None:
            return False
        temp = self.__head
        while(temp is not None):
            if temp.get_data() == data:
                #check if data deleted is head node
                if temp == self.__head:
                    self.__head = self.__head.get_next()
                    # if no tail exist
                    if self.__head != None:
                        self.__head.set_prev(None)
                #check if data deleted is tail node
                elif temp == self.__tail:
                    self.__tail.get_prev().set_next(None)
                    self.__tail = self.__tail.get_prev()
                else:
                    temp.get_prev().set_next(temp.get_next())
                    temp.get_next().set_prev(temp.get_prev())
                #delete temp
                del temp
                return True
            temp = temp.get_next()
        return False

    def __str__(self):
        temp=self.__head
        msg=[]
        while(temp is not None):
           msg.append(str(temp.get_data()))
           temp=temp.get_next()
        msg=" -> ".join(msg)
        msg="\nLinkedlist data(Head to Tail): "+ msg
        return msg


    def traverse(self):
        temp = self.__head
        index = 0
        while(temp is not None):
            print ('\n[{}].node:data = {}'.format(index,temp.get_data()))
            print ('[{}].node:addr = {}'.format(index,temp))
            print ('[{}].node:prev = {}'.format(index,temp.get_prev()))
            print ('[{}].node:next = {}'.format(index,temp.get_next()))
            temp = temp.get_next()
            index += 1


dlist = DLinkedList()
#del dlist

while(True):
    print('\n\tMenu')
    print('\nA. Add Data')
    print('\nD. Delete Data')
    print('\nT. Traverse Data')
    print('\nQ. Quit')
    ch = input('\nChoice : ')
    ch = ch.upper()
    if ch == 'A':
        data = input('\nEnter data to add: ')
        dlist.add(data)
        print(dlist)
    if ch == 'D':
        data = input('\nEnter data to delete: ')
        if dlist.delete(data):
            print('\nData Deleted')
        else:
            print('\nData not found')
        print(dlist)
    if ch == 'T':
        dlist.traverse()
    if ch == 'Q':
        break