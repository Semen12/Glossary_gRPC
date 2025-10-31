import grpc

# Импортируем сгенерированные классы
from generated import dictionary_pb2
from generated import dictionary_pb2_grpc

def run():
    """
    Функция для запуска gRPC клиента и демонстрации всех CRUD-операций.
    """
    print("Запуск gRPC клиента...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = dictionary_pb2_grpc.DictionaryStub(channel)

        # --- 1. CREATE: Добавляем начальные термины ---
        print("\n--- 1. Добавление терминов (CREATE) ---")
        terms_to_add = [
            dictionary_pb2.Term(term="Дуплексная (полнодуплексная) связь", definition="в клиент‑серверном взаимодействии означает, что клиент и сервер могут одновременно передавать и принимать данные по одному соединению — без ожидания смены режима «приём/передача»"),
            dictionary_pb2.Term(term="GraphQL", definition="Язык запросов и среда выполнения для API"),
            dictionary_pb2.Term(term="gRPC", definition="Высокопроизводительный RPC фреймворк"),
            dictionary_pb2.Term(term="WebSocket", definition="Протокол для двусторонней связи")
        ]
        for term_obj in terms_to_add:
            request = dictionary_pb2.AddTermRequest(term_to_add=term_obj)
            response = stub.AddTerm(request)
            print(f"Ответ сервера: {response.message}")

        # --- 2. READ: Получаем все термины ---
        print("\n--- 2. Получение всех терминов (READ ALL) ---")
        all_terms_response = stub.GetAllTerms(dictionary_pb2.GetAllTermsRequest())
        print("Текущие термины в словаре:")
        for term in all_terms_response.terms:
            print(f"- {term.term}: {term.definition}")

        # --- 3. READ: Получаем один конкретный термин ---
        print("\n--- 3. Получение одного термина (READ ONE) ---")
        try:
            term_to_get = "GraphQL"
            print(f"Запрос термина '{term_to_get}'...")
            get_term_response = stub.GetTerm(dictionary_pb2.GetTermRequest(term=term_to_get))
            print(f"Найден термин: {get_term_response.term} - {get_term_response.definition}")
        except grpc.RpcError as e:
            print(f"Ошибка при получении термина: {e.details()}")

        # --- 4. UPDATE: Обновляем существующий термин ---
        print("\n--- 4. Обновление термина (UPDATE) ---")
        update_request = dictionary_pb2.UpdateTermRequest(
            original_term="gRPC",
            new_term_data=dictionary_pb2.Term(term="gRPC", definition="Современный RPC фреймворк от Google.")
        )
        update_response = stub.UpdateTerm(update_request)
        print(f"Ответ сервера: {update_response.message}")

        # --- 5. DELETE: Удаляем термин ---
        print("\n--- 5. Удаление термина (DELETE) ---")
        delete_request = dictionary_pb2.DeleteTermRequest(term="WebSocket")
        delete_response = stub.DeleteTerm(delete_request)
        print(f"Ответ сервера: {delete_response.message}")

        # --- 6. Проверка: Снова получаем все термины ---
        print("\n--- 6. Итоговое состояние словаря ---")
        final_terms_response = stub.GetAllTerms(dictionary_pb2.GetAllTermsRequest())
        print("Термины в словаре после всех операций:")
        if not final_terms_response.terms:
            print("Словарь пуст.")
        for term in final_terms_response.terms:
            print(f"- {term.term}: {term.definition}")
            
        # --- 7. Демонстрация обработки ошибок ---
        print("\n--- 7. Попытка получить удаленный термин ---")
        try:
            term_to_get = "WebSocket"
            print(f"Запрос термина '{term_to_get}'...")
            stub.GetTerm(dictionary_pb2.GetTermRequest(term=term_to_get))
        except grpc.RpcError as e:
            print(f"Ожидаемая ошибка: Статус='{e.code()}', Сообщение='{e.details()}'")


if __name__ == '__main__':
    run()