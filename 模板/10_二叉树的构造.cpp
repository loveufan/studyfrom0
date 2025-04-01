#include <iostream>
#include <queue>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* constructTree(vector<int> nodes) {
    if(nodes.empty() || nodes[0] == -1) return nullptr;
    
    queue<TreeNode*> q;
    TreeNode* root = new TreeNode(nodes[0]);
    q.push(root);
    
    int index = 1;
    while(!q.empty() && index < nodes.size()) {
        TreeNode* current = q.front();
        q.pop();
        
        // 处理左子节点
        if(nodes[index] != -1) {
            current->left = new TreeNode(nodes[index]);
            q.push(current->left);
        }
        index++;
        
        // 处理右子节点
        if(index < nodes.size() && nodes[index] != -1) {
            current->right = new TreeNode(nodes[index]);
            q.push(current->right);
        }
        index++;
    }
    return root;
}