import pytest
from assignment_1.online_shopping_cart.product.product_search import display_csv_as_table, display_filtered_table

# ----- TASK 3.2 -----
# Write 10 test cases for the function 'display_csv_as_table' located in  /online_shopping_cart/product/product_search.py


def test_display_csv_as_table_default_file(mocker, capsys):
    """Test that display_csv_as_table displays all products from default CSV file (as list)"""
    # Mock get_csv_data to return controlled data
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [
        ['Beans', '2', '10'],
        ['Banana', '1', '15'],
        ['Bread', '1.5', '8']
    ]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_csv_as_table()
    captured = capsys.readouterr()
    
    # Verify header is printed
    assert "['Product', 'Price', 'Units']" in captured.out
    # Verify some products are printed
    assert "Beans" in captured.out
    assert "Banana" in captured.out


def test_display_csv_as_table_with_missing_columns(mocker, capsys):
    """Test rows with fewer columns than header (incomplete data)"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [
        ['Cookies', '2'],              # Missing 'Units' column
        ['Biscuit'],                  # Missing 'Price' and 'Units'
        ['Donut', '1.5', '8']       # Complete row (normal)
    ]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_csv_as_table()
    captured = capsys.readouterr()
    
    # Should display all rows even with missing columns
    assert "Cookies" in captured.out
    assert "Biscuit" in captured.out
    assert "Donut" in captured.out
    # Header should still be present
    assert "Product" in captured.out


def test_display_csv_as_table_with_empty_strings(mocker, capsys):
    """Test data with empty string values in different columns"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [
        ['', '2', '10'],           # Empty product name
        ['Cereal', '', '10'],       # Empty price
        ['Flour', '1', ''],       # Empty units
        ['Bread', '1.5', '8']     # Normal row for comparison
    ]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_csv_as_table()
    captured = capsys.readouterr()
    
    # Should display all rows including those with empty strings
    assert "Cereal" in captured.out
    assert "Flour" in captured.out
    assert "Bread" in captured.out
    # Header should be present
    assert "['Product', 'Price', 'Units']" in captured.out


def test_display_csv_as_table_without_header(mocker, capsys):
    """Test CSV with empty header (no column names)"""
    mock_header = []  # Empty header
    mock_data = [
        ['Lotion', '200', '10'],
        ['Shampoo', '150', '5']
    ]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_csv_as_table()
    captured = capsys.readouterr()
    
    # Should still display data rows even without header
    assert "Lotion" in captured.out
    assert "Shampoo" in captured.out
    # Empty list should be printed
    assert "[]" in captured.out


def test_display_csv_as_table_with_extra_columns(mocker, capsys):
    """Test that rows with extra columns beyond header are displayed correctly"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [
        ['Tortilla', '2', '10', 'Extra1', 'Extra2'],  # 5 elements instead of 3
        ['Chips', '1', '15', 'ExtraData'],        # 4 elements instead of 3
        ['Salsa', '1.5', '8']                      # Normal 3 elements
    ]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_csv_as_table()
    captured = capsys.readouterr()
    
    # Should display all data including extra columns
    assert "Tortilla" in captured.out
    assert "Extra1" in captured.out
    assert "Extra2" in captured.out
    assert "Chips" in captured.out
    assert "ExtraData" in captured.out
    assert "Salsa" in captured.out


def test_display_csv_as_table_with_special_characters(mocker, capsys):
    """Test display_csv_as_table with special characters and symbols in data"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [
        ['Piña-Colada™', '12.99', '5'],     # Trademark symbol and hyphen
        ['Item #123 @50%', '99', '1'],      # Hash, at, percent symbols
        ['Product/Service', '25.00', '7'],  # Slash
        ['Test&Test', '5.5', '20']          # Ampersand
    ]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_csv_as_table()
    captured = capsys.readouterr()
    
    # Check all special characters are preserved in output
    assert "Piña-Colada™" in captured.out
    assert "Item #123 @50%" in captured.out
    assert "Product/Service" in captured.out
    assert "Test&Test" in captured.out


def test_display_csv_as_table_row_count(mocker, capsys):
    """Test that all rows from CSV are displayed"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [
        ['Product1', '1', '10'],
        ['Product2', '2', '20'],
        ['Product3', '3', '30'],
        ['Product4', '4', '40'],
        ['Product5', '5', '50'],
        ['Product6', '6', '60'],
        ['Product7', '7', '70'],
        ['Product8', '8', '80'],
        ['Product9', '9', '90'],
        ['Product10', '10', '100'],
        ['Product11', '11', '110']
    ]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_csv_as_table()
    captured = capsys.readouterr()
    
    # Count number of lines (should be header + data rows)
    lines = [line for line in captured.out.split('\n') if line.strip()]
    # Should have at least header + some data rows
    assert len(lines) > 10


def test_display_csv_as_table_preserves_order(mocker, capsys):
    """Test that products are displayed in CSV order"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [
        ['Apple', '2', '10'],
        ['Banana', '1', '15'],
        ['Orange', '1.5', '8']
    ]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_csv_as_table()
    captured = capsys.readouterr()
    
    # Find positions of products to verify order
    apple_pos = captured.out.find("Apple")
    banana_pos = captured.out.find("Banana")
    orange_pos = captured.out.find("Orange")
    
    # Verify Apple comes before Banana, and Banana before Orange
    assert apple_pos < banana_pos < orange_pos


def test_display_csv_as_table_with_empty_csv(mocker, capsys):
    """Test display_csv_as_table with only header (no data rows)"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = []
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_csv_as_table()
    captured = capsys.readouterr()
    
    # Should still show header
    assert "Product" in captured.out
    assert "Price" in captured.out
    assert "Units" in captured.out


def test_display_csv_as_table_file_not_found(mocker):
    """Test that FileNotFoundError is raised for non-existent file"""
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', side_effect=FileNotFoundError)
    
    with pytest.raises(FileNotFoundError):
        display_csv_as_table(csv_filename="nonexistent_file.csv")







# ----- TASK 3.2 -----
# Write 10 test cases for the function 'display_filtered_table' located in  /online_shopping_cart/product/product_search.py


def test_display_filtered_table_with_none_search_target(mocker, capsys):
    """Test that display_filtered_table calls display_csv_as_table when search_target is None"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [['Hat', '20', '10'], ['Coat', '100', '15']]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_filtered_table(search_target=None)
    captured = capsys.readouterr()
    
    # Should display all products like display_csv_as_table
    assert "Hat" in captured.out
    assert "Coat" in captured.out


def test_display_filtered_table_exact_match(mocker, capsys):
    """Test filtering with exact product name match"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [
        ['HotDog', '2', '10'],
        ['Salchicha', '1', '15'],
        ['Zuchini', '1.5', '8']
    ]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_filtered_table(search_target='HotDog')
    captured = capsys.readouterr()
    
    # Should only show Hot Dog
    assert "HotDog" in captured.out
    assert "Salchicha" not in captured.out
    assert "Zuchini" not in captured.out


def test_display_filtered_table_partial_match(mocker, capsys):
    """Test filtering where search_target contains the product name"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [
        ['Watermelon', '2', '10'],
        ['Melon', '5', '3'],
        ['Tape', '1', '15']
    ]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    # Search for 'Watermelon' which contains 'melon' as substring
    display_filtered_table(search_target='Watermelon')
    captured = capsys.readouterr()
    
    # Should show both Apple and Pineapple (both match the pattern)
    assert "Water" in captured.out
    assert "Melon" in captured.out
    assert "Tape" not in captured.out


def test_display_filtered_table_case_insensitive(mocker, capsys):
    """Test that filtering is case-insensitive"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [
        ['PASTA', '2', '10'],
        ['Tomato', '1', '15']
    ]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    # Search with lowercase
    display_filtered_table(search_target='pasta')
    captured = capsys.readouterr()
    
    assert "PASTA" in captured.out
    assert "Tomato" not in captured.out


def test_display_filtered_table_no_matches(mocker, capsys):
    """Test filtering when no products match"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [
        ['Cheesecake', '2', '10'],
        ['Cheese', '1', '15']
    ]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_filtered_table(search_target='Mango')
    captured = capsys.readouterr()
    
    # Should only show header, no products
    assert "Product" in captured.out
    assert "Cheesecake" not in captured.out
    assert "Cheese" not in captured.out


@pytest.mark.parametrize(
    "search_target,mock_data,expected_products,not_expected_products",
    [
        # search_target must CONTAIN the product name for it to match
        ('Grapes', [['Grape', '3', '5'], ['Apple', '2', '10']], ['Grape'], ['Apple']),
        ('Strawberry', [['Straw', '4', '12'], ['Berry', '3', '8'], ['Apple', '2', '10']], 
         ['Straw', 'Berry'], ['Apple']),
        ('Bell Pepper', [['Bell', '1.2', '8'], ['Pepper', '1.5', '5'], ['Tomato', '1', '15']], 
         ['Bell', 'Pepper'], ['Tomato'])
    ])
def test_display_filtered_table_multiple_scenarios(mocker, capsys, search_target, mock_data, 
                                                   expected_products, not_expected_products):
    """Test filtering with multiple search scenarios - search_target contains product names"""
    mock_header = ['Product', 'Price', 'Units']
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_filtered_table(search_target=search_target)
    captured = capsys.readouterr()
    
    # Check expected products appear (their names are contained in search_target)
    for product in expected_products:
        assert product in captured.out
    
    # Check unwanted products don't appear
    for product in not_expected_products:
        assert product not in captured.out


def test_display_filtered_table_header_always_displayed(mocker, capsys):
    """Test that header is always displayed even with no matches"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [['Apple', '2', '10']]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_filtered_table(search_target='NonExistent')
    captured = capsys.readouterr()
    
    # Header should always be present
    assert "['Product', 'Price', 'Units']" in captured.out


def test_display_filtered_table_all_products_match(mocker, capsys):
    """Test when search target contains all product names"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [
        ['App', '3', '5'],
        ['le', '5', '2'],
        ['ppl', '2', '10']
    ]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    # Search for 'Apple' which contains 'App', 'le', and 'ppl'
    display_filtered_table(search_target='Apple')
    captured = capsys.readouterr()
    
    # All products should appear (all their names are substrings of 'Apple')
    assert "App" in captured.out
    assert "le" in captured.out
    assert "ppl" in captured.out


def test_display_filtered_table_single_character_search(mocker, capsys):
    """Test filtering with single character search"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [
        ['A', '2', '10'],
        ['B', '3', '5'],
        ['C', '1', '15']
    ]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    # Search for 'ABC' which contains 'A', 'B', and 'C'
    display_filtered_table(search_target='ABC')
    captured = capsys.readouterr()
    
    # Should match all products whose names are contained in 'ABC'
    assert "A" in captured.out
    assert "B" in captured.out
    assert "C" in captured.out


def test_display_filtered_table_newline_format(mocker, capsys):
    """Test that output starts with newline"""
    mock_header = ['Product', 'Price', 'Units']
    mock_data = [['Apple', '2', '10']]
    mocker.patch('assignment_1.online_shopping_cart.product.product_search.get_csv_data', return_value=(mock_header, mock_data))
    
    display_filtered_table(search_target='Apple')
    captured = capsys.readouterr()
    
    # Should start with newline
    assert captured.out.startswith('\n')

