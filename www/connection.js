(function(){
    window.socket = new WebSocket('ws://'+location.host+'/ws');
    var socket = window.socket;
    socket.onopen = function(){
        console.log('connected');
    };
})();