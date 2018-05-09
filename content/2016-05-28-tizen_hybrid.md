title: Tizen Hybrid App Tutorial
date: 2016-05-28
category: web
slug: tizen_hybrid

> 너무 오래 전에 작성한 포스트라 제대로 동작할지에 대한 확신은 없습니다.

A hybrid app is an application that runs on the device like native apps and is written with web technologies (HTML5, CSS and JavaScript).

### Pros

- Easy to support multiple mobile devices and platforms
  - Reusable UI Codes
- Web UI and Native Services
  - Data processing in background
  - Broader access to device hardware with native services
- Rapid development using open-source native/web libraries

### Cons

- Additional effort for communicating between native and web

In Tizen version 2.3, there are three ways for implementing hybrid apps (if there are more, let me know).

- Message Port (Built-in)
- WebSocket
- Bridge Server

## Implementing Hybrid App with Message Port

### Step 1. Creating Projects

- Create Tizen Web Application
  - New Project > Tizen > Tizen Web Project > Template > jQuery Mobile > Single Page Application
- Create Tizen Native Service Application
  - New Project > Tizen > Tizen Native Project > Template > Service Application

### Step 2. Setting Privileges

- Add Web App Privileges (Web App > Package > tizen-manifest.xml > Privileges > Add)
  - http://tizen.org/privilege/application.info
  - http://tizen.org/privilege/application.launch
- Add Native Service App Privileges (Native Service App > Package > config.xml > Privileges > Add)
  - http://tizen.org/privilege/packagemanager.info

### Step 3. Packaging

- Refer the Native Service App in the Web App
  - Web App Root (Right Click) > Properties > Project References
  - Check the Native Service App
- Build the Web App
  - Check the Native App ID
    - Web App > {Your Web App Name}.wgt > tizen-manifest.xml

### Step 4. Implementing Web App

- Open Web App > js > main.js
- Add the following lines at the end
 
```javascript
$(document).ready(function () {
    $("#bt_send").click(function () {
        var a = tizen.application.getAppInfo(nativeServiceAppId);

        //To open an message port to invoke message port 
        var remoteMessagePort = tizen.messageport.requestRemoteMessagePort(
            nativeServiceAppId, "RECEIVE_NAME");
        //To send a message
        remoteMessagePort.sendMessage([ {
            key: 'name',
            value: "Web"
        } ], null);
    });
});
```

- Add the following lines after the line, `console.log(“init() called”);`

```javascript
// Launch context transmitter service
tizen.application.launch(nativeServiceAppId, function () {
    console.log('success');
}, function (err) {
    console.log(err.message);
});

// Open message port
localMessagePort = tizen.messageport.requestLocalMessagePort("RECEIVE_HELLO_MESSAGE");
localMessagePort.addMessagePortListener(function (data, replyPort) {
    console.log("Message Received. " + data[0].value);
});

// Register click listener
$("#bt_send").click(function () {
    var a = tizen.application.getAppInfo(nativeServiceAppId);

    //To open an message port to invoke message port 
    var remoteMessagePort = tizen.messageport.requestRemoteMessagePort(
        nativeServiceAppId, "RECEIVE_NAME");
    //To send a message
    remoteMessagePort.sendMessage([ {
        key: 'name',
        value: "Web"
    } ], null);
});
```

### Step 5. Implementing Native Service App

- Open Native App > `service.c` (Your file name may differ.)
- Import `message_port.h`

```c
#include "message_port.h"
```

- Add the two functions
 
```c
void send_message(const char * remote_app_id, const char *name) {
    bundle *b = bundle_create();
    char hello_message[20] = "Hello ";
    strcat(hello_message, name);
    bundle_add_str(b, "helloMessage", hello_message);
     
    //To send a message through a specific message port
    message_port_send_message(remote_app_id, "RECEIVE_HELLO_MESSAGE", b);
    bundle_free(b);
}
     
void message_port_cb(int local_port_id, const char *remote_app_id,
    const char *remote_port, bool trusted_remote_port, bundle *message) {
    char *name = NULL;
    bundle_get_str(message, "name", &name);
     
    //To print received message
    dlog_print(DLOG_INFO, "RECEIVE_NAME_CALLBACK", "Message from %s, name: %s ",
    remote_app_id, name);
     
    //To send a message through a specific message port
    send_message(remote_app_id, name);
}
```

- Add the following lines to `service_app_create()` function

```c
bool service_app_create(void *data) {
    // Todo: add your code here.
 
    dlog_print(DLOG_INFO, "NativeService", "Created.");
 
    int local_port_id = message_port_register_local_port("RECEIVE_NAME", message_port_cb, NULL);
    if (local_port_id < 0) {
        dlog_print(DLOG_ERROR, "NativeService", "Port register error : %d", local_port_id);
    } else {
        dlog_print(DLOG_INFO, "NativeService", "port_id : %d", local_port_id);
    }
 
    return true;
}
```

### Step 6. Build and Run

- Build the Web App
- Run the Web App (in Debugging Mode)
- Click the 'Send Message' Button
- Check the Console

```
js/main.js (21) :init() called
js/main.js (25) :success
js/main.js (33) :Message Received. Hello Web
```
