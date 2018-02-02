#include <iostream>
#include <vector>

using namespace std;

#ifdef __DFS_SOLUTION__
class Solution{

public:

    int findCircleNumber(vector<vector<int> >& M)
    {
        if (M.empty()) return 0;

        int n = M.size();
        int groups = 0;
        vector<bool> visited(n, false);

        for (int i = 0; i < visited.size(); i++)
        {
            groups += !visited[i] ? dfs(i, M, visited), 1: 0;
        }

        return groups;
    }

private:

    void dfs(int i, vector<vector<int> >& M, vector<bool>& visited)
    {
        visited[i] = true;
        for (int j = 0; j < visited.size(); j++)
        {
            if (i != j && M[i][j] && !visited[j])
            {
                dfs(j, M, visited);
            }
        }
    }
};
#else
// UnionFind 并查集 [优化： 路径压缩，记录每个节点所属的根节点，根节点相同说明属于一个圈子 ]
class Solution{

public:

    int findCircleNumber(vector<vector<int> >& M)
    {
        if (M.empty()) return 0;
        int n = M.size();
        int i = 0;
        int j = 0;

        // initialize leads for every kid as themselves
        vector<int> leads(n, 0);
        for (i = 0; i < n; i++)
        {
            leads[i] = i;
        }

        int groups = n;
        for (i = 0; i < n; i++)
        {
            for (j = i + 1; j < n; j++)         // avoid recaculate M[i][j], M[j][i]
            {
                if (M[i][j])                    // 'i' is Friend of 'j'.
                {
                    int lead1 = findLeader(i, leads);
                    int lead2 = findLeader(j, leads);
                    if (lead1 != lead2)         // if 2 group belongs 2 different leads, merge 2 group to 1
                    {
                        leads[lead1] = lead2;
                        groups--;
                    }
                }
            }
        }

        return groups;
    }

private:

    int findLeader(int x, vector<int>& parents)
    {
        return parents[x] == x ? x : findLeader(parents[x], parents);
    }

};

#endif

void print(vector<vector<int> >& M)
{
    int n = M[0].size();
    cout << "size: " << n << endl;

    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            cout << M[i][j] << ", ";
        }
        cout << endl;
    }
    cout << endl;
}


int main(void)
{
    int i = 0;
    int j = 0;

    int arr[5][5] = {
        1, 1, 0, 0, 0,
        1, 1, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 1, 1,
        0, 0, 0, 1, 1
    };

    vector<vector<int> > M(5);
    for (i = 0; i < 5; ++i)
    {
        vector<int> r(arr[i], arr[i] + 5);
        M[i] = r;
    }

    print(M);

    Solution s;
    int group = s.findCircleNumber(M);

    cout << group << endl;

    return 0;
}
