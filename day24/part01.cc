#include <array>
#include <bitset>
#include <fstream>
#include <iostream>
#include <unordered_set>

constexpr int field_height = 5;
constexpr int field_width = 5;
constexpr int field_size = field_height * field_width;
constexpr char const* INPUT = "input_day24.txt";

std::array<int, field_size> generate_masks() {
    auto masks = std::array<int, 25>();
    for (int y = 0; y < field_height; ++y) {
        for (int x = 0; x < field_width; ++x) {
            const int pos = (y * field_width) + x;
            int mask = 0;
            if (x > 0)
                mask |= 1 << (y * field_width + (x - 1));
            if (x < (field_width - 1))
                mask |= 1 << (y * field_width + (x + 1));
            if (y > 0)
                mask |= 1 << ((y - 1) * field_width + x);
            if (y < (field_height - 1))
                mask |= 1 << ((y + 1) * field_width + x);
            masks[pos] = mask;
        }
    }
    return masks;
}

void print_field(int field) {
    for (int c = 0; c < field_size; ++c) {
        if (c % field_width == 0)
            std::cout << "\n";
        if (field & (1 << c))
            std::cout << '#';
        else
            std::cout << '.';
    }
    std::cout << "\n";
}

int read_input() {
	std::ifstream input(INPUT);
    char c;
    int result = 0;
    int mask = 1;
	while (input >> c) {
        if (c == '#')
            result |= mask;
        mask <<= 1;
	}
    return result;
}

int evolve(int field, const std::array<int, field_size>& masks) {
    int new_field = 0;
    for (int i = 0; i < field_size; ++i) {
        const int nbs = std::bitset<32>(field & masks[i]).count();
        const int has_bug = field & (1 << i);
        if (has_bug && nbs == 1) {
            new_field |= has_bug;
        } else if (!has_bug && (nbs == 1 || nbs == 2)) {
            new_field |= (1 << i);
        }
    }
    return new_field;
}

int main() {
    const auto masks = generate_masks();
    int field = read_input();
    auto seen = std::unordered_set<int>();
    while (1) {
        if (seen.insert(field).second == false) {
            std::cout << "Seen " << field << " twice\n";
            return 0;
        }
        field = evolve(field, masks);
    }
}
