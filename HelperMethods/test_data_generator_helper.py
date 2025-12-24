import random
import string


class DataGenerator:

    @staticmethod
    def generate_unique_text(length=5):
        """Generate a random string of letters and digits with given length."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
