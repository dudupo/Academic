



if __name__ == "__main__":
    ret, n = [ ], 10
    for _ in range(10):
        ret += [ f'a{_} W a_{_}' ]
    def add_G(i,j):
        return [ 
                f'a{i} G A',
                f'+a{i} a{j}',
                f'a{i} G B',
                f'+a{i} a{j}',
                f'a{i} G C'
            ]
    ret += add_G(0,1)
    ret += add_G(2,3)
    ret += add_G(4,5)
    ret += add_G(6,7)
    ret += add_G(8,9)
    print("\n".join(ret))
