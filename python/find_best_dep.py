#!/usr/bin/env python3.6


def process_block(block: str):
    d = dict()
    lines = block.split('\n')
    name = lines[0]
    total = int(lines[1])
    for line in lines[3:]:
        if line.startswith('```'):
            break
        pair = line.split(':')
        assert len(pair) == 2
        k, v = int(pair[0]), int(pair[1])
        if k != 0:
            d[k] = v
    sum_all = sum(d.values())
    d[0] = total - sum_all
    sum_all = sum(d.values())
    print('{} insts in all'.format(sum_all))
    s = 0
    for n in sorted(d.keys()):
        # print(n, d[n])
        s += d[n]
        if 4 <= n <= 8:
            print("{} dependancies coverd {} of {}".format(n, s/sum_all, name))
            if s/sum_all >= 0.995:
                break
        elif s/sum_all >= 0.995:
            print("{} dependancies coverd {} of {}".format(n, s/sum_all, name))
            break
        elif s/sum_all >= 0.99:
            print("{} dependancies coverd {} of {}".format(n, s/sum_all, name))


def process(content: str):
    blocks = content.split('###')
    for block in blocks:
        if len(block):
            process_block(block)


def main():
    f = open('../history.md')
    content = f.read()
    f.close()
    process(content)



if __name__ == '__main__':
    main()

