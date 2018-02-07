#include <iostream>

using namespace std;

/*
LeetCode 141:

    1. 判断一个链表是否有环.
    2. 如果有环，返回环的入口点位置.
*/

struct Node{
    int value;
    struct Node *next;
    Node(int x):value(x),next(NULL){}
};

// Two Point (fast & slow)
//
// Time O(n), Space O(1)
//
class Solution{

public:
    int hasCycle(Node *head)
    {
        Node *slow = head;
        Node *fast = head;

        while (fast != NULL && fast->next != NULL)
        {
            slow = slow->next;
            fast = fast->next->next;

            if (fast == slow)
            {
                return 1;
            }
        }

        return 0;
    }

    int entryNodeOfLinkedList(Node *head)
    {
        if (head == NULL || head->next == NULL) return -1;

        int n = 0;
        Node *slow = head;
        Node *fast = head;

        while(fast != NULL && fast->next != NULL)
        {
            slow = slow->next;
            fast = fast->next->next;

            if (slow == fast)     // 快、慢指针相遇(fast pointer == slow pointer)
            {
                Node *p = head;
                Node *q = slow;
                while (p != q)
                {
                    ++n;
                    p = p->next;
                    q = q->next;
                }

                // return p; // 返回入口节点的指针
                return n; // 第n个(n=0,1,2,3...n)
            }
        }

        return -1; // 没有环
    }

};

int main(void)
{
    Node n1(1);
    Node n2(2);
    Node n3(3);
    Node n4(4);
    Node n5(5);
    Node n6(6);
    Node n7(7);
    Node n8(8);
    Node n9(9);
    Node n10(10);
    Node n11(11);

    n1.next = &n2;
    n2.next = &n3;
    n3.next = &n4;
    n4.next = &n5;
    n5.next = &n6;
    n6.next = &n7;
    n7.next = &n8;
    n8.next = &n9;
    n9.next = &n10;
    n10.next = &n11;
    n11.next = &n5;

    Solution s;

    int has_cycle = s.hasCycle(&n1);
    cout << "has_cycle: " << has_cycle << endl;

    int entry = s.entryNodeOfLinkedList(&n1);
    cout << "entry: " << entry << endl;

    return 0;
}

