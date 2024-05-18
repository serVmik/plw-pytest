from typing import Generator

import pytest
from playwright.sync_api import Page, expect

from tests.utils import TODO_ITEMS, assert_number_of_todos_in_local_storage


@pytest.fixture(scope='function', autouse=True)
def run_around_tests(page: Page) -> Generator[None, None, None]:
    page.goto('https://demo.playwright.dev/todomvc')
    yield


def test_should_display_the_current_number_of_todo_items(page: Page) -> None:
    page.locator('.new-todo').fill(TODO_ITEMS[0])
    page.locator('.new-todo').press('Enter')
    expect(page.locator('.todo-count')).to_contain_text('1')

    page.locator('.new-todo').fill(TODO_ITEMS[1])
    page.locator('.new-todo').press('Enter')
    expect(page.locator('.todo-count')).to_contain_text('2')

    assert_number_of_todos_in_local_storage(page, 2)
