function addProductReview(e){
	e.preventDefault();
	var review_form = jQuery(e.target);
	jQuery.ajax({
		url: review_form.attr('action'),
		type: review_form.attr('method'),
		data: review_form.serialize(),
		dataType: 'json',
		success: function(response){
			if(response.success == "True"){
				// disable the submit button to prevent duplicates
				jQuery("#submit_review").attr('disabled','disabled');
				// if this is first review, get rid of "no reviews" text
				jQuery("#no_reviews").empty();
				// add the new review to the reviews section
				jQuery("#reviews").prepend(response.html).slideDown();
				// get the newly added review and style it with color
				new_review = jQuery("#reviews").children(":first");
				new_review.addClass('new_review');
				// hide the review form
				jQuery("#review_form").slideToggle();
			}
			else{
				// add the error text to the review_errors div
				jQuery("#review_errors").append(response.html);
			}
		},
		error: function(xhr, ajaxOptions, thrownError){
			// log ajax errors?
		}
	});
}

//toggles visibility of "write review" link
//and the review form.
function slideToggleReviewForm(){
	jQuery("#review_form").slideToggle();
	jQuery("#add_review").slideToggle();
}

function statusBox(){
	jQuery('<div id="loading">Loading...</div>')
	.prependTo("#main")
	.ajaxStart(function(){jQuery(this).show();})
	.ajaxStop(function(){jQuery(this).hide();})
	}

function prepareDocument(){
	jQuery("form#search").submit(function(){
		text = jQuery("#id_q").val();
		if (text == "" || text == "Search"){
			// if empty, pop up alert
			alert("Enter a search term.");
			// halt submission of form
			return false;
		}
	});
	jQuery("form#review").submit(function(e){
		addProductReview(e);
	});
	jQuery("#review_form").addClass('hidden');
	jQuery("#add_review").click(slideToggleReviewForm);
	jQuery("#add_review").addClass('visible');
	jQuery("#cancel_review").click(slideToggleReviewForm);
	statusBox();
}
jQuery(document).ready(prepareDocument);
