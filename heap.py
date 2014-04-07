import random
import sys
import profile

DEFAULT_CAPACITY = 32
class Heap:

    def __init__(self, capacity=DEFAULT_CAPACITY):
        # array item type: tuple, (id, value)
        self.array = [None] * (capacity+1)

        self.array[0] = (-1,None)
        self.length = 0
        self.count = 0

    def __len__(self):
        return self.length

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
        self.length += 1
        if len(self.array) <= len(self):
            self.array.extend([None]*DEFAULT_CAPACITY)
        self.array[self.length] = elm
        i_child = len(self)
        i_parent = int(i_child/2)
        self.adjust(i_parent, i_child)

    def adjust(self, i_parent, i_child):
        if i_parent == 0:
            return
        if self.array[i_parent][1] > self.array[i_child][1]:
            self.swap(i_parent, i_child)
            self.adjust(int(i_parent/2), i_parent)

    def delete_root(self):
        if len(self) < 1:
            return

        root_index = 1
        self.array[root_index] = self.array[self.length]
        self.array[self.length] = None
        self.length -= 1
        self.downAdjust(root_index)

    def delete(self, item):
        """
        delete specific item
        1. find item index
        2. swap item with last item
        3. remove item at the last item
        4. start from item index, adjust up
        """
        for i in range(len(self)):
            elm = self.array[i+1]
            if item == elm[0]:
                self.swap(i+1, len(self))
                self.array[len(self)] = None
                self.length -=1
                self.adjust(int((i+1)/2), i+1)
                return

    def downAdjust(self, index):
        # check if index has been the lowest leave
        if index*2 > len(self):
            return

        #print self.array, index
        smaller_index = index*2
        c1 = self.array[index*2][1]
        c2 = sys.maxsize
        if len(self) > index*2:
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
        self.array[0] = (-1,None)

    def getMin(self):
        raise Exception("MaxHeap doesn't support getMin()")

    def getMax(self):
        return self.array[1]

    @profile.counted
    def adjust(self, i_parent, i_child):
        if i_parent == 0:
            return
        self.count +=1 # COUNTER
        if self.array[i_parent][1] < self.array[i_child][1]:
            self.swap(i_parent, i_child)
            self.adjust(int(i_parent/2), i_parent)

    @profile.counted
    def downAdjust(self, index):
        # check if index has been the lowest leave
        if index*2 > len(self):
            return

        self.count +=1 # COUNTER
        larger_index = index*2
        c1 = self.array[index*2][1]
        c2 = 0
        if len(self) > index*2:
            c2 = self.array[index*2+1][1]
        if c1 < c2:
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

    NUM_TEST = 20
    MIN_WEIGHT = 10000000
    MAX_WEIGHT = 1000000000
    r = []
    for i in range(NUM_TEST):
        r.append(random.randint(MIN_WEIGHT, MAX_WEIGHT))
    test_input = zip(range(-NUM_TEST-10, -10, 1), r)

    """
    h = MaxHeap(NUM_TEST)
    for t in test_input:
        h.insert(t)
    print h.array
    h.delete(-20)
    while(len(h)>0):
        r = h.getMax()
        h.delete_root()
        print r[1],
    print
    return
    """

    total = 50000
    _bin = 10
    for i in range(1,_bin+1):
        i = _bin - i +1
        n = int(total/_bin*i)
        h = MaxHeap(n)
        x = zip(range(n), range(n))
        random.shuffle(x)
        insert()

        contains()

        total_insert_time = 0
        total_call = 0
        prev_counter = h.adjust.called
        for t in test_input:
            h.insert(t)
            total_insert_time += h.insert.times
            #print h.adjust.called , prev_counter
            total_call += h.adjust.called - prev_counter
            #h.delete(t[0])
            prev_counter = h.adjust.called
        #print n, total_insert_time/len(test_input)
        print n, float(total_call)/len(test_input)

        #print n, insert.times, contains.times, delete.times ,h.adjust.called, h.downAdjust.called

    try:
        h.getMin()
    except Exception as e:
        print e


if __name__ == '__main__':
    main()
