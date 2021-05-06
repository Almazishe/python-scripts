


def main():
    containers = list(map(int, input().strip().split()))
    
    if not sorted(containers) == containers:
        print(-1)
    else:
        print(containers[-1] - containers[0])


if __name__ == '__main__':
    main()