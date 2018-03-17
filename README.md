# Calling MXroute's cPanel API from Python

This is a simple Python 3 class that demonstrates how to call MXroute's cpanel API for manipulating email accounts.  The class is not comprehensive, nor is it bullet-proof, and so you will want to consider this mostly as an example to use to build your own, more appropriate code.

The motivation for writing this merely because there's very little information out there to help get started with calling the API, and so after I figured it out I thought the best way to document it was with working code.

## Using the class

Here is a quick tester you can use to to verify the code works:

```python
import MXroute

mx = MXroute.MXroute('youruserid', 'yourpassword')

print(mx.list_domains())
print(mx.single_domain_data('foobar.com'))
print(mx.add_forwarder('foo@foobar.com', 'foo@barfoo.com'))
print(mx.list_forwarders('foobar.com'))
print(mx.delete_forwarder('foo@foobar.com', 'foo@barfoo.com'))
print(mx.add_pop('admin@foobar.com', 'admin1234', 256))
print(mx.change_pop_password('admin@foobar.com', 'admin5678'))
print(mx.change_pop_quota('admin@foobar.com', 128))
print(mx.delete_pop('admin@foobar.com'))
```

##### Where do you get the user id and password?

That had me confused too.  When you first create an account with MXroute, one of the emails you receive is  entitled `[MXroute] Important Account Information`.  You can retrieve that email by going to the `Hello user` dropdown in the upper right and picking Email History.

In that email, look for the line `cPanel Login URL`.  That contains the server information (in case you need to change that), the username, and the password for the cPanel account.  This is what you use to connect via the API.

## Extending the Class with New API Calls

I only implemented a subset of the API calls supported by cPanel. If you wish to add more, you can follow the patterns in the code and reference the cPanel documentation for how to make additional calls:

https://documentation.cpanel.net/display/DD/UAPI+Modules+-+Email

