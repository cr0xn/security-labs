# Lab_1: Reflected XSS into HTML Context with Nothing Encoded

## Lab Overview

This lab contains a Reflected Cross-Site Scripting (XSS) vulnerability in the search functionality.

Type: Reflected XSS
Context: HTML Body Context
Source: URL parameter (search)
Sink: Server-generated HTML response

This vulnerability occurs because user input is inserted directly into the HTML without applying any output encoding.


## 1– Initial Analysis – Discovering the Attack Surface

When the lab is opened, a standard blog interface is displayed.
My first objective is to understand how the application processes user input.
When I type test into the search box and perform a search, the URL changes to:

```
https://<lab-id>.web-security-academy.net/?search=test
```

This indicates that the search functionality uses a GET parameter.

```
HTTP Request
GET /?search=test HTTP/1.1
Host: <lab-id>.web-security-academy.net
```

At this point, my goal is to observe how the entered value is handled in the server response.

## 2– Vulnerability Detection – Reflection Analysis

When inspecting the page source, the following structure is observed:

```
<h1>0 search results for 'test'</h1>
```

The value I entered is not passed through any sanitization process, Has no HTML entity encoding applied, Is directly embedded into the HTML content

## 3– Context Analysis

The actual template structure is as follows:

```
<h1>0 search results for 'USER_INPUT'</h1>
```

Important observations:

The input is inside an `<h1>` tag
It is not inside an attribute
It is not inside a JavaScript string context
It is inside an HTML body context

Therefore: No need to break out of quotes, No need for attribute escaping, Direct tag injection is possible, This is a classic HTML Body Reflected XSS scenario.

Browser Parsing Mechanism

After the server generates the response, the process continues entirely on the client (browser) side.

Example response:

```
<h1>0 results for '<script>alert(document.domain)</script>'</h1>
```

The browser follows these steps:

The HTML parser starts building the DOM tree

An `<h1>` node is created

The content is parsed
The <script> token is detected
A script node is added to the DOM
The JavaScript engine executes it synchronously
As a result, the exploit:
Executes when the page loads
Requires no additional user interaction
Results in client-side code execution

## 4– Exploitation

Objective: Execute arbitrary JavaScript code.

I entered the following payload into the search box:
```
<script>alert('Hacked')</script>
```

After clicking the search button, the server generates the following response:

```
<h1>0 results for '<script>alert(document.domain)</script>'</h1>
```

The browser interprets the `<script>` tag as a valid HTML node and executes the JavaScript code inside it.

The appearance of the alert box confirms the presence of the vulnerability.

## 5– Security Impact

In a real-world scenario, this vulnerability could lead to:

→ Session Hijacking

If the HttpOnly flag is not set, session cookies can be stolen using document.cookie.

→ CSRF Token Exfiltration

Hidden input fields on the page can be read and exfiltrated.

→ Phishing Injection

An attacker can inject a fake login form.

→ Privilege Abuse

If the victim is an admin:
User deletion
Permission modification
Data manipulation

Reflected XSS is generally considered Medium severity because it requires user interaction. However, if a high-privileged user is targeted, the risk level increases significantly.

## 6– How Could This Vulnerability Be Prevented?

The fundamental rule:

User input must never be rendered as-is.
Before inserting user input into the HTML context, proper output encoding must be applied.

Incorrect Implementation
```
<h1>... '<script>alert(1)</script>'</h1>
Correct Implementation
<h1>... '&lt;script&gt;alert(1)&lt;/script&gt;'</h1>
```

In this case, the browser interprets <script> as plain text instead of executable code.

Alternatively:

Use frameworks with auto-escaping mechanisms
Implement a proper Content Security Policy (CSP)

## 7– Conclusion

In this lab, it was identified that:

User input is reflected in the HTML body context without encoding
During browser parsing, a script node is created
Arbitrary JavaScript execution is possible
The root cause of the vulnerability is the lack of proper output encoding.
