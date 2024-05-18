from typing import Generator

import pytest
from playwright.sync_api import Page, expect

from tests.utils import (
    TODO_ITEMS,
    check_number_of_completed_todos_in_local_storage,
    create_default_todos,
    check_todos_in_local_storage,
)


@pytest.fixture(autouse=True)
def run_around_tests(page: Page) -> Generator[None, None, None]:
    page.goto('https://demo.playwright.dev/todomvc')
    yield


def test_should_allow_me_to_mark_items_as_completed(page: Page) -> None:
    # Create two items.
    for item in TODO_ITEMS[:2]:
        page.locator('.new-todo').fill(item)
        page.locator('.new-todo').press('Enter')

    # Check first item.
    first_todo = page.locator('.todo-list li').nth(0)
    first_todo.locator('.toggle').check()
    expect(first_todo).to_have_class('completed')

    # Check second item.
    second_todo = page.locator('.todo-list li').nth(1)
    expect(second_todo).not_to_have_class('completed')
    second_todo.locator('.toggle').check()

    # Assert completed class.
    expect(first_todo).to_have_class('completed')
    expect(second_todo).to_have_class('completed')


def test_should_allow_me_to_un_mark_items_as_completed(page: Page) -> None:
    for item in TODO_ITEMS[:2]:
        page.locator('.new-todo').fill(item)
        page.locator('.new-todo').press('Enter')

    first_todo = page.locator('.todo-list li').nth(0)
    second_todo = page.locator('.todo-list li').nth(1)

    first_todo.locator('.toggle').check()
    expect(first_todo).to_have_class('completed')
    expect(second_todo).not_to_have_class('completed')
    check_number_of_completed_todos_in_local_storage(page, 1)

    first_todo.locator('.toggle').uncheck()
    expect(first_todo).not_to_have_class('completed')
    expect(second_todo).not_to_have_class('completed')
    check_number_of_completed_todos_in_local_storage(page, 0)


def test_should_allow_me_to_edit_an_item(page: Page) -> None:
    create_default_todos(page)

    todo_items = page.locator('.todo-list li')
    second_todo = todo_items.nth(1)

    second_todo.dblclick()
    expect(second_todo.locator('.edit')).to_have_value(TODO_ITEMS[1])
    second_todo.locator('.edit').fill('buy some sausages')
    second_todo.locator('.edit').press('Enter')

    expect(todo_items).to_have_text(
        [TODO_ITEMS[0], 'buy some sausages', TODO_ITEMS[2]])
    check_todos_in_local_storage(page, 'buy some sausages')
