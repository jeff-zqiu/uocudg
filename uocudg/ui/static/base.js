$(document).ready(function() {
  $(".card-body").click(function() {
    post_url = ["/forum/", $(this).attr('id'), "/"];
    $("#content-overlay").load(post_url.join(''))
  });
});
