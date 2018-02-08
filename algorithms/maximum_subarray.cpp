#include <iostream>
#include <algorithm>

using namespace std;


/*
    Time O(n)
*/

class Solution{

public:

    int maxSubArray(int *a, int size)
    {
        if (a == NULL || size <= 0) return 0;

        int cur_max_sum = a[0];
        int index = 0;
        int pre_max_sum = 0;

        for (index = 0; index < size; index++)
        {
            pre_max_sum += a[index];
            cur_max_sum = max(pre_max_sum, cur_max_sum);
            pre_max_sum = max(pre_max_sum, 0);
        }

        return cur_max_sum;
    }

};

int main(void)
{
    int a[] = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    int sum = 0;

    Solution s;
    sum = s.maxSubArray(a, sizeof(a) / sizeof(int));

    cout << "maxSum: " << sum << endl;

    return 0;
}
