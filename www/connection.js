(function(){
    var wsProto='ws';
    if(location.protocol == 'https:'){
        wsProto='wss';
    }
    window.socket = new WebSocket(wsProto+'://'+location.host+'/ws');
    var socket = window.socket;
    socket.onopen = function(){
        console.log('connected');
    };
})();