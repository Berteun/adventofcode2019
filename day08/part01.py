f = open("input_day09.txt")
image = f.read().strip()

width = 25
height = 6
pos = 0
fewest = width * height * 10
one_times_two = 0
while pos < len(image):
    layer = image[pos:pos + width * height]
    pos += width * height
    if (layer.count('0') < fewest):
        one_times_two = layer.count('1') * layer.count('2')
        fewest = layer.count('0')

print(one_times_two)
