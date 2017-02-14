
BLACK = 0
RED = 1

class Node(object):
    def __init__(self, key, value=None, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right



class RBNode(object):
    def __init__(self, color, key=None, value=None, parent=None, left=None, right=None):
        self.color = color
        self.key = key
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right


class Tree(object):

    def __init__(self):
        self.root = None

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def find(self, key):
        return self._find(self.root, key)

    def remove(self, key):
        self._remove(self.root, key)
        if self.root.left is None and self.root.right is None and self.root.key == key:
            self.root = None

    def visualize(self):
        self._visualize(self.root, '')


class BinaryTree(Tree):

    # def __init__(self):
    #     self.root = None

    # def insert(self, key, value):
    #     self.root = self._insert(self.root, key, value)

    # def find(self, key):
    #     return self._find(self.root, key)

    # def remove(self, key):
    #     self._remove(self.root, key)
    #     if self.root.left is None and self.root.right is None and self.root.key == key:
    #         self.root = None

    # def visualize(self):
    #     self._visualize(self.root, '')

    def _insert(self, node, key, value):
        if node is None:
            node = Node(key, value)
            return node

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value

        return node

    def _find(self, node, key):
        if node is None:
            raise KeyError(key)

        try:
            if key < node.key:
                return self._find(node.left, key)
            elif key > node.key:
                return self._find(node.right, key)
            else:
                return node.value
        except KeyError:
            raise KeyError(key)

    def _visualize(self, node, prefix):
        if node is None:
            return

        print '%s%s' % (prefix, node.key)
        self._visualize(node.left, prefix + '    ')
        self._visualize(node.right, prefix + '    ')

    def get_most_left(self, node):
        if node.left is not None:
            return self.get_most_left(node.left)
        else:
            return node

    def _remove(self, node, key):
        if node is None:
            return None

        if node.key < key:
            node.left = self._remove(node.left, key)
        elif node.key > key:
            node.right = self._remove(node.right, key)
        else:
            if node.left is not None and node.right is not None:
                if node.right.left is None:
                    node.key = node.right.key
                    node.right = node.right.right
                else:
                    most_left = self.get_most_left(node.right)
                    node.key = most_left.key
                    self._remove(node.right, key)
                return node
            elif node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            else:
                return node.left


class RBTree(Tree):

    def grandparent(self, node):
        if node is not None and node.parent is not None:
            return node.parent.parent

    def uncle(self, node):
        g = self.grandparent(node)

        if g is None:
            return None

        if node.parent == g.left:
            return g.right
        else:
            return g.left

    def rotate_left(self, node):
        print 'rotate left'
        pivot = node.right

        if pivot is None:
            pivot = RBNode(BLACK, parent=node)

        pivot.parent = node.parent
        if not node.parent is None:
            if node.parent.left == node:
                node.parent.left = pivot
            else:
                node.parent.right = pivot

        node.right = pivot.left
        if not pivot.left is None:
            pivot.left.parent = node

        node.parent = pivot
        pivot.left = node

    def rotate_right(self, node):
        print 'rotate right'
        pivot = node.left

        if pivot is None:
            pivot = RBNode(BLACK, parent=node)

        pivot.parent = node.parent
        if not node.parent is None:
            if node.parent.left == node:
                node.parent.left = pivot
            else:
                node.parent.right = pivot

        node.left = pivot.right
        if not pivot.right is None:
            pivot.right.parent = node

        node.parent = pivot
        pivot.right = node

    def _visualize(self, node, prefix):
        if node is None:
            print '%s - None' % (prefix)
            return

        print '%s(%s) - %s' % (prefix, node.color, node.key)
        self._visualize(node.left, prefix + '    ')
        self._visualize(node.right, prefix + '    ')

    def _insert(self, node, key, value, parent=None):
        if node is None:
            # color, key=None, value=None, parent=None, left=None, right=None, isnode
            node = RBNode(RED, key=key, value=value, parent=parent)
            # node.left = RBNode(BLACK, parent=node, isnode=False)
            # node.right = RBNode(BLACK, parent=node, isnode=False)
            self._insert_case1(node)
            return node

        if key < node.key:
            node.left = self._insert(node.left, key, value, node)
        elif key > node.key:
            node.right = self._insert(node.right, key, value, node)
        else:
            node.value = value
            node.color = RED
            # self._insert_case2(node)

        return node

    def _insert_case1(self, node):
        print 'insert 1'
        if node.parent is None:
            node.color = BLACK
        else:
            self._insert_case2(node)

    def _insert_case2(self, node):
        print 'insert 2'
        if node.parent.color == BLACK:
            # if node.parent.parent is not None and node.parent.parent.color == BLACK:
                # self.parent.color = RED
            return
        else:
            self._insert_case3(node)

    def _insert_case3(self, node):
        print 'insert 3'
        uncle = self.uncle(node)

        if uncle is not None and uncle.color == RED and node.parent.color == RED:
            node.parent.color = BLACK
            uncle.color = BLACK
            grand = self.grandparent(node)
            brand.color = RED
            self._insert_case1(grand)
        else:
            self._insert_case4(node)

    def _insert_case4(self, node):
        print 'insert 4'
        grand = self.grandparent(node)

        if node == node.parent.right and node.parent == grand.left:
            self.rotate_left(node.parent)
            node = node.left
        else:
            self.rotate_right(node.parent)
            node = node.right

        self._insert_case5(node)

    def _insert_case5(self, node):
        print 'insert 5'
        grand = self.grandparent(node)
        self.visualize()

        node.parent.color = BLACK
        grand.color = RED

        if node == node.parent.left and node.parent == grand.left:
            self.rotate_right(grand)
        else:
            self.rotate_left(grand)


