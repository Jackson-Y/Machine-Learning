#include <iostream>
#include <algorithm>
#include <vector>
#include <cmath>

using namespace std;

// 4 Solutions using Partition, Max-Heap, priority_queue and multiset respectively.

class BaseSolution{

public:

    // Using C++ Standord function sort().
    // Time O(nlogn), Space O(1)
    virtual int findKthLargest(vector<int> &nums, int k)
    {
        sort(nums.begin(), nums.end());
        return nums[k - 1];
    }

};

/*
Solution 1: 
    using Partition(idea from quick-sort).
    Worest Case: 
        Select the least pivot Every time.
        Time O(n^2), Space O(1)
    Average Case:
        Time O(n)
    Best Case:
        Select the middle one as pivot Every time. Time O(nlogn).
        Select the largest one as pivot Every time. Time O(k).
*/
class SolutionPartition : public BaseSolution{

public:

    int findKthLargest(vector<int> &nums, int k)
    {
        int left = 0;
        int right = nums.size() - 1;
        
        while(true){
            int pos = partition(nums, left, right);
            if (pos == k - 1)
            {
                return nums[pos];
            }

            if (pos > k - 1) 
            {
                right = pos - 1;
            }
            else
            {
                left = pos + 1;
            }
        }
    }

private:

    int partition(vector<int> &nums, int left, int right)
    {
        int pivot = nums[left];
        int l = left + 1;
        int r = right;
        
        while (l <= r)
        {
            if (nums[l] < pivot && nums[r] > pivot)
            {
                swap(nums[l++], nums[r--]);
            }
            if (nums[l] >= pivot) l++;
            if (nums[r] <= pivot) r--;
        }

        swap(nums[left], nums[r]);

        return r;
    }
};
/*
Solution 2: 
    using Max-Heap.
    1) Build Heap.
        Time O(K) about, SpaceO(K)
            高度 Height: 1-h, h = log(n+1);
            总节点数 Total-Node-Number: 1-n, n = 2^n - 1;
            层数 Layer-Number: 1-i
            每层节点数 Node-Number-per-Layer: 2^(i-1)
            最坏情况，
                倒数第一层节点需要向下比较 0 次，
                倒数第二层节点需要向下比较 1 次，
                倒数第三层节点需要向下比较 2 次，
                ...
                (每次只需要比较 与根节点交换的 分支即可)
            Time(h) = 2^(h) * 0 + 2^(h-1) * 1 + 2^(h-2) * 2 + ... + 2^1 * (h-1)
            错位相减法：
            等式两边同乘以 2，得：
            2*Time(h) = 2^(h+1) * 0 + 2^(h) * 1 + 2^(h-1) * 2 + ... + 2^2 * (h-1)
            Time(h) = 2*Time(h) - Time(h)
                    = 2^(h) * 1 + 2^(h-1) + 2^(h-2) + ... + 2^2 - 2^1(h-1)
                    = { 2^h + 2^(h-1) + 2^(h-2) + ... + 2^2 } - 2(h-1)
                    = { (4 - 2^(h+1) ) / (1-2) } - 2h +2         // 大括号{}内是等比数列求和公式.
                    = {2^(h+1) - 4} - 2h + 2
            lim{Time(h)} = lim{n - 2log(n) - 2}  = n             // h = log(n+1), n 足够大时.
        所以，建堆的时间复杂度大约为 Time O(n).
    2) Heapify.
        Time O(logK)
            每次调整只需选择当前节点的一个分支，因此调整节点的时间复杂度 O(logK).
        heap_sort时，对所有元素都进行一次调整，因此 Time O(nlogn).
*/
class SolutionHeap : public BaseSolution{

public:

    int findKthLargest(vector<int> &nums, int k)
    {
        int size = nums.size();
        int index = 0;
        vector<int> k_size_array;
        k = k < size ? k : size;

        for (index = 0; index < k; index ++)
        {
            k_size_array.push_back(nums[index]);
        }

        buildMinHeapify(k_size_array);

        for (; index < size; index++)
        {
            if (k_size_array[0] < nums[index])
            {
                swap(k_size_array[0], nums[index]);
                minHeapify(k_size_array, 0);
                //print_array(k_size_array);
            }
            
        }
        return k_size_array[0];
    }

    void print_array(vector<int> &nums)
    {
        vector<int>::iterator iter;
        for (iter = nums.begin(); iter != nums.end(); iter++)
        {
            cout << *iter << endl;
        }
        cout << endl;
    }

private:

    inline int leftChild(int index)
    {
        return ((index << 1) + 1);
    }

    inline int rightChild(int index)
    {
        return ((index << 1) + 2);
    }

    inline int parent(int index)
    {
        return ((index - 1) >> 1);
    }

    void minHeapify(vector<int> &array, int index)
    {
        int length = array.size();
        int left = leftChild(index);
        int right = rightChild(index);

        int least = index;
        if (left < length && array[index] > array[left])     // 切记先判断下标是否越界
        {
            least = left;
        }
        if (right < length && array[least] > array[right])   // 切记先判断下标是否越界
        {
            least = right;
        }
        
        if (least != index)
        {
            swap(array[least], array[index]);
            minHeapify(array, least);
        }
    }

    void buildMinHeapify(vector<int> &array)
    {
        int index = parent(array.size() - 1);

        for (; index >= 0; index--)
        {
            minHeapify(array, index);
        }
    }
};

/*
Solution 3: 
    using priority_queue.
    Time O(n), Space O(K)
*/
#include <queue>  // For priority_queue.
#include <functional> // For greater
class SolutionPriorityQueue : public BaseSolution{

public:
/*
    // Using queue-size: nums.size()
    int findKthLargest(vector<int> &nums, int k)
    {
        priority_queue<int> pq(nums.begin(), nums.end());
        for (int i = 0; i < k - 1; i++)
        {
            pq.pop();
        }
        return pq.top();
    }
*/

    // Using queue-size: k
    int findKthLargest(vector<int> &nums, int k)
    {
        priority_queue<int, vector<int>, greater<int> > pq;

        for (int i = 0; i < nums.size(); i++)
        {
            if (pq.size() == k)
            {
                int x = pq.top();
                if (nums[i] > x)
                {
                    pq.pop();
                    pq.push(nums[i]);
                }
            }
            else
            {
                pq.push(nums[i]);
            }
        }
        return pq.top();
    }
};

/*
Solution 4: 
    using multiset.
    Time O(n), Space O(K)
*/
#include <set>  // For multiset

class SolutionMultiset : public BaseSolution{

public:

    int findKthLargest(vector<int> &nums, int k)
    {
        multiset<int> mset;
        int n = nums.size();
        for (int i = 0; i < n; i++)
        {
            mset.insert(nums[i]);
            if (mset.size() > k)
            {
                mset.erase(mset.begin());
            }
            return *mset.begin();
        }
    }

};


int main(void)
{
    vector<int> nums;
    for (int i = 0; i < 100; i++)
    {
        nums.push_back(i);
    }

    SolutionHeap sh;

    int kth = sh.findKthLargest(nums, 5);
    cout << "Kth: " << kth << endl;

    return 0;
}
