# Классификация отзывов КиноПоиска

В данной работе я на небольшом наборе данных постараюсь провести классификацию отзывов с сайта КиноПоиска с использованием нейросетей. Основная идея - получить наилучший результат классификации по трем категориям отзывов: положительные, отрицательные и нейтральные. Так же я выдвигаю гипотезу, что нейтральные отзывы существенно снижают точность классификации из-за своей невыраженной эмоциональной окраски. Последним шагом исследования будет исключение этой категории из датасета и проверка гипотезы.

Для анализа я использую самостоятельно собранный датасет из 3000 отзывов по 1000 в каждой категории.

Весь код ноутбука исполнялся с помощью google colab.