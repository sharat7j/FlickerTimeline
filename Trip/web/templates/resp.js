/**
 * Created with IntelliJ IDEA.
 * User: root
 * Date: 7/16/13
 * Time: 3:30 PM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function() {

    //Stops the submit request
    $("#fileUploadAjax").submit(function(e){
        e.preventDefault();
    });

    //checks for the button click event
    $("#submitButton").click(function(e){

        //get the form data and then serialize that
        dataString = $("#myAjaxRequestForm").serialize();

        //get the form data using another method
        var countryCode = $("input#countryCode").val();
        dataString = "countryCode=" + countryCode;
        file=$("input#uploadFile").val();
        //make the AJAX request, dataType is set to json
        //meaning we are expecting JSON data in response from the server
        $.ajax({
            type: "POST",
            url: "UploadServlet",
            data: file,
            dataType: "file",

            //if received a response from the server
            success: function( data, textStatus, jqXHR) {
                //our country code was correct so we have some information to display
                if(data.success){
                    $("#ajaxResponse").html("");

                }
                //display error message
                else {
                    $("#ajaxResponse").html("<div><b>File in Invalid!</b></div>");
                }
            },

            //If there was no resonse from the server
            error: function(jqXHR, textStatus, errorThrown){
                console.log("Something really bad happened " + textStatus);
                $("#ajaxResponse").html(jqXHR.responseText);
            },

            //capture the request before it was sent to server
            beforeSend: function(jqXHR, settings){
                //adding some Dummy data to the request
                settings.data += "&dummyData=whatever";
                //disable the button until we get the response
                $('#myButton').attr("disabled", true);
            },

            //this is called after the response or error functions are finsihed
            //so that we can take some action
            complete: function(jqXHR, textStatus){
                //enable the button
                $('#myButton').attr("disabled", false);
            }

        });
    });

});
