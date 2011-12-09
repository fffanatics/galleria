/**
 * photo.js
 *
 * contains javascript for all photo related activity
 */

/** the previous photo url */
var g_prevUrl=null;

/** the next photos url */
var g_nextUrl=null;

/**
 * Binds the left and right arrow keys to advance to the prev and next photos
 */
$(window).keyup(function(event) {
	if(event.keyCode == "37") { // left arrow
		prevPhoto();
	} else if(event.keyCode == "39") { // right arrow
		nextPhoto();
	}
});

/**
 * Loads the previous photo in the album
 */
function prevPhoto() {
	if(g_prevUrl) {
		window.location=g_prevUrl;
	}
}

/**
 * Loads the next photo in the album
 */
function nextPhoto() {
	if(g_nextUrl) {
		window.location=g_nextUrl;
	}
}