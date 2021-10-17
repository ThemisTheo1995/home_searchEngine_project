document.addEventListener("DOMContentLoaded", function() {
    var secondarySlider = new Splide('#secondary-slider', {
        direction   : 'ttb',
        perPage     : 2,
        heightRatio : 1.11,
        gap         : 10,
        cover       : true,
        lazyLoad    : 'nearby',
        isNavigation: true,
        arrows      : false,
        focus       : '',
        breakpoints : {
            '1023': {
                fixedWidth: 1,
                height    : 1,
                direction : 'ltr',
                pagination: false,
            }
        },
        }).mount();

    var primarySlider = new Splide('#image-slider', {
        type        : 'loop',
        cover       : true ,
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