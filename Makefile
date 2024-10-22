lint:
	docker-compose exec cryptopals python3 -m flake8 cryptopals

runAll:
	docker-compose exec cryptopals python3 runAll.py
