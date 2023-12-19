from typing import Callable, Generic, Hashable, TypeVar

# Key-Value types
K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class Hashmap(Generic[K, V]):
    def __init__(
        self,
        initial_size: int = 10,
        load_factor: float = 0.7,
        hash_function: Callable[[K], int] = hash,
    ):
        if not (0 < load_factor <= 1):
            raise ValueError(
                f"Load factor must be between 0 and 1, '{load_factor}' is given"
            )

        if initial_size * load_factor < 1:
            raise ValueError(
                f"Initial size '{initial_size}' with given load factor '{load_factor}' is invalid"
            )

        self._size = initial_size
        self._load_factor = load_factor
        self._threshold = int(self._size * self._load_factor)
        self._table: list[list[tuple[K, V]] | None] = [None] * self._size
        # Separate chaining collision resolution method is used

        self._num_elements = 0
        self._hash_function = hash_function

    def _hash(self, key: K) -> int:
        return self._hash_function(key) % self._size

    def _resize(self, new_size: int) -> None:
        old_table = self._table
        self._size = new_size
        self._threshold = int(self._size * self._load_factor)
        self._table = [None] * self._size
        self._num_elements = 0

        for entry in old_table:
            if entry is None:
                continue

            for key, value in entry:
                self[key] = value

    def __getitem__(self, key: K) -> V:
        hash_value = self._hash(key)
        searched_values = self._table[hash_value]
        if searched_values is not None:
            for stored_key, value in searched_values:
                if stored_key == key:
                    return value
        raise KeyError(key)

    def __setitem__(self, key: K, value: V) -> None:
        hash_value = self._hash(key)
        searched_values = self._table[hash_value]
        if searched_values is None:
            self._table[hash_value] = [(key, value)]
            self._num_elements += 1
        else:
            for i, (stored_key, _) in enumerate(searched_values):
                if stored_key == key:
                    searched_values[i] = (key, value)
                    break
            else:
                searched_values.append((key, value))
                self._num_elements += 1

        if self._num_elements > self._threshold:
            self._resize(self._size * 2)
