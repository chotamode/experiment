"""
Random Kanji Generator
Generates random Japanese kanji combinations to create obscure search queries
"""
import random


class KanjiGenerator:
    """Generates random kanji combinations for image searches"""

    # Common kanji ranges (CJK Unified Ideographs)
    KANJI_RANGES = [
        (0x4E00, 0x9FFF),  # Common kanji
        (0x3400, 0x4DBF),  # Extension A (rare)
    ]

    # Some interesting/weird kanji categories
    NATURE_KANJI = ['森', '山', '川', '海', '空', '雲', '雨', '雪', '花', '木', '石', '水', '火', '土', '風', '月', '星', '光']
    ABSTRACT_KANJI = ['夢', '心', '魂', '影', '闇', '虚', '幻', '謎', '無', '空', '零', '混', '沌', '深', '遠', '静', '動']
    COLOR_KANJI = ['赤', '青', '緑', '黄', '黒', '白', '紫', '桃', '茶', '銀', '金', '灰']
    CREATURE_KANJI = ['龍', '鳥', '魚', '虫', '獣', '蛇', '猫', '犬', '馬', '牛', '豚', '鼠', '猿', '狐', '狼', '鹿', '熊']
    MYSTICAL_KANJI = ['神', '仏', '鬼', '妖', '魔', '霊', '精', '聖', '呪', '符', '祭', '儀', '禁', '封', '術', '法']
    TIME_KANJI = ['昔', '古', '今', '未', '来', '永', '刹', '那', '瞬', '間', '時', '世', '代', '紀', '劫']

    ALL_THEMED_KANJI = (
        NATURE_KANJI + ABSTRACT_KANJI + COLOR_KANJI +
        CREATURE_KANJI + MYSTICAL_KANJI + TIME_KANJI
    )

    def __init__(self):
        self.last_query = None

    def generate_random_kanji(self, count=1):
        """Generate completely random kanji from Unicode ranges"""
        kanji = []
        for _ in range(count):
            range_choice = random.choice(self.KANJI_RANGES)
            code_point = random.randint(range_choice[0], range_choice[1])
            kanji.append(chr(code_point))
        return ''.join(kanji)

    def generate_themed_query(self, length=None):
        """Generate a search query using themed kanji"""
        if length is None:
            length = random.randint(2, 5)

        kanji = random.sample(self.ALL_THEMED_KANJI, min(length, len(self.ALL_THEMED_KANJI)))
        query = ''.join(kanji)
        self.last_query = query
        return query

    def generate_mixed_query(self, themed_count=None, random_count=None):
        """Generate a query mixing themed and random kanji"""
        if themed_count is None:
            themed_count = random.randint(1, 3)
        if random_count is None:
            random_count = random.randint(1, 3)

        themed = random.sample(self.ALL_THEMED_KANJI, min(themed_count, len(self.ALL_THEMED_KANJI)))
        random_kanji = list(self.generate_random_kanji(random_count))

        # Mix them up
        all_chars = themed + random_kanji
        random.shuffle(all_chars)

        query = ''.join(all_chars)
        self.last_query = query
        return query

    def generate_nonsense_query(self, length=None):
        """Generate completely nonsensical kanji combination"""
        if length is None:
            length = random.randint(3, 7)

        query = self.generate_random_kanji(length)
        self.last_query = query
        return query

    def generate_query(self, mode='mixed'):
        """
        Generate a search query based on mode

        Args:
            mode: 'themed', 'random', 'mixed', 'nonsense', 'auto'
        """
        if mode == 'auto':
            mode = random.choice(['themed', 'mixed', 'nonsense'])

        if mode == 'themed':
            return self.generate_themed_query()
        elif mode == 'random':
            return self.generate_nonsense_query()
        elif mode == 'mixed':
            return self.generate_mixed_query()
        elif mode == 'nonsense':
            return self.generate_nonsense_query()
        else:
            return self.generate_mixed_query()


if __name__ == '__main__':
    # Test the generator
    gen = KanjiGenerator()

    print("=== Random Kanji Generator Test ===\n")

    print("Themed queries:")
    for _ in range(5):
        print(f"  {gen.generate_themed_query()}")

    print("\nMixed queries:")
    for _ in range(5):
        print(f"  {gen.generate_mixed_query()}")

    print("\nNonsense queries:")
    for _ in range(5):
        print(f"  {gen.generate_nonsense_query()}")
