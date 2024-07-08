document.addEventListener('DOMContentLoaded', () => {
    // Функция для отправки запроса на сервер и получения данных
    const fetchData = () => {
        fetch('http://localhost:8000/api/data')
            .then(response => response.json())
            .then(data => {
                // Обработка полученных данных
                document.getElementById('responseData').innerText = data.message;
            })
            .catch(error => console.error('Error:', error));
    };

    // Добавляем обработчик события на кнопку
    document.getElementById('fetchData').addEventListener('click', fetchData);
});