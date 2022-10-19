let center = [48.8866527839977,2.34310679732974];

function init() {
	let map = new ymaps.Map('map-test', {
		center: center,
		zoom: 17
	});

	let placemark = new ymaps.Placemark([48.8875,2.3451], {
		balloonContentHeader: 'Трешка',
		balloonContentBody: 'Продается срочно',
		balloonContentFooter: 'Покупай быстрее',
	}, {
		iconLayout: 'default#image',
		iconImageHref: 'https://pics.freeicons.io/uploads/icons/png/5381700031595453756-512.png',
		iconImageSize: [40, 40],
		iconImageOffset: [-19, -44]
	});

	let placemark1 = new ymaps.Placemark(center, {
		balloonContent: `
			<div class="balloon">
				<div class="balloon__address">4x-комнатная квартира</div>
				<div>Ленинский проспект, дом 1</div>
                <div class="balloon__contacts">
					<a href="tel:+7999999999">+7999999999</a>
				</div>
			</div>
		`
	}, {
		iconLayout: 'default#image',
		iconImageHref: 'https://pics.freeicons.io/uploads/icons/png/5381700031595453756-512.png',
		iconImageSize: [40, 40],
		iconImageOffset: [-19, -44]
	});

	map.controls.remove('geolocationControl'); // удаляем геолокацию
  map.controls.remove('searchControl'); // удаляем поиск
  map.controls.remove('trafficControl'); // удаляем контроль трафика
  map.controls.remove('typeSelector'); // удаляем тип
  map.controls.remove('fullscreenControl'); // удаляем кнопку перехода в полноэкранный режим
  // map.controls.remove('zoomControl');  удаляем контрол зуммирования
  map.controls.remove('rulerControl'); // удаляем контрол правил
  // map.behaviors.disable(['scrollZoom']); // отключаем скролл карты (опционально)

	// map.geoObjects.add(placemark);
	map.geoObjects.add(placemark1);
    map.geoObjects.add(placemark)
	placemark1.balloon.open();
}

ymaps.ready(init);