var appName = "Tux Drive";
var appDescn = "Console App to interact with Google Drive";

var repoName = "prahladyeri/tuxdrive";

function showBackdrop(done) {
	//$('<div class="modal-backdrop fade-in"></div>').appendTo(document.body);
	//$('.modal').modal({show:true});
	console.log('showbd');
	$('.modal').on('shown.bs.modal', function(){
		console.log('shown');
		done();
	});
	$('.modal').modal('show');
}

function hideBackdrop(){
	//$(".modal-backdrop").remove();
	console.log('hidebd');
	$('.modal').modal({show:false});
	$('.modal').modal('hide');
}

function getAllReleases(done) {
	console.log('here');
	$.getJSON("https://api.github.com/repos/" + repoName + "/releases")
	.done(function(releases){
		//console.log('returns');
		//console.log(releases);
		
		//first one will be the latest
		for(var i=0;i<releases.length;i++) {
			console.log(releases[i]['name'], releases[i]['tag_name'], releases[i]['body']);
			//$div = $("<div class='relese'></div>");
			$div = $(".template").clone().removeClass('template d-none');
			$div.find('.card-title').text("Version " + releases[i]['tag_name'] + " of " + appName + " has been Released.");
			$div.find('.btn-binary').attr('href', releases[i].assets[0].browser_download_url);
			$div.find('.btn-src').attr('href', releases[i].tarball_url);
			if (i==0) {
				$div.find('.card-header').text("Latest Release");
				$div.find('.card-header').addClass("font-weight-bold");
				$div.find('.btn-binary').attr('name','btnLatest');
			}
			
			//$div.append("<span class='info'>");
			//$div.find('.info').text("Version " + releases[i]['tag_name'] + " of " + appName + " has been Released!");
			//$div.append("<br><a class='btn btn-sm btn-primary' href='" + releases[i].assets[0].browser_download_url + "'>Download Binary</a><br>");
			
			$('.releases').append($div);
		}
		
		done();
	})
	;
}

//https://stackoverflow.com/questions/24987542/is-there-a-link-to-github-for-downloading-a-file-in-the-latest-release-of-a-repo
function getLatestDownloadURL(func) {
	console.log('getting latest url');
	$.getJSON("https://api.github.com/repos/" + repoName + "/releases/latest").done(function (release) {
		//console.log('success',release);
		var asset = release.assets[0];
		//return asset.browser_download_url;
		func(asset.browser_download_url);
		//~ var downloadCount = 0;
		//~ for (var i = 0; i < release.assets.length; i++) {
			//~ downloadCount += release.assets[i].download_count;
		//~ }
		//~ var oneHour = 60 * 60 * 1000;
		//~ var oneDay = 24 * oneHour;
		//~ var dateDiff = new Date() - new Date(asset.updated_at);
		//~ var timeAgo;
		//~ if (dateDiff < oneDay)
		//~ {
			//~ timeAgo = (dateDiff / oneHour).toFixed(1) + " hours ago";
		//~ }
		//~ else
		//~ {
			//~ timeAgo = (dateDiff / oneDay).toFixed(1) + " days ago";
		//~ }
		//~ var releaseInfo = release.name + " was updated " + timeAgo + " and downloaded " + downloadCount.toLocaleString() + " times.";
		//~ $(".btn-download").attr("href", asset.browser_download_url);
		//~ $(".release-info").text(releaseInfo);
		//~ $(".release-info").fadeIn("slow");
	});
}
