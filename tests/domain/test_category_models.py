from app.domain.category import CategoryCreate, Category


def test_category_create_valid():
    category = CategoryCreate(name="Electronics", description="Gadgets and tech")
    assert category.name == "Electronics"
    assert category.description == "Gadgets and tech"


def test_category_valid():
    category = Category(id=1, name="Electronics", description="Gadgets and tech")
    assert category.id == 1
    assert category.name == "Electronics"
