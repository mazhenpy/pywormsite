(function($){
	// Settings
	var repeat = localStorage.repeat || 0,
		shuffle = localStorage.shuffle || 'false',
		continous = true,
		autoplay = false,
		playlist = [
            {
title: '创世',
artist: 'WOW',
album: 'The Shaping of The World.mp3',
cover: '/static/music/img/The Shaping of The World.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/The%20Shaping%20of%20The%20World.mp3',
ogg: ''
},
		{
title: '愿艾露恩与你同在',
artist: '灰谷',
album: 'Song of Elune.mp3',
cover:'/static/music/img/elune.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/Song%20of%20elune.mp3',
ogg: ''
},
{
title: '夜歌森林的轻语',
artist: '海加尔山',
album: 'Night song.mp3',
cover: '/static/music/img/nightsong.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/Nightsong.mp3%20',
ogg: ''
},

{
title: '上层精灵的挽歌',
artist: '幽暗城',
album: 'Lament of the Highbourne.mp3',
cover: '/static/music/img/Lament of the Highbourne .jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/Lament%20of%20the%20Highbourne.mp3',
ogg: ''
},
{
title: '战争时节',
artist: 'WOW',
album: 'Seasons of War.mp3',
cover: '/static/music/img/Seasons of War.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/Seasons%20of%20War.mp3',
ogg: ''
},
{
title: '暴风城',
artist: '暴风城',
album: 'Stormwind.mp3',
cover: '/static/music/img/Stormwind.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/Stormwind.mp3',
ogg: ''
},
{
title: '战争的召唤',
artist: 'WOW',
album: 'A Call to Arms.mp3',
cover: '/static/music/img/A Call to Arms.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/A%20Call%20to%20Arms.mp3',
ogg: ''
},
{
title: '德国装甲是第一进行曲',
artist: 'Era',
album: 'The mass.mp3',
cover: '/static/music/img/The mass.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/The%20Mass.mp3',
ogg: ''
},
{
title: '亡灵序曲',
artist: 'Roger',
album: 'The down.mp3',
cover: '/static/music/img/The Down.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/The%20Dawn.mp3',
ogg: ''
},
{
title: '酒馆',
artist: '酒馆',
album: 'Tavern.mp3',
cover: '/static/music/img/tavern.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/Tavern.mp3',
ogg: ''
},
{
title: '泰达希尔',
artist: '泰达希尔',
album: 'Teldrassil.mp3',
cover: '/static/music/img/teldrassil.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/Teldrassil.mp3',
ogg: ''
},
{
title: '雷霆崖',
artist: '雷霆崖',
album: 'Thunder Bluff.mp3',
cover: '/static/music/img/leitingya2.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/Thunder%20Bluff.mp3',
ogg: ''
},
{
title: '巫妖王的陨落',
artist: 'Arthas, My Son',
album: 'Arthas, My Son.mp3',
cover: '/static/music/img/Arthas, My Son.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/Arthas%2C%20My%20Son.mp3',
ogg: ''
},
{
title: '艾尔文森林',
artist: '艾尔文森林',
album: 'Elwynn Forest.mp3',
cover: '/static/music/img/Elwynn Forest.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/Elwynn%20Forest(Ambient).mp3',
ogg: ''
},
{
title: '燃烧平原',
artist: '燃烧平原',
album: 'Burning Steppes.mp3',
cover: '/static/music/img/Burning Steppes.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/Burning%20Steppes.mp3',
ogg: ''
},
{
title: '荆棘谷',
artist: '荆棘谷',
album: 'Stranglethorn Vale.mp3',
cover: '/static/music/img/Stranglethorn Vale.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/Stranglethorn%20Vale.mp3',
ogg: ''
},
{
title: '达纳苏斯',
artist: '达纳苏斯',
album: 'Darnassus.mp3',
cover: '/static/music/img/Darnassus.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/Darnassus.mp3',
ogg: ''
},
{
title: '银月城',
artist: '银月城',
album: 'Silvermoon City.mp3',
cover: '/static/music/img/Silvermoon City.jpg',
mp3: 'http://7xpc8i.com1.z0.glb.clouddn.com/Silvermoon%20City.mp3',
ogg: ''
},


        ];

	// Load playlist
	for (var i=0; i<playlist.length; i++){
		var item = playlist[i];
		$('#playlist').append('<li>'+item.artist+' - '+item.title+'</li>');
	}

	var time = new Date(),
		currentTrack = shuffle === 'true' ? time.getTime() % playlist.length : 0,
		trigger = false,
		audio, timeout, isPlaying, playCounts;

	var play = function(){
		audio.play();
		$('.playback').addClass('playing');
		timeout = setInterval(updateProgress, 500);
		isPlaying = true;
	};

	var pause = function(){
		audio.pause();
		$('.playback').removeClass('playing');
		clearInterval(updateProgress);
		isPlaying = false;
	};

	// Update progress
	var setProgress = function(value){
		var currentSec = parseInt(value%60) < 10 ? '0' + parseInt(value%60) : parseInt(value%60),
			ratio = value / audio.duration * 100;

		$('.timer').html(parseInt(value/60)+':'+currentSec);
		$('.progress .pace').css('width', ratio + '%');
		$('.progress .slider a').css('left', ratio + '%');
	};

	var updateProgress = function(){
		setProgress(audio.currentTime);
	};

	// Progress slider
	$('.progress .slider').slider({step: 0.1, slide: function(event, ui){
		$(this).addClass('enable');
		setProgress(audio.duration * ui.value / 100);
		clearInterval(timeout);
	}, stop: function(event, ui){
		audio.currentTime = audio.duration * ui.value / 100;
		$(this).removeClass('enable');
		timeout = setInterval(updateProgress, 500);
	}});

	// Volume slider
	var setVolume = function(value){
		audio.volume = localStorage.volume = value;
		$('.volume .pace').css('width', value * 100 + '%');
		$('.volume .slider a').css('left', value * 100 + '%');
	};

	var volume = localStorage.volume || 0.5;
	$('.volume .slider').slider({max: 1, min: 0, step: 0.01, value: volume, slide: function(event, ui){
		setVolume(ui.value);
		$(this).addClass('enable');
		$('.mute').removeClass('enable');
	}, stop: function(){
		$(this).removeClass('enable');
	}}).children('.pace').css('width', volume * 100 + '%');

	$('.mute').click(function(){
		if ($(this).hasClass('enable')){
			setVolume($(this).data('volume'));
			$(this).removeClass('enable');
		} else {
			$(this).data('volume', audio.volume).addClass('enable');
			setVolume(0);
		}
	});

	// Switch track
	var switchTrack = function(i){
		if (i < 0){
			track = currentTrack = playlist.length - 1;
		} else if (i >= playlist.length){
			track = currentTrack = 0;
		} else {
			track = i;
		}

		$('audio').remove();
		loadMusic(track);
		if (isPlaying == true) play();
	};

	// Shuffle
	var shufflePlay = function(){
		var time = new Date(),
			lastTrack = currentTrack;
		currentTrack = time.getTime() % playlist.length;
		if (lastTrack == currentTrack) ++currentTrack;
		switchTrack(currentTrack);
	};

	// Fire when track ended
	var ended = function(){
		pause();
		audio.currentTime = 0;
		playCounts++;
		if (continous == true) isPlaying = true;
		if (repeat == 1){
			play();
		} else {
			if (shuffle === 'true'){
				shufflePlay();
			} else {
				if (repeat == 2){
					switchTrack(++currentTrack);
				} else {
					if (currentTrack < playlist.length) switchTrack(++currentTrack);
				}
			}
		}
	};

	var beforeLoad = function(){
		var endVal = this.seekable && this.seekable.length ? this.seekable.end(0) : 0;
		$('.progress .loaded').css('width', (100 / (this.duration || 1) * endVal) +'%');
	};

	// Fire when track loaded completely
	var afterLoad = function(){
		if (autoplay == true) play();
	};

	// Load track
	var loadMusic = function(i){
		var item = playlist[i],
			newaudio = $('<audio>').html('<source src="'+item.mp3+'"><source src="'+item.ogg+'">').appendTo('#player');
		
		$('.cover').html('<img src="'+item.cover+'" alt="'+item.album+'">');
		$('.tag').html('<strong>'+item.title+'</strong><span class="artist">'+item.artist+'</span><span class="album">'+item.album+'</span>');
		$('#playlist li').removeClass('playing').eq(i).addClass('playing');
		audio = newaudio[0];
		audio.volume = $('.mute').hasClass('enable') ? 0 : volume;
		audio.addEventListener('progress', beforeLoad, false);
		audio.addEventListener('durationchange', beforeLoad, false);
		audio.addEventListener('canplay', afterLoad, false);
		audio.addEventListener('ended', ended, false);
	};

	loadMusic(currentTrack);
	$('.playback').on('click', function(){
		if ($(this).hasClass('playing')){
			pause();
		} else {
			play();
		}
	});
	$('.rewind').on('click', function(){
		if (shuffle === 'true'){
			shufflePlay();
		} else {
			switchTrack(--currentTrack);
		}
	});
	$('.fastforward').on('click', function(){
		if (shuffle === 'true'){
			shufflePlay();
		} else {
			switchTrack(++currentTrack);
		}
	});
	$('#playlist li').each(function(i){
		var _i = i;
		$(this).on('click', function(){
			switchTrack(_i);
		});
	});

	if (shuffle === 'true') $('.shuffle').addClass('enable');
	if (repeat == 1){
		$('.repeat').addClass('once');
	} else if (repeat == 2){
		$('.repeat').addClass('all');
	}

	$('.repeat').on('click', function(){
		if ($(this).hasClass('once')){
			repeat = localStorage.repeat = 2;
			$(this).removeClass('once').addClass('all');
		} else if ($(this).hasClass('all')){
			repeat = localStorage.repeat = 0;
			$(this).removeClass('all');
		} else {
			repeat = localStorage.repeat = 1;
			$(this).addClass('once');
		}
	});

	$('.shuffle').on('click', function(){
		if ($(this).hasClass('enable')){
			shuffle = localStorage.shuffle = 'false';
			$(this).removeClass('enable');
		} else {
			shuffle = localStorage.shuffle = 'true';
			$(this).addClass('enable');
		}
	});
})(jQuery);