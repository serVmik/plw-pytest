from playwright.sync_api import Page

TODO_ITEMS = ["buy some cheese", "feed the cat", "book a doctors appointment"]


def create_default_todos(page: Page) -> None:
    for item in TODO_ITEMS:
        page.locator('.new-todo').fill(item)
        page.locator('.new-todo').press('Enter')


def check_number_of_completed_todos_in_local_storage(
        page: Page,
        expected: int
) -> None:
    assert (
        page.evaluate(
            "JSON.parse(localStorage['react-todos']).filter(i => i.completed).length"   # Noqa: E501
        )
        == expected
    )


def assert_number_of_todos_in_local_storage(page: Page, expected: int) -> None:
    assert len(page.evaluate("JSON.parse(localStorage['react-todos'])")) == expected    # Noqa: E501


def check_todos_in_local_storage(page: Page, title: str) -> None:
    title in page.evaluate("JSON.parse(localStorage['react-todos']).map(i => i.title)")     # Noqa: E501
