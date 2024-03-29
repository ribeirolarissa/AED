class Node:
  RED = True
  BLACK = False

  def __init__(self, key, color = RED):
    if not type(color) == bool:
      raise TypeError("Bad value for color parameter, expected True/False but given %s" % color)
    self.color = color
    self.key = key
    self.left = self.right = self.parent = NilNode.instance()

  def __str__(self, level = 0, indent = "   "):
    s = level * indent + str(self.key)
    if self.left:
      s = s + "\n" + self.left.__str__(level + 1, indent)
    if self.right:
      s = s + "\n" + self.right.__str__(level + 1, indent)
    return s

  def __nonzero__(self):
    return True

  def __bool__(self):
    return True


class NilNode(Node):
  __instance__ = None

  @classmethod
  def instance(self):
    if self.__instance__ is None:
      self.__instance__ = NilNode()
    return self.__instance__

  def __init__(self):
    self.color = Node.BLACK
    self.key = None
    self.left = self.right = self.parent = None

  def __nonzero__(self):
    return False

  def __bool__(self):
    return False

class RedBlackTree:
  def __init__(self):
    self.root = NilNode.instance()
    self.size = 0

  def __str__(self):
    return ("(root.size = %d)\n" % self.size)  + str(self.root)

  def add(self, key):
    self.insert(Node(key))

  def insert(self, x):
    self.__insert_helper(x)

    x.color = Node.RED
    while x != self.root and x.parent.color == Node.RED:
      if x.parent == x.parent.parent.left:
        y = x.parent.parent.right
        if y and y.color == Node.RED:
          x.parent.color = Node.BLACK
          y.color = Node.BLACK
          x.parent.parent.color = Node.RED
          x = x.parent.parent
        else:
          if x == x.parent.right:
            x = x.parent
            self.__left_rotate(x)
          x.parent.color = Node.BLACK
          x.parent.parent.color = Node.RED
          self.__right_rotate(x.parent.parent)
      else:
        y = x.parent.parent.left
        if y and y.color == Node.RED:
          x.parent.color = Node.BLACK
          y.color = Node.BLACK
          x.parent.parent.color = Node.RED
          x = x.parent.parent
        else:
          if x == x.parent.left:
            x = x.parent
            self.__right_rotate(x)
          x.parent.color = Node.BLACK
          x.parent.parent.color = Node.RED
          self.__left_rotate(x.parent.parent)
    self.root.color = Node.BLACK

  def delete(self, z):
    if not z.left or not z.right:
      y = z
    else:
      y = self.successor(z)
    if not y.left:
      x = y.right
    else:
      x = y.left
    x.parent = y.parent

    if not y.parent:
      self.root = x
    else:
      if y == y.parent.left:
        y.parent.left = x
      else:
        y.parent.right = x

    if y != z: z.key = y.key

    if y.color == Node.BLACK:
      self.__delete_fixup(x)

    self.size -= 1
    return y

  def minimum(self, x = None):
    if x is None: x = self.root
    while x.left:
      x = x.left
    print("\n O mínimo é: ", x)
    return x

  def maximum(self, x = None):
    if x is None: x = self.root
    while x.right:
      x = x.right
    print("\n O Maximo é: ", x)
    return x

  def successor(self, x):
    if x.right:
      return self.minimum(x.right)
    y = x.parent
    while y and x == y.right:
      x = y
      y = y.parent
    print("\n O Sucessor é: ", y)
    return y

  def predecessor(self, x):
    if x.left:
      return self.maximum(x.left)
    y = x.parent
    while y and x == y.left:
      x = y
      y = y.parent
    print("\n O Predecessor é: ", y)
    return y

  def inorder_walk(self, x = None):
    if x is None: x = self.root
    x = self.minimum()
    while x:
      yield x.key
      x = self.successor(x)

  def reverse_inorder_walk(self, x = None):
    if x is None: x = self.root
    x = self.maximum()
    while x:
      yield x.key
      x = self.predecessor(x)

  def search(self, key, x = None):
    if x is None: x = self.root
    while x and x.key != key:
      if key < x.key:
        x = x.left
      else:
        x = x.right
    return x

  def is_empty(self):
    return bool(self.root)

  def black_height(self, x = None):
    if x is None: x = self.root
    height = 0
    while x:
      x = x.left
      if not x or x.is_black():
        height += 1
    return height

  def __left_rotate(self, x):
    if not x.right:
      raise "x.right is nil!"
    y = x.right
    x.right = y.left
    if y.left: y.left.parent = x
    y.parent = x.parent
    if not x.parent:
      self.root = y
    else:
      if x == x.parent.left:
        x.parent.left = y
      else:
        x.parent.right = y
    y.left = x
    x.parent = y

  def __right_rotate(self, x):
    if not x.left:
      raise "x.left is nil!"
    y = x.left
    x.left = y.right
    if y.right: y.right.parent = x
    y.parent = x.parent
    if not x.parent:
      self.root = y
    else:
      if x == x.parent.left:
        x.parent.left = y
      else:
        x.parent.right = y
    y.right = x
    x.parent = y

  def __insert_helper(self, z):
    y = NilNode.instance()
    x = self.root
    while x:
      y = x
      if z.key < x.key:
        x = x.left
      else:
        x = x.right

    z.parent = y
    if not y:
      self.root = z
    else:
      if z.key < y.key:
        y.left = z
      else:
        y.right = z

    self.size += 1

  def __delete_fixup(self, x):
    while x != self.root and x.color == Node.BLACK:
      if x == x.parent.left:
        w = x.parent.right
        if w.color == Node.RED:
          w.color = Node.BLACK
          x.parent.color = Node.RED
          self.__left_rotate(x.parent)
          w = x.parent.right
        if w.left.color == Node.BLACK and w.right.color == Node.BLACK:
          w.color = Node.RED
          x = x.parent
        else:
          if w.right.color == Node.BLACK:
            w.left.color = Node.BLACK
            w.color = Node.RED
            self.__right_rotate(w)
            w = x.parent.right
          w.color = x.parent.color
          x.parent.color = Node.BLACK
          w.right.color = Node.BLACK
          self.__left_rotate(x.parent)
          x = self.root
      else:
        w = x.parent.left
        if w.color == Node.RED:
          w.color = Node.BLACK
          x.parent.color = Node.RED
          self.__right_rotate(x.parent)
          w = x.parent.left
        if w.right.color == Node.BLACK and w.left.color == Node.BLACK:
          w.color = Node.RED
          x = x.parent
        else:
          if w.left.color == Node.BLACK:
            w.right.color = Node.BLACK
            w.color = Node.RED
            self.__left_rotate(w)
            w = x.parent.left
          w.color = x.parent.color
          x.parent.color = Node.BLACK
          w.left.color = Node.BLACK
          self.__right_rotate(x.parent)
          x = self.root
    x.color = Node.BLACK
    

arvore = RedBlackTree()

print("Programa da Arvore Vermelha e Preta")

while True:

    print("""
==========================================
==========================================
        Qual ação você deseja realizar?
        1 - Inserir
        2 - Deletar
        3 - Buscar 
        4 - Minimo
        5 - Maximo
        6 - Sucessor
        7 - Predecessor
        8 - Sair
==========================================
==========================================
    """)

    opcao = input("Digite aqui sua opção: ")

    if opcao == "1":
        x = int(input("Digite o número a ser inserido: "))
        arvore.add(x)
        continue
    if opcao == '2':
        x = int(input("Digite a opção que voçê deseja deletar: "))
        arvore.delete(x)
        continue
    if opcao == '3':
        x = int(input("Digite a opção que você deseja buscar: "))
        arvore.search(x)
        continue
    if opcao == "4":
        arvore.minimum()
        continue
    if opcao == "5":
        arvore.maximum()
        continue
    if opcao == "6":
        x = int(input("Digite o numero para saber o sucessor: "))
        arvore.successor(x)
        continue
    if opcao == "7":
        x = input("Digite o número para saber o predecessor: ")
        arvore.predecessor(x)
        continue

    if opcao == '8':
        break


