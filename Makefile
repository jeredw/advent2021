book: Advent\ of\ Code\ 2021.ipynb
	jupyter-book build Advent\ of\ Code\ 2021.ipynb

.PHONY: publish
publish:
	ghp-import -n -p -f _build/_page/Advent\ of\ Code\ 2021/html