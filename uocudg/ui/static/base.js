$(document).ready(function() {

  $('*').click(function(e) {
    target = e.target;
    if (!$(target).parents().is(".content-card") &&
      !$(target).is(".content-card") &&
      $("#content-overlay").html()) {
      $('#content-overlay').html('');
    }
  });

  $(".card-body-ajax").click(function() {
    post_url = ["/forum/", $(this).attr('id'), "/"];
    $("#content-overlay").load(post_url.join(''));
  });

  $(".new-post-ajax").click(function() {
    $("#content-overlay").load("/forum/edit/");
  });

  $(".clickup-button-ajax").click(function(e) {
    e.preventDefault();
    post_id = $(this).attr('id');
    click_url=["/forum/", post_id, "/clickup/"].join('');
    selector = ['#',post_id,'.clickup-button-ajax'].join('');
    $.ajax({
      url: click_url,
      success: function(data) {
        string = ['Click ', data['clicks']].join('');
        $(selector).html(string);
        if (data['clicked']) {
          $(selector).css('color', 'red');
        } else {
          $(selector).css('color', 'blue');
        }
      },
      error: function(xhr, ajaxOptions, thrownError) {
        alert(xhr.status);
        alert(thrownError);
      },
    })
  });

});
