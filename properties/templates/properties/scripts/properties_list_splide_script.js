document.addEventListener("DOMContentLoaded", function() {
    /*
    * Splide module
    */
    var spliders = document.querySelectorAll('.splide');
    if (spliders){
        for(var i = 0; i < spliders.length; i++){
            var primarySlider = new Splide(spliders[i], {
                type        : 'loop',
                cover       : true,
                perPage     : spliders[i].dataset.pages,
                perMove     : 1,
                heightRatio : spliders[i].dataset.ratio,
                gap         : '0.2rem',
                rewind      : true,
                lazyLoad    : 'nearby',
                pagination  : true,
                keyboard: "focused",
                breakpoints : {
                    '1024'  : {
                        heightRatio : 0.30,
                        perPage     : 2,
                        perMove     : 1,
                    },
                    '640'  : {
                        heightRatio : 0.60,
                        perPage     : 1,
                        perMove     : 1,
                    },
                },
            }).mount();
        }
    }
});