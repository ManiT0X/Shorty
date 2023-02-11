$(document).ready(function() {
var csrftoken = $('meta[name=csrf-token]').attr('content')
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})

//=======================================================================
 // Make the AJAX request to retrieve the link and chart data
$(".linkinfo").click(function() {
  var idinput = $(this).attr('aria-label');
  var baseURL = window.location.origin;

  $.ajax({
    url: window.location.origin + "/user/get-data/" + idinput,
    type: "GET",
    cache: false,
    success: function(response) {
      var linkData = response[0];
      var visitorData = response[1];

      // Update the information on the page
      $("#fullLink").val(linkData[1]);
      $("#linkDate").text(linkData[2]);
      $("#visitsid").text(linkData[3]);
      $("#linkDescription").val(linkData[6]);
      $("#qrid").attr("src", baseURL + "/static/" + linkData[5]);
      $("#updateLinkButton").attr("customid", linkData[0]);
      $("#updateDescriptionButton").attr("customid", linkData[0]);
      $("#DeleteLink").attr("customid", linkData[7]);
      $("#qr_download_button").attr("href", baseURL + "/download/qr/" + linkData[7]);
      $("#qr_download_button").removeAttr("hidden");
      $("#dataChart").removeAttr("hidden");
      $("#dataChartCol").removeAttr("hidden");
      $("#dataSorting").attr('linkid', idinput)

      // Display the visitor chart
      if(window.myNewChart1 != null){
        window.myNewChart1.destroy();
      }

      const ctx = document.getElementById('visitChart');
      var dates = visitorData[0];
      var visits = visitorData[1];

      window.myNewChart1 = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: dates,
          datasets: [{
            label: 'Visitors',
            data: visits,
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });

      // Display the data chart
      if(window.myNewChart2 != null){
        window.myNewChart2.destroy();
      }

      const ctx2 = document.getElementById('dataChart');
      var os = visitorData[2];
      var os_visits = visitorData[3];
       var colors = visitorData[4];

      window.myNewChart2 = new Chart(ctx2, {
        type: 'doughnut',
        data: {
          labels: os,
          datasets: [{
            label: 'visitors',
            data: os_visits,
            backgroundColor: colors ,
            hoverOffset: 4
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
      // Add a change event listener to the select box
    $('#dataSorting').on('change', function() {
    var option = $(this).val();
    var dataID = $('#dataSorting').attr('linkid');

    $.ajax({
    url: window.location.origin + "/user/get-data/" + dataID,
    type: "GET",
    cache: false,
    success: function(response) {
      var visitorData = response[1];

      if (option == "0"){
        window.myNewChart2.data.labels = visitorData[2];
        window.myNewChart2.data.datasets[0].data = visitorData[3];
        window.myNewChart2.data.datasets[0].backgroundColor = visitorData[4];
        window.myNewChart2.update();
      }
      else if (option == "1"){
        window.myNewChart2.data.labels = visitorData[8];
        window.myNewChart2.data.datasets[0].data = visitorData[9];
        window.myNewChart2.data.datasets[0].backgroundColor = visitorData[10];
        window.myNewChart2.update();
      }
      else if (option == "2"){
        window.myNewChart2.data.labels = visitorData[5];
        window.myNewChart2.data.datasets[0].data = visitorData[6];
        window.myNewChart2.data.datasets[0].backgroundColor = visitorData[7];
        window.myNewChart2.update();
      }
      else if (option == "3"){
        window.myNewChart2.data.labels = visitorData[11];
        window.myNewChart2.data.datasets[0].data = visitorData[12];
        window.myNewChart2.data.datasets[0].backgroundColor = visitorData[13];
        window.myNewChart2.update();
      }
      }
    });

  });
  },
  error: function(xhr, status, error) {
    console.error("An error occurred while retrieving data:", error);
    alert("An error occurred while retrieving data. Please try again later.");
  }
});
});
//=======================================================================


//=======================================================================
//this is the function for Deleting Link from database
$("#DeleteLink").click(function() {
    var short_link_id = $(this).attr("customid");
  $.ajax({
    url: window.location.origin + "/user/delete/"+short_link_id,
    type: "POST",
    success: function(response) {
      latestData = response;
      location.reload()
    }
    });
});
//=======================================================================


//=======================================================================
//this is the function for Shorting Link from the HOMEPAGE
$("#homepage_short_button").click(function() {
    var url = $("#url_input").val();
    if (!url.match(/^(http[s]?:\/\/)?.+\..+/gi)) { alert("url not valid"); return 0; }
  req = $.ajax({
    url: window.location.origin,
    type: "POST",
    data: {long_url:url},
    success: function(response) {
      latestData = response;
    }
    });

    req.done(function(data) {
    $("#qr_img").attr("src", window.location.origin + "/static/" +data['qr_image']);
    $("#qr_download_button").attr("href", window.location.origin + "/download/qr/" +data['shortlink']);
    $("#qr_download_button").removeAttr("hidden");
    $("#generate_link").remove();
    $("#short_url").val(window.location.origin +"/"+ data['shortlink']);
    $("#copy_link").removeAttr("hidden");

  });
});
//=======================================================================


//=======================================================================
//this is the function for Updating LINK from the PROFILE
$("#updateLinkButton").click(function() {
    var url = $("#fullLink").val();
    var id = $(this).attr('customid');
    if (!url.match(/^(http[s]?:\/\/)?.+\..+/gi)) { alert("url not valid"); return 0; }
    req = $.ajax({
    url: window.location.origin + "/user/update/link",
    type: "POST",
    data: {id:id,updatedLink:url},
    success: function(response) {
    $("#qrid").attr("src", window.location.origin + "/static/" +response['qr_image']);
    setTimeout(function() {
    location.reload()
    }, 1000); // wait for 1 second (i have a slow computer, without that second , the page refresh before fetching the data)
    }
    });

});
//=======================================================================


//=======================================================================
//this is the function for Updating LINK DESCRIPTION from the PROFILE
$("#updateDescriptionButton").click(function() {
    var description = $("#linkDescription").val();
    var id = $(this).attr('customid');
  req = $.ajax({
    url: window.location.origin + "/user/update/description",
    type: "POST",
    data: {id:id, description:description},
    success: function(response) {
     $('#linkDescription').text(response.description);
    location.reload(true);
    }
    });

});
//=======================================================================


//=======================================================================
//this is to short links from PROFILE
$("#profile_short_button").click(function() {
    var url = $("#profile_url_input").val();
    var description = $("#profile_link_description").val();
    if (!url.match(/^(http[s]?:\/\/)?.+\..+/gi)) { alert("url not valid"); return 0; }
  req = $.ajax({
    url: window.location.origin + "/user/",
    type: "POST",
    data: {full_link:url, link_description:description},
    success: function(response) {
      location.reload(true);
    }
    });


});
//=======================================================================


});



