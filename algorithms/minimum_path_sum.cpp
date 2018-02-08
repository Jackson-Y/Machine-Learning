#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

/*
    动态规划 DP (Dynamic Programming)
    到达当前节点的最小路径和：
        只需要知道：
            到达前一个节点的最小路径加上当前节点值。
            前一个节点有两个，分别是上方节点 和 左方节点。

    因此，递推公式：

        dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + g[i-1][j-1];

    // dp下标从1开始，g下标从0开始，方便 dp 数组循环调用及初始化。 
    // 因此，dp[i][j] 标识到达节点g[i-1][j-1]时的最短路径和。
*/

class Solution{

public:

    int minPathSum(vector<vector<int> > &g)
    {
        int m = g.size();
        if (m == 0) return 0;

        int n = g[m-1].size();

        vector<vector<int> > dp(m+1, vector<int>(n+1, INT_MAX));
        dp[0][1] = 0;

        for (int i = 1; i <= m; ++i)
        {
            for (int j = 1; j <= n; ++j)
            {
                dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + g[i-1][j-1];
            }
        }

        return dp[m][n];
    }

};


int main(void)
{
    return 0;
}
