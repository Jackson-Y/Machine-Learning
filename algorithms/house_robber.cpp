#include <iostream>
#include <algorithm> // std::max
#include <map>
#include <vector>

using namespace std;

struct TreeNode {
     int val;
     TreeNode *left;
     TreeNode *right;
     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 };

#ifdef _SOLUTION_1_

// recursion 递归，效率低，需要重复计算多次。
class Solution {

public:

    int rob(TreeNode* root) {
        if (root == NULL) return 0;

        int val = 0;

        if (root->left != null)
        {
            val += rob(root->left->left) + rob(root->left->right);
        }

        if (root->right != null)
        {
            val += rob(root->right->left) + rob(root->right->right);
        }

        return max(val + root->val, rob(root->left) + rob(root->right))
    }

};

#elif defined _SOLUTION_2_

class Solution {

public:

    int rob(TreeNode root) {
        return robSub(root, new map<TreeNode, int>());
    }

private:

    int robSub(TreeNode root, map<TreeNode, int> m)
    {
        if (root == NULL) return 0;
        if (m.find(root)) return m[root];

        int val = 0;

        if (root.left != NULL)
        {
            val += robSub(root.left->left, m) + robSub(root.left->right, m);
        }

        if (root.right != NULL)
        {
            val += robSub(root.right->left, m) + robSub(root.right->right, m);
        }

        val = max(val + root.val, robSub(root.left, m) + robSub(root.right, m));
        m.put(root, val);

        return val;
    }

};

#else

class Solution {

public:

    int rob(TreeNode* root)
    {
        vector<int> res = robSub(root);
        
        return max(res[0], res[1]);
    }

private:

    vector<int> robSub(TreeNode* root)
    {
        if (root == NULL)
        {
            return vector<int>(2,0);
        }

        vector<int> left = robSub(root->left);
        vector<int> right = robSub(root->right);

        vector<int> res(2, 0);
        res[0] = max(left[0], left[1]) + max(right[0], right[1]);
        res[1] = root->val + left[0] + right[0];

        return res;
    }

};

#endif


/*************
       3
      / \
     4   5
    / \   \
   1   3   1
**************/
int main(void)
{
    TreeNode root(3);
    TreeNode left_1(4);
    TreeNode right_1(5);
    TreeNode left_1_left_2(1);
    TreeNode left_1_right_2(3);
    TreeNode right_1_right_2(1);

    root.left = &left_1;
    root.right = &right_1;
    left_1.left = &left_1_left_2;
    left_1.right = &left_1_right_2;
    right_1.right = &right_1_right_2;

    Solution s;
    int money = s.rob(&root);
    cout << "Money: $" << money << endl;

    return 0;
}
