#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

class Solution{

public:

    void heapSort(int *array, int size)
    {
        int i = 0;

        for (i = size - 1; i > 0; --i)
        {
            // TODO: pop up the Largest one.
            cout << "largest: " << array[0] << endl;

            swap(array[0], array[i]);
            maxHeapify(array, 0, i);
        }
    }

    void buildMaxHeap(int *array, int size)
    {
        int startIndex = getParentIndex(size - 1);
        for ( int i = startIndex; i >= 0; --i)
        {
            maxHeapify(array, i, size);
        }
    }

    void printHeap(int *array, int size)
    {
        for (int i = 0; i < (size - 2) / 2; ++i)
        {
            cout << array[i] << ", ";
            if (i % (int)(pow(2, i)) == 0)
            {
                cout << endl;
            }
        }
        cout << endl;
    }

private:

    void maxHeapify(int *array, int index, int heap_size)
    {
        int left = getLeftChildIndex(index);
        int right = getRightChildIndex(index);

        int largest = index;
        if (left < heap_size && array[index] < array[left])
        {
            largest = left;
        }
        if (right < heap_size && array[largest] < array[right])
        {
            largest = right;
        }

        if (largest != index)
        {
            swap(array[largest], array[index]);
            maxHeapify(array, largest, heap_size);
        }
    }

    int getParentIndex(int current)
    {
        return (current - 1) >> 1;
    }
    
    int getLeftChildIndex(int current)
    {
        return (current << 1) + 1;
    }

    int getRightChildIndex(int current)
    {
        return (current << 1) + 2;
    }

    void swap(int &a, int &b)
    {
        int temp = a;
        a = b;
        b = temp;
        /*
        a = a + b;
        b = a - b;
        a = a - b;
        */
    }

};


int main()
{
    int a[] = {0, 9, 4, 3, 1, 2, 8, 7, 5, 6};
    int size = sizeof(a) / sizeof(int);

    Solution s;

    s.printHeap(a, size);
    s.buildMaxHeap(a, size);

    s.printHeap(a, size);
    s.heapSort(a, size);

    s.printHeap(a, size);

    return 0;
}
