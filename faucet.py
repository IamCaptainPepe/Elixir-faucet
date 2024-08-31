from web3 import Web3

# Подключение к общедоступному RPC-провайдеру сети Sepolia
sepolia_rpc_url = 'https://sepolia.rpc.thirdweb.com'
w3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))

# Проверка подключения
if not w3.is_connected():
    raise Exception("Не удалось подключиться к сети Sepolia")

# Функция для обработки транзакции
def process_transaction(private_key):
    try:
        print(f"Обработка транзакции для ключа: {private_key}")

        # Получаем адрес из приватного ключа
        account = w3.eth.account.from_key(private_key)
        sender_address = account.address

        print(f"Адрес отправителя: {sender_address}")

        # Удаляем префикс '0x' из адреса
        address_no_prefix = sender_address[2:]

        # Константная строка data для передачи 1000 токенов
        data_template = f'0xc63d75b6000000000000000000000000{address_no_prefix}00000000000000000000000000000000000000000000003635c9adc5dea00000'

        # Получаем текущую цену газа
        gas_price = w3.eth.gas_price

        # Получаем nonce
        nonce = w3.eth.get_transaction_count(sender_address)

        # Оценка лимита газа
        transaction = {
            'chainId': 11155111,
            'to': '0x800eC0D65adb70f0B69B7Db052C6bd89C2406aC4',
            'from': sender_address,
            'nonce': nonce,
            'gas': 0,  # Установим временно 0, так как будем рассчитывать лимит газа
            'gasPrice': gas_price,
            'data': data_template,
            'value': 0
        }

        # Используем estimate_gas для вычисления необходимого лимита газа
        gas_limit = w3.eth.estimate_gas(transaction)
        print(f"Оценка лимита газа: {gas_limit}")

        # Обновляем данные транзакции с расчетным лимитом газа
        transaction['gas'] = gas_limit

        # Подписываем транзакцию
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

        # Отправляем транзакцию в сеть
        txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        # Выводим хэш транзакции
        print(f"Хэш транзакции: {w3.to_hex(txn_hash)}")

    except Exception as e:
        print(f"Ошибка при обработке транзакции с ключом {private_key}: {e}")

# Чтение приватных ключей из файла
with open('private_keys.txt', 'r') as file:
    private_keys = file.readlines()

# Обрабатываем каждый приватный ключ
if not private_keys:
    print("Файл с приватными ключами пуст или не найден.")
else:
    for key in private_keys:
        key = key.strip()  # Удаляем пробелы и символы новой строки
        if key:
            process_transaction(key)
