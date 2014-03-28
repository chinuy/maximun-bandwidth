import random
import sys

class Heap:

    def __init__(self):
        # array item type: tuple, (id, value)
        self.array = [(-1,-1)]

    def __len__(self):
        return len(self.array) -1

    def __contains__(self, item):
        "Return True if item id is in"
        for elm in self.array:
            if item is elm[0]:
                return True
        return False

    def getMin(self):
        return self.array[1]

    def insert(self, elm):
        self.array.append(elm)
        i_child = len(self.array) -1
        i_parent = int(i_child/2)
        if i_child > 2: # more than one element
            self.adjust(i_parent, i_child)

    def adjust(self, i_parent, i_child):
        #print self.array, i_parent, i_child
        if self.array[i_parent][1] > self.array[i_child][1]:
            self.swap(i_parent, i_child)
            self.adjust(int(i_parent/2), i_parent)

    def delete_root(self):
        if len(self) < 1:
            return

        root_index = 1
        self.array[root_index] = self.array[-1]
        del self.array[-1]
        self.downAdjust(root_index)

    def downAdjust(self, index):
        # check if index has been the lowest leave
        if index*2 > len(self):
            return

        #print self.array, index
        smaller_index = index*2
        c1 = self.array[index*2][1]
        c2 = sys.maxsize
        if len(self.array) > index*2 +1:
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

    def __init__(self):
        # array item type: tuple, (id, value)
        self.array = [(-1,sys.maxint)]

    def getMin(self):
        raise Exception("MaxHeap doesn't support getMin()")

    def getMax(self):
        return self.array[1]

    def adjust(self, i_parent, i_child):
        if self.array[i_parent][1] < self.array[i_child][1]:
            self.swap(i_parent, i_child)
            self.adjust(int(i_parent/2), i_parent)

    def downAdjust(self, index):
        # check if index has been the lowest leave
        if index*2 > len(self):
            return

        larger_index = index*2
        c1 = self.array[index*2][1]
        c2 = sys.maxsize
        if len(self.array) > index*2 +1:
            c2 = self.array[index*2+1][1]
        if c1 > c2:
            larger_index = index*2 +1

        if self.array[index][1] < self.array[larger_index][1]:
            self.swap(index, larger_index)
            self.downAdjust(larger_index)

def main():

    h = MaxHeap()
    x = range(10)
    random.shuffle(x)
    x = zip(range(10), [1,3,5,8,1,2,2,2,2,5])
    for i in x:
        h.insert(i)
    print h.array
    print "-- Test contains()"
    print 10 in h
    print 1 in h
    print "-- DELETE"
    for i in range(len(h)):
        h.delete_root()
    print h.array
    try:
        h.getMin()
    except Exception as e:
        print e

if __name__ == '__main__':
    main()
