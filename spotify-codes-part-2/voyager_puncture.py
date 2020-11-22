from typing import List
import voyager_encode


def un_puncture(code: List[int], patterns: List[List[int]]):
    n = len(patterns[0])
    codes = []
    i = 0
    count = 0
    while i < len(code):
        c = []
        for p in patterns:
            if i >= len(code):
                break
            if p[count % n]:
                c.append(code[i])
                i += 1
            else:
                c.append(None)
        count += 1
        codes.append(c)
    return codes

def puncture(codes: List[List[int]], patterns: List[List[int]]):
    n = len(patterns[0])
    code = []
    for i, c in enumerate(codes):
        for ii, cc in enumerate(c):
            if patterns[ii][i % n]:
                code.append(cc)
    return code


if __name__ == "__main__":
    output = voyager_encode.encode([1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1], [[1], [1]])
    code = puncture(output, [[1, 0, 1], [1, 1, 0]])
    print(code)
    codes = un_puncture(code, [[1, 0, 1], [1, 1, 0]])
    for c in codes:
        print(c)