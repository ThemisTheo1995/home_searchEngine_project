document.addEventListener("DOMContentLoaded", function() {
    var secondarySlider = new Splide('#secondary-slider', {
        direction   : 'ttb',
        type        : 'loop',
        perPage     : 2,
        perMove     : 1,
        heightRatio : 1.11,
        gap         : 10,
        cover       : true,
        lazyLoad    : 'nearby',
        isNavigation: true,
        arrows      : false,
        focus       : '',
        breakpoints : {
            '1023': {
                heightRatio: 0.2,
                direction : 'ltr',
                pagination: false,
                perPage     : 3,
                perMove     : 1,
            }
        },
        }).mount();

    var primarySlider = new Splide('#image-slider', {
        type        : 'loop',
        cover       : true ,
        direction : 'ltr',
        heightRatio : 0.55,
        rewind      : true,
	    focus    : 'center',
        lazyLoad    : 'nearby',
        pagination  : false,
        breakpoints : {
            '1023'  : {
                heightRatio: 0.65,
                pagination: true,
            }
        },
    });

    primarySlider.sync(secondarySlider).mount();
});