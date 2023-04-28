def gen_to_list(gen):
    return [gen_to_list(x) if hasattr(x, '__iter__') else x for x in gen]

class Lambda:
    def __init__(self, tree='.'):
        self.tree = tree

    @staticmethod
    def _prototype(attr):
        def fn(*args):
            return Lambda([attr] + [x.tree if type(x) is Lambda else x for x in args])
        fn.__name__ = attr
        return fn

    @staticmethod
    def _replace_args(tree, ai):
        for elem in tree:
            if elem == '.':
                yield next(ai)
            elif type(elem) == list:
                yield from _replace_args(tree, ai)
            else:
                yield elem

    @staticmethod
    def _run_tree(tree):
        v1, *va = [Lambda._run_tree(x) if type(x) is list else x for x in tree[1:]]
        return getattr(v1, tree[0])(*va)

    def __call__(self, *args):
        return Lambda._run_tree(gen_to_list(Lambda._replace_args(self.tree, iter(args))))

    def __str__(self): return '_'
    def __repr__(self): return '_'

method_dict = int.__dict__ | str.__dict__
for m, f in method_dict.items():
    if m not in Lambda.__class__.__dict__ and callable(f) and m not in ('__str__', '__repr__'):
        setattr(Lambda, m, Lambda._prototype(m))

_ = Lambda()
f = 2 * (_ + 1)
# print(f(1))
print(f.tree)