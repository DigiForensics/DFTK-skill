# Frida recipes for APK observation

Starter hooks for *observing* an authorized app's runtime behavior. Use to
confirm static hypotheses, not to defeat controls you are not authorized to
alter. Always run on an authorized device / isolated emulator.

## List processes & spawn

```bash
frida-ps -U                       # USB device process list
frida-ps -Ua                      # include apps
frida -U -f com.example.app -l hook.js   # spawn + inject
```

## Hook a Java method (print args/return)

```javascript
// hook.js
Java.perform(function () {
  var Login = Java.use("com.example.app.LoginActivity");
  Login.verifyPassword.implementation = function (user, pwd) {
    console.log("[*] verifyPassword called user=" + user + " pwd=" + pwd);
    var ret = this.verifyPassword(user, pwd);
    console.log("[*] verifyPassword returned=" + ret);
    return ret;
  };
});
```

## Trace certificate / SSL calls

```bash
frida-trace -U -f com.example.app -j '*!*certificate*'
frida-trace -U -f com.example.app -j 'java.security.*!*'
```

## Hook a native export

```javascript
var mod = Process.getModuleByName("libnative.so");
var addr = mod.getExportByName("Java_com_example_app_sign");
Interceptor.attach(addr, {
  onEnter: function (args) {
    console.log("[*] sign() called, arg0=" + args[0]);
  },
  onLeave: function (retval) {
    console.log("[*] sign() returned=" + retval);
  }
});
```

## Observe crypto

```javascript
Java.perform(function () {
  var Md = Java.use("java.security.MessageDigest");
  Md.digest.overload("[B").implementation = function (data) {
    console.log("[*] MessageDigest.digest input=" + bytesToHex(data));
    return this.digest(data);
  };
});
```

## Notes

- Print first, modify later. Never silently alter return values on apps you do
  not own or are not authorized to assess.
- Record each hook target + observed value in the audit ledger.
- For deeper native control flow, divert to `ida-reverse` / `radare2`.
