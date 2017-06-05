The command used to generate coverage for front-end:
coverage run --branch --omit=.env*,lang_cfg*,tests* -m unittest tests/test_crawler.py tests/test_test_executor.py tests/test_data_interpreter.py tests/test_main.py tests/test_compilation_executor.py
