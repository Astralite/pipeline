sample_product_data = [
	{
		"name": "T-Shirt",
		"tags": ["red", "large"],
		"code": "A21313"
	},
	{
		"name": "T-Shirt",
		"tags": ["green", "medium"],
		"code": "A21312"
	},
	{
		"name": "Pants",
		"tags": ["green", "medium"],
		"code": "A21455"
	},
	{
		"name": "Pants",
		"tags": ["fuschia", "small"],
		"code": "A21317"
	},
	{
		"name": "Socks",
		"tags": ["blue", "yellow", "medium", "small", "large"],
		"code": "A21319"
	},
	{
		"name": "Socks",
		"tags": ["green", "small", "medium", "large"],
		"code": "A21412"
	},
	{
		"name": "Jacket",
		"tags": ["blue", "medium"],
		"code": "A21501"
	},
	{
		"name": "Jacket",
		"tags": ["yellow", "small"],
		"code": "A21502"
	},
	{
		"name": "T-Shirt",
		"tags": ["black", "white", "large"],
		"code": "A21311"
	}
]

from collections import namedtuple
from pipeline import main
PreferenceMatch = namedtuple("PreferenceMatch", ["product_name", "product_codes"])

def test_should_filter_by_include_tags():
    include_tags = ['yellow', 'black', 'white']
    exclude_tags = []

    expectedOutput = [
        PreferenceMatch(product_name='Socks', product_codes=['A21319']),
        PreferenceMatch(product_name='Jacket', product_codes=['A21502']),
        PreferenceMatch(product_name='T-Shirt', product_codes=['A21311']),
    ]
    order_items = main(sample_product_data, include_tags, exclude_tags)
    assert order_items == expectedOutput

def test_should_return_empty_without_include_tags():
    include_tags = ['']
    exclude_tags = ['medium', 'small']

    expectedOutput = []
    order_items = main(sample_product_data, include_tags, exclude_tags)
    assert order_items == expectedOutput

def test_should_filter_by_include_and_exclude_tags():
    include_tags = ['medium', 'large']
    exclude_tags = ['red', 'blue']

    expectedOutput = [
        PreferenceMatch(product_name='T-Shirt', product_codes=['A21312', 'A21311']),
        PreferenceMatch(product_name='Pants', product_codes=['A21455']),
        PreferenceMatch(product_name='Socks', product_codes=['A21412']),
    ]
    order_items = main(sample_product_data, include_tags, exclude_tags)
    assert order_items == expectedOutput
