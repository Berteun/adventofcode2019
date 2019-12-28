#include <array>
#include <bitset>
#include <fstream>
#include <iostream>
#include <unordered_set>

constexpr int field_height = 5;
constexpr int field_width = 5;
constexpr int field_size = field_height * field_width;
constexpr char const* INPUT = "input_day24.txt";

using masks_t = std::array<int, field_size>;
constexpr masks_t generate_outer_masks() {
    auto masks = masks_t();
    for (int y = 0; y < field_height; ++y) {
        for (int x = 0; x < field_width; ++x) {
            const int pos = (y * field_width) + x;
            int mask = 0;
            if (x == 0)
                mask |= (1 << 11);
            if (x == field_width - 1)
                mask |= (1 << 13);
            if (y == 0)
                mask |= (1 <<  7);
            if (y == field_height - 1)
                mask |= (1 << 17);
            masks[pos] = mask;
        }
    }
    return masks;
}

constexpr masks_t generate_inner_masks() {
    auto masks = masks_t();
    masks[7] = (0b11111);
    masks[11] = (1 << 0 | (1 << 5) | (1 << 10) | (1 << 15) | (1 << 20));
    masks[13] = (1 << 4 | (1 << 9) | (1 << 14) | (1 << 19) | (1 << 24));
    masks[17] = (0b11111 << 20);
    return masks;
}

constexpr masks_t generate_masks() {
    auto masks = masks_t();
    for (int y = 0; y < field_height; ++y) {
        for (int x = 0; x < field_width; ++x) {
            const int pos = (y * field_width) + x;
            int mask = 0;
            if (x > 0)
                mask |= (x > 0) << (y * field_width + (x - 1));
            mask |= (x < (field_width - 1)) << (y * field_width + (x + 1));
            if (y > 0)
                mask |= (y > 0)  << ((y - 1) * field_width + x);
            mask |= (y < (field_height - 1)) << ((y + 1) * field_width + x);
            masks[pos] = mask;
        }
    }
    return masks;
}

void print_field(int field) {
    for (int c = 0; c < field_size; ++c) {
        if (c % field_width == 0)
            std::cout << "\n";
        if (c == 12)
            std::cout << "?";
        else if (field & (1 << c))
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

constexpr int MINUTES = 200;
constexpr int LEVELS = 2 * MINUTES + 2;
constexpr int START_LEVEL = MINUTES + 1;
using levels_t = std::array<int, LEVELS>;

levels_t evolve(const levels_t& levels, int iteration, const masks_t& masks, const masks_t& inner_masks, const masks_t& outer_masks) {
    auto new_levels = levels_t();
    for (int l = START_LEVEL - iteration - 1; l <= START_LEVEL + iteration + 1; ++l) {
        int new_field = 0;
        for (int i = 0; i < field_size; ++i) {
            if (i == (field_size) / 2) {
                continue;
            }

            auto& outer_field = levels[l - 1];
            auto& field = levels[l];
            auto& inner_field = levels[l + 1];

            const int nbs = (
                      std::bitset<32>(inner_field & inner_masks[i]).count()
                    + std::bitset<32>(outer_field & outer_masks[i]).count()
                    + std::bitset<32>(field & masks[i]).count()
            );
            const int has_bug = field & (1 << i);
            if (has_bug && nbs == 1) {
                new_field |= has_bug;
            } else if (!has_bug && (nbs == 1 || nbs == 2)) {
                new_field |= (1 << i);
            }
        }
        new_levels[l] = new_field;
    }
    return new_levels;
}

int bug_count(const levels_t& levels) {
    int sum = 0;
    for (auto level : levels)
        sum += std::bitset<32>(level).count();
    return sum;
}

int main() {
    const auto masks = generate_masks();
    const auto inner_masks = generate_inner_masks();
    const auto outer_masks = generate_outer_masks();
    int field = read_input();
    auto levels = levels_t();

    levels[START_LEVEL] = field;
    for (int i = 0; i < MINUTES; ++i) {
        levels = evolve(levels, i, masks, inner_masks, outer_masks);
        /*
        std::cout << "------------ " << (i+1) << " ----------\n";
        for (int l = START_LEVEL - 6; l <= START_LEVEL + 6; ++l) {
            std::cout << "Level " << (l - START_LEVEL);
            print_field(levels[l]);
        }
        */
    }
    std::cout << "minute " << MINUTES << ", bugs: " << bug_count(levels) << "\n";
}
