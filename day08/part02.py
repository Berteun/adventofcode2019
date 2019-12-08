f = open("input_day09.txt")
image = f.read().strip()

#image = '0222112222120000';
width = 25
height = 6

pos = 0
fewest = width * height * 10
one_times_two = 0

pixels = [[None]*width for _ in range(height)]
pos = len(image) - width * height;
while pos >= 0:
    layer = image[pos:pos + width * height]
    for h in range(height):
        for w in range(width):
            p = h * width + w
            if layer[p] == '0':
                pixels[h][w] = '█'
            elif layer[p] == '1':
                pixels[h][w] = ' '

    pos -= width * height


print('█'*width)
for n in range(height):
    print(''.join(pixels[n]))
print('█'*width)
