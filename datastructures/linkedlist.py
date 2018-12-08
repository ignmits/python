class Node:
    def __init__(self,data):
        self.__data=data
        self.__next=None
    
    def get_data(self):
        return self.__data
    
    def set_data(self,data):
        self.__data=data
    
    def get_next(self):
        return self.__next
    
    def set_next(self,next_node):
        self.__next=next_node
    
class LinkedList:
    def __init__(self):
        self.__head=None
        self.__tail=None
    
    def get_head(self):
        return self.__head
    
    def get_tail(self):
        return self.__tail
    
    def add(self,data):
        new_node=Node(data)
        if(self.__head is None):
            self.__head=self.__tail=new_node
        else:
            self.__tail.set_next(new_node)
            self.__tail=new_node
    
    def display(self):
        temp=self.__head
        while(temp is not None):
            print(temp.get_data())
            temp=temp.get_next()

    def reverse_list(self):
        if (self.__head == self.__tail):
            return
        # temporary linked list for revers
        rlist = LinkedList()
        #set tail and head for the new list
        rlist.add(self.__head.get_data())
        temp_node = self.__head
        while(temp_node != self.__tail):
            #hop to the next node in the Link list
            temp_node = temp_node.get_next()
            #create new node
            new_node = Node(temp_node.get_data())
            #set new node as the head
            new_node.set_next(rlist.__head)
            rlist.__head = new_node   
        #reset the link list to the original
        self.__head = rlist.__head
        self.__tail = rlist.__tail
                                              
    #You can use the below __str__() to print the elements of the DS object while debugging
    def __str__(self):
        temp=self.__head
        msg=[]
        while(temp is not None):
           msg.append(str(temp.get_data()))
           temp=temp.get_next()
        msg=" ".join(msg)
        msg="Linkedlist data(Head to Tail): "+ msg
        return msg

    def traverse(self):
        temp = self.__head
        index = 0
        while(temp is not None):
            print ('\n[{}].node:data = {}'.format(index,temp.get_data()))          
            print ('[{}].node:addr = {}'.format(index,temp))
            print ('[{}].node:next = {}'.format(index,temp.get_next()))
            temp = temp.get_next()
            index += 1

def count_nodes(biscuit_list):
    count=0
    llist = biscuit_list
    if llist.get_head() == None:
        return 0
    else:
        node = llist.get_head()
        while (node is not None):
            count += 1
            #print(node.get_data())
            node = node.get_next()
    return count

biscuit_list=LinkedList()
biscuit_list.add("Goodday")
biscuit_list.add("Bourbon")
biscuit_list.add("Hide&Seek")
biscuit_list.add("Nutrichoice")
print(biscuit_list)
biscuit_list.reverse_list()
print(biscuit_list)
biscuit_list.traverse()