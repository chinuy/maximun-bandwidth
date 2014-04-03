import random
import sys
import profile

DEFAULT_CAPACITY = 32
class Heap:

    def __init__(self, capacity=DEFAULT_CAPACITY):
        # array item type: tuple, (id, value)
        self.array = [None] * (capacity+1)

        self.array[0] = (-1,-1)
        self.len = 0

    def __len__(self):
        return self.len

    def __contains__(self, item):
        "Return True if item id is in"
        for i in range(len(self)):
            elm = self.array[i+1]
            if item is elm[0]:
                return True
        return False

    def getMin(self):
        return self.array[1]

    @profile.timeit
    def insert(self, elm):
        self.len += 1
        if len(self.array) <= len(self):
            self.array.extend([None]*DEFAULT_CAPACITY)
        self.array[self.len] = elm
        i_child = len(self)
        i_parent = int(i_child/2)
        if i_child > 2: # more than one element
            self.adjust(i_parent, i_child)

    def adjust(self, i_parent, i_child):
        #print self.array, i_parent, i_child
        if self.array[i_parent][1] > self.array[i_child][1]:
            self.swap(i_parent, i_child)
            self.adjust(int(i_parent/2), i_parent)

    @profile.timeit
    def delete_root(self):
        if len(self) < 1:
            return

        root_index = 1
        self.array[root_index] = self.array[self.len]
        self.array[self.len] = None
        self.len -= 1
        self.downAdjust(root_index)

    def delete(self, item):
        """
        delete specific item
        1. find item index
        2. swap item with root
        3. remove item at the root
        4. start from item index, adjust up
        """
        for i in range(len(self)):
            elm = self.array[i+1]
            if item is elm[0]:
                self.swap(i+1, len(self)-1)
                self.adjust(int((i+1)/2), i+1)

    def downAdjust(self, index):
        # check if index has been the lowest leave
        if index*2 > len(self):
            return

        #print self.array, index
        smaller_index = index*2
        c1 = self.array[index*2][1]
        c2 = sys.maxsize
        if len(self) > index*2 +1:
            c2 = self.array[index*2+1][1]
        if c1 > c2:
            smaller_index = index*2 +1

        if self.array[index][1] > self.array[smaller_index][1]:
            self.swap(index, smaller_index)
            self.downAdjust(smaller_index)

    def swap(self, a, b):
        self.array[a], self.array[b] = self.array[b], self.array[a]
        return

class MaxHeap(Heap):

    def __init__(self, capacity=DEFAULT_CAPACITY):
        # array item type: tuple, (id, value)
        Heap.__init__(self, capacity)
        self.array[0] = (-1,sys.maxint)

    def getMin(self):
        raise Exception("MaxHeap doesn't support getMin()")

    def getMax(self):
        return self.array[1]

    @profile.counted
    def adjust(self, i_parent, i_child):
        if self.array[i_parent][1] < self.array[i_child][1]:
            self.swap(i_parent, i_child)
            self.adjust(int(i_parent/2), i_parent)

    @profile.counted
    def downAdjust(self, index):
        # check if index has been the lowest leave
        if index*2 > len(self):
            return

        larger_index = index*2
        c1 = self.array[index*2][1]
        c2 = sys.maxsize
        if len(self) > index*2 +1:
            c2 = self.array[index*2+1][1]
        if c1 > c2:
            larger_index = index*2 +1

        if self.array[index][1] < self.array[larger_index][1]:
            self.swap(index, larger_index)
            self.downAdjust(larger_index)

def main():

    @profile.timeit
    def insert():
        #print "-- Inserting"
        for i in x:
            h.insert(i)

    @profile.timeit
    def contains():
        #print "-- Test contains()"
        #print 10 in h
        1 in h

    @profile.timeit
    def delete():
        #print "-- DELETE"
        for i in range(len(h)):
            h.delete_root()

    test_input = zip(range(10), [1,3,5,8,1,2,2,2,2,5])
    total = 50000000
    _bin = 100
    for i in range(_bin):
        #i = _bin - i
        n = int(total/_bin*i)
        h = MaxHeap(n)
        x = zip(range(n), range(n))
        random.shuffle(x)
        insert()

        contains()

        for t in test_input:
            h.insert(t)
            print h.insert.times

        delete()
        print n, insert.times, contains.times, delete.times ,h.adjust.called, h.downAdjust.called

    try:
        h.getMin()
    except Exception as e:
        print e


if __name__ == '__main__':
    main()
