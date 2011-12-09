/**
 * exif.js
 * 
 * processes the exif data on the page, formats it, and displays it
 */

/** the timer that is started once the photo is ready */
var g_timer = null;

/** the id of the photo that has been laoded */
var g_photoId = null;

/** the location of the exif <div> that we're loading data in to */
var g_locationId = null;

Object.prototype.size = function () {
	var len = this.length ? --this.length : -1;
	for (var k in this)
		len++;
	return len;
}

/**
 * this loads the exif data for a particular photo and displays it.
 * it does this by constantly polling the image until its exif data
 * is ready to be displayed
 * 
 * @param string photoId the id of the photo
 * @param string locationId the location where to display the data
 */
function loadExif(photoId, locationId) {
	g_photoId=photoId;
	g_locationId=locationId;
	
	$("#"+photoId).ready(function() {
		g_timer = setInterval(getExifData, 100);
	});
}

/**
 * this attempts to get the exif data from the photo. if it successfully
 * gets the data, then it clears the interval timer and displays the exif data
 */
function getExifData() {
	var exif=null;
	try {
		var exif = $("#"+g_photoId).exifAll();
		exif=exif[0];
	} catch (e) {
		exif=null;
	}
	
	if(exif != null && exif.size() > 0) {
		clearInterval(g_timer);
		g_timer = null;
		createExifDisplay(exif);
	}
}

/**
 * this actually displays the exif data
 * @param object exif the exif data for the image
 */
function createExifDisplay(exif) {
	console.log(exif);
	
	var exifStr="";
	for (var prop in exif) {
		if (exif.hasOwnProperty(prop) && prop != "UserComment" && prop != "size") {
			var propInfo = getExifPropClean(prop, exif[prop]);
			if(propInfo.name != null) {
				exifStr += propInfo.name + ": " + "<em>" + propInfo.desc + "</em><br>";
			}
		}
	}
	
	$("#"+g_locationId).html(exifStr); 
}

/**
 * maps a list of supported proper named exif properties to their real exif name
 * @param string prop the real exif name from the exif metadata
 * @param string value the value of the exif property
 * @returns object "cleansed" exif information
 */
function getExifPropClean(prop, value) {
	var cleansed=new Object();
	cleansed.name=null;
	cleansed.desc=null;
	switch(prop) {
		case "Make": 
			cleansed.name="Camera";
			cleansed.desc=value;
		break;
		case "Model": 
			cleansed.name=prop; 
			cleansed.desc=value;
		break;
		case "Flash": 
			cleansed.name="Flash Used"; 
			cleansed.desc=value;
		break;
		case "ApertureValue":
			cleansed.name="Aperture";
			cleansed.desc=Math.round(value*100)/100;
		break;
		case "ISOSpeedRatings":
			cleansed.name="ISO";
			cleansed.desc=value;
		break;
		case "FocalLength":
			cleansed.name="Focal Length";
			cleansed.desc=value + "mm";
		break;
		case "ExposureTime":
			cleansed.name="Exposure";
			cleansed.desc=value;
		break;
		case "DateTimeOriginal":
			cleansed.name="Date Taken";
			var date = new Date(value.substring(0,10).replace(/:/g, "/"));
			cleansed.desc=date.toLocaleDateString();
		break;
		case "FNumber":
			cleansed.name="F-Stop";
			cleansed.desc="f/"+value;
		break;
	}
	return cleansed;
}
