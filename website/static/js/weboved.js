var updateIframe = function() {
    if(!window.location.search) return
    var location = window.location.search.split('=')[1].replace(/%3A/g, ':').replace(/%2F/g, '/');
    $('#text').val(location);
    var container = $('.standalone-container');
    container.empty();
    container.append(
        $('<iframe src="/api/loadurl?url=' + location +'" id="content-iframe" width="100%" height="600px" frameborder="0"></iframe>')
    )
};

$("body").ready(function(){
    updateIframe()
});
