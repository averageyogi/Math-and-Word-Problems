f=lambda a,n=1:print(''.join(j*(n%i<1)for i,j in a)or n)+f(a,n+1)

def g(N,a):
    for n in range(1,N+1):
        print(''.join(j*(n%i<1)for i,j in a)or n)


if __name__ == "__main__":
    g(1000, [[4, "Foo"], [7, "Bar"], [9, "Baz"]])
    f([[4, "Foo"], [7, "Bar"], [9, "Baz"]])
