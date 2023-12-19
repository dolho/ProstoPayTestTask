from unittest.mock import MagicMock

import pytest

from source.hashmap.hashmap import Hashmap


def test_hashmap_retrieves_values() -> None:
    custom_dict = Hashmap[str, str]()
    custom_dict["key1"] = "value1"
    custom_dict["key2"] = "value2"

    assert custom_dict["key1"] == "value1"
    assert custom_dict["key2"] == "value2"


def test_hashmap_handles_collisions() -> None:
    mock = MagicMock(
        return_value=1
    )  # hash function, that always return the same value, which results in collisions
    custom_dict = Hashmap[str, str](hash_function=mock)

    custom_dict["key1"] = "value1"
    mock.assert_called_with("key1")

    custom_dict["key2"] = "value2"
    mock.assert_called_with("key2")

    assert custom_dict["key1"] == "value1"
    assert custom_dict["key2"] == "value2"


def test_hashmap_handles_resizing() -> None:
    custom_dict = Hashmap[str, int](initial_size=5)

    for item in range(100):
        custom_dict[f"key{item}"] = item

    for item in range(100):
        assert custom_dict[f"key{item}"] == item


def test_hashmap_raises_key_error() -> None:
    custom_dict = Hashmap[str, str](initial_size=5)
    custom_dict["key1"] = "value1"

    with pytest.raises(KeyError):
        _ = custom_dict["non_existent_key"]


def test_hashmap_overwrites_values() -> None:
    custom_dict = Hashmap[str, str](initial_size=5)
    custom_dict["key1"] = "value1"

    new_value = "overwritten_key"
    custom_dict["key1"] = new_value

    assert custom_dict["key1"] == new_value


def test_hashmap_invalid_load_factor() -> None:
    with pytest.raises(ValueError):
        Hashmap[str, str](load_factor=-1)

    with pytest.raises(ValueError):
        Hashmap[str, str](load_factor=0)

    with pytest.raises(ValueError):
        Hashmap[str, str](load_factor=1.00001)

    Hashmap[str, str](load_factor=1)
    Hashmap[str, str](load_factor=0.5)


def test_hashmap_invalid_load_factor_initial_size() -> None:
    with pytest.raises(ValueError):
        Hashmap[str, str](load_factor=0.0001, initial_size=10)


def test_hashmap_invalid_initial_size() -> None:
    with pytest.raises(ValueError):
        Hashmap[str, str](load_factor=0.7, initial_size=-10)


def test_hashmap_invalid_key_type() -> None:
    custom_dict = Hashmap[str, str](initial_size=5)
    unhashable_key: list = []
    with pytest.raises(TypeError):
        custom_dict[unhashable_key] = "value"  # type: ignore
