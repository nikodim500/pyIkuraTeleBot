<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Пример вывода ломаной линии, с использованием JavaScript API Яндекс.Карт 2.х</title>
<!-- Подключаем API  карт 2.x  -->
<script src="http://api-maps.yandex.ru/2.0/?load=package.full&lang=ru-RU" type="text/javascript"></script>
<script type="text/javascript">
        // Как только будет загружен API и готов DOM, выполняем инициализацию
        ymaps.ready(init);

        function init () {
            // Создание экземпляра карты и его привязка к контейнеру с
            // заданным id ("map")
            var myMap = new ymaps.Map('map', {
                    // При инициализации карты, обязательно нужно указать
                    // ее центр и коэффициент масштабирования
                    center: [56.310073,43.998007], // Нижний Новгород
                    zoom: 14
                });
            myMap.behaviors.enable('scrollZoom');
            myMap.controls.add('zoomControl', {size: "small"});

			var geometry = [[56.308475,43.982986], [56.30795,43.987793], [56.310073,43.998007], [56.314963,44.012555]],

			properties = {
				hintContent: "Хинт",
				balloonContentHeader: "Балун контент хедер",
				balloonContent: "Балун контент",
				balloonContentBody: "Балун контент боди",
				balloonContentFooter: "Балун контент футер"
			},
			options = {
				draggable: true,
				hasBalloon: true,
				strokeColor: '#ff0000',
				strokeWidth: 5

			},
			polyline = new ymaps.Polyline(geometry, properties, options);

            // Определяем границы набора объектов
            bounds = new ymaps.GeoCollectionBounds(geometry[0]);
            // Применяем область показа к карте
//            myMap.setBounds(bounds);

			myMap.geoObjects.add(polyline);

        }
    </script>
</head>

<body>
<div id="map" style="width:800px; height:600px"></div>
</body>
</html>