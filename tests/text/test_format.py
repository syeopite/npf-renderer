# TODO
# import hashlib
# import logging
#
# from npf_renderer.parse.text_block import TextBlockNPFParser
# from npf_renderer.format import Formatter
#
# from example_data import *
#
#
# def helper_function(raw, answer_hash):
#     parsed_results = []
#     for block in raw["content"]:
#         parsed_results.append(TextBlockNPFParser.process(block))
#
#     logging.info(f"Parsed: {parsed_results}")
#
#     formatter = Formatter(parsed_results)
#
#     rendered_result = formatter.render_content()
#
#
# def test_subtype_and_indent_level_parse():
#     helper_function(*subtype_and_indent_level_test)
#
