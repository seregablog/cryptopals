lint:
	docker-compose exec cryptopals flake8 cryptopals

runAll:
	docker-compose exec cryptopals python3 runAll.py
