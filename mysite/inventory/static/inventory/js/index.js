/**
 * Created by Erick on 2/25/2017.
 */
$( document ).ready(function(){
	$(".button-collapse").sideNav();
});

// lightGallery init
$('#aniimated-thumbnials').lightGallery({
    thumbnail:true,
    animateThumb: false,
    showThumbByDefault: false
});

/* JavaScript Media Queries */
if (matchMedia) {
	var mq = window.matchMedia("(min-width: 1600px)");
	mq.addListener(WidthChange);
	WidthChange(mq);
}

// media query change
function WidthChange(mq) {
	var cardCols = document.getElementsByClassName('cardCol');

	if (mq.matches) {
        // Adds l2 class from materilize and removes l3
        for(var i=0; i < cardCols.length; i++){
            cardCols[i].classList.remove("l3");
            cardCols[i].className += " l2";
        }
	} else {
        // Adds l2 class from materilize and removes l3
        for(var i=0; i < cardCols.length; i++){
            cardCols[i].classList.remove("l2");
            cardCols[i].className += " l3";
        }
	}
}